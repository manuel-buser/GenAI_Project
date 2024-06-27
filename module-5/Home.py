import os
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from semantic_router.layer import RouteLayer, Route
from semantic_router.encoders import AzureOpenAIEncoder
from langchain_community.vectorstores.azuresearch import AzureSearch

load_dotenv()

model = AzureChatOpenAI(
    azure_deployment="gpt4o",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    azure_deployment="embeddings",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

index_name: str = "products-optimized"
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    azure_search_key=os.getenv("AZURE_SEARCH_KEY"),
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)

small_talk = Route(
    name="small_talk",
    utterances=[
        "Hey, how are you?", 
        "How's it going?",
        "Nice weather today"
    ],
)

headphones_questions = Route(
    name="headphones_questions",
    utterances=[
        "How much do the ClearSound X7 headphones cost?",
        "What headphones do you offer?",
        "What features does the SoundWave Elite 900 have?"
    ],
)

laptop_questions = Route(
    name="laptop_questions",
    utterances=[
        "How much do the TechMax UltraBook 14 laptop cost?",
        "What laptops do you offer?",
        "What features does the SwiftBook Pro 13 have?"
    ],
)

smartphone_questions = Route(
    name="smartphone_questions",
    utterances=[
        "How much do the TechMax NexTech Pro X smartphone cost?",
        "What smartphones do you offer?",
        "What features does the Galaxy Star G5 have?"
    ],
)

smartwatch_questions = Route(
    name="smartwatch_questions",
    utterances=[
        "How much do the FitGear 6X smartwatch cost?",
        "What smartwatchs do you offer?",
        "What features does the ChronoTrack A1 have?"
    ],
)

home_theater_questions = Route(
    name="home_theater_questions",
    utterances=[
        "How much does the Ultimate Home Theater System cost?",
        "What home theater packages do you offer?",
        "What features does the Ultimate Home Theater System have?"
    ],
)

routes = [small_talk, headphones_questions, laptop_questions, smartphone_questions, smartwatch_questions, home_theater_questions]
encoder = AzureOpenAIEncoder(api_key=os.getenv("AZURE_OPENAI_API_KEY"), deployment_name="embeddings", azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), api_version="2024-02-15-preview", model="text-embedding-ada-002")
rl = RouteLayer(encoder=encoder, routes=routes)

laptop_prompt = """Your job is to answer questions on laptops
Answer the question based only on the following context and be sure to include citations (ie: laptop1 or laptop2):
{context}

Question: {question}
"""

smartphone_prompt = """Your job is to answer questions on smartphones
Answer the question based only on the following context and be sure to include citations (ie: smartphone1 or smartphone2):
{context}

Question: {question}
"""

headphone_prompt = """Your job is to answer questions on headphones
Answer the question based only on the following context and be sure to include citations (ie: headphones1 or headphones2):
{context}

Question: {question}
"""

smartwatch_prompt = """Your job is to answer questions on smartwatches
Answer the question based only on the following context and be sure to include citations (ie: smartwatch1 or smartwatch2):
{context}

Question: {question}
"""

home_theater_prompt = """Your job is to answer questions on the home theater package we sell
Answer the question based only on the following context and be sure to include citations (ie: hometheatersystem):
{context}

Question: {question}
"""

small_talk_prompt = ChatPromptTemplate.from_template("""Your job is a friendly customer service bot. Respond to the user in a 
friendly way and remind them we have lots of tech products like headphones, smartwatches, laptops, and more and ask how you can help.

Input: {input}
""")

chat_history_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
    "Original Question: {original_question}"
    "Chat History: {chat_history}"
)

retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(), llm=model
)

def semantic_layer(query: str):
    route = rl(query)
    result = None 

    if route.name == "laptop_questions":
        prompt = ChatPromptTemplate.from_template(laptop_prompt)
        retrieval_chain = (
            {"context": retriever_from_llm, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        result = retrieval_chain.invoke(query)
    elif route.name == "headphones_questions":
        prompt = ChatPromptTemplate.from_template(headphone_prompt)
        retrieval_chain = (
            {"context": retriever_from_llm, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        result = retrieval_chain.invoke(query)
    elif route.name == "smartphone_questions":
        prompt = ChatPromptTemplate.from_template(smartphone_prompt)
        retrieval_chain = (
            {"context": retriever_from_llm, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        result = retrieval_chain.invoke(query)
    elif route.name == "smartwatch_questions":
        prompt = ChatPromptTemplate.from_template(smartwatch_prompt)
        retrieval_chain = (
            {"context": retriever_from_llm, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        result = retrieval_chain.invoke(query)
    elif route.name == "home_theater_questions":
        prompt = ChatPromptTemplate.from_template(home_theater_prompt)
        retrieval_chain = (
            {"context": retriever_from_llm, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
        )
        result = retrieval_chain.invoke(query)
    elif route.name == "small_talk":
        chain = small_talk_prompt | model | StrOutputParser()
        result = chain.invoke({"input": query})
    else:
        return "Sorry, I cannot help you with that."
    
    return result

class ChatHistory:
    def __init__(self):
        self.queries = []

    def add_query(self, query):
        if len(self.queries) >= 10:
            self.queries.pop(0)
        self.queries.append(query)

    def get_queries(self):
        return self.queries
    

chat_history = ChatHistory()

def process_chat_history(question, chat_history):
    prompt = ChatPromptTemplate.from_template("Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
        "Original Question: {question}"
        "Chat History: {chat_history}")
    chain = prompt | model | StrOutputParser()
    result = chain.invoke({"question": question, "chat_history": chat_history})
    return result

# Streamlit app
st.title("Generic Tech Shop Inc. Customer Service Bot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def submit():
    user_input = st.session_state.user_input
    st.session_state.user_input = ""
    if user_input:
        chat_history.add_query(f"Human: {user_input}")
        result = process_chat_history(user_input, chat_history.get_queries())
        answer = semantic_layer(result)
        chat_history.add_query(f"AI: {answer}")
        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Bot", answer))

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
