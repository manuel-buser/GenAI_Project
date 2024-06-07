import os
from dotenv import load_dotenv
import streamlit as st
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_community.retrievers import AzureAISearchRetriever
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Load environment variables
load_dotenv()

# Define the prompts and models
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

model = AzureChatOpenAI(
    azure_deployment="gpt4o",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

retriever = AzureAISearchRetriever(
    content_key="content", top_k=5, index_name="product-info", api_key=os.getenv("AZURE_SEARCH_KEY"), service_name="genai-on-azure-search"
)

history_aware_retriever = create_history_aware_retriever(
    model, retriever, contextualize_q_prompt
)

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# Chat history store
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

# Streamlit app
st.title("Generic Tech Shop Inc. Customer Service Bot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def submit():
    user_input = st.session_state.user_input
    st.session_state.user_input = ""
    if user_input:
        result = conversational_rag_chain.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": "1"}}
        )
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Bot", result["answer"]))

st.text_input("Your Question", key="user_input", on_change=submit)

# Add JavaScript to trigger form submission on Enter key press
st.markdown(
    """
    <script>
    const inputBox = parent.document.querySelector('input[type="text"]');
    inputBox.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const inputElement = parent.document.querySelector('button[type="submit"]');
            inputElement.click();
        }
    });
    </script>
    """,
    unsafe_allow_html=True
)

for sender, message in st.session_state.chat_history:
    if sender == "User":
        st.markdown(f"**{sender}:** {message}")
    else:
        st.markdown(f"**{sender}:** {message}")
