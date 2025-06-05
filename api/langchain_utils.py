from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
import os
from chroma_utils import vectorstore

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
output_parser = StrOutputParser()

os.environ["GOOGLE_API_KEY"] = "AIzaSyAghcgqCcTFZC_4Ryt9mdqgBTnUwChwYuY"

# Set up prompts and chains
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant. Use the following context to answer the user's question. 
    
    Guidelines:
    - If the context contains relevant information, use it to provide a comprehensive answer
    - If the context doesn't contain relevant information, politely say that you don't have enough information to answer based on the provided documents
    - For simple greetings like 'hi', 'hello', respond naturally and ask how you can help
    - Always be helpful and conversational
    - Don't mention policy violations or safety concerns unless there's actual harmful content"""),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

def get_rag_chain(model="gpt-4o-mini"):
    # Simple configuration without safety settings to avoid compatibility issues
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.7,
        max_output_tokens=1000
    )
    
    # Alternative: Use OpenAI if Gemini continues to be problematic
    # llm = ChatOpenAI(model=model, temperature=0.7)
    
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain