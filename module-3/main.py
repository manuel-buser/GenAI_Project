import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import AzureChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

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

index_name: str = "products"
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    azure_search_key=os.getenv("AZURE_SEARCH_KEY"),
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)




retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(), llm=model
)

template = """Answer the question based only on the following context and ensure to include citations (ie: hometheatersystem.txt, smartphone1.txt etc.):
{context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

retrieval_chain = (
    {"context": retriever_from_llm, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

print(retrieval_chain.invoke("what is the price of the home theater system?"))