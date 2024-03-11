# pip install -r requirements.txt

import gradio as gr
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import HuggingFaceEndpoint

from pathlib import Path
import chromadb
from unidecode import unidecode

from transformers import AutoTokenizer
import transformers
import torch
import tqdm
import accelerate

def load_doc(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1024, chunk_overlap = 128)
    doc_splits = text_splitter.split_documents(pages)
    return doc_splits



splt = load_doc('data.pdf')

def initialize_database(file_path):
    # Create list of documents (when valid)
    collection_name = Path(file_path).stem
    # Fix potential issues from naming convention
    ## Remove space
    collection_name = collection_name.replace(" ","-")
    ## Limit lenght to 50 characters
    collection_name = collection_name[:50]
    ## Enforce start and end as alphanumeric character
    if not collection_name[0].isalnum():
        collection_name[0] = 'A'
    if not collection_name[-1].isalnum():
        collection_name[-1] = 'Z'
    # print('list_file_path: ', list_file_path)
    print('Collection name: ', collection_name)
    # Load document and create splits
    doc_splits = load_doc(file_path)
    # global vector_db
    vector_db = create_db(doc_splits, collection_name)
    return vector_db, collection_name, "Complete!"

def create_db(splits, collection_name):
    embedding = HuggingFaceEmbeddings()
    new_client = chromadb.EphemeralClient()
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=embedding,
        client=new_client,
        collection_name=collection_name,
    )
    return vectordb

vec = initialize_database('data.pdf')

vec_cre = create_db(splt, 'data')


def initialize_llmchain(temperature, max_tokens, top_k, vector_db):
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key='answer',
        return_messages=True
    )

    llm = HuggingFaceEndpoint(
            repo_id='mistralai/Mixtral-8x7B-Instruct-v0.1',
            temperature = temperature,
            max_new_tokens = max_tokens,
            top_k = top_k,
            load_in_8bit = True 
            #Vous pouvez ajouter ici votre huggingfacehub_api_token comme variable ou bien mieux dans votre espace d'environement
      
        )
    retriever=vector_db.as_retriever()
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        chain_type="stuff",
        memory=memory,
        return_source_documents=True,
        verbose=False,
    )
    return qa_chain

qa = initialize_llmchain(0.6, 1024, 40, vec_cre) #The model question answer

pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr") # This pipeline translate english to french , it isn't adviced as it add more latency


def format_chat_history(message, chat_history):
    formatted_chat_history = []
    for user_message, bot_message in chat_history:
        formatted_chat_history.append(f"User: {user_message}")
        formatted_chat_history.append(f"Assistant: {bot_message}")
    return formatted_chat_history

def conversation(message, history):
    formatted_chat_history = format_chat_history(message, history)

    # Generate response using QA chain
    response = qa({"question": message, "chat_history": formatted_chat_history})
    response_answer = response["answer"]
    if response_answer.find("Helpful Answer:") != -1:
        response_answer = response_answer.split("Helpful Answer:")[-1]
    #You can also return from where the model got the answer to fine-tune or adjust your model mais ici c'est bon
    response_sources = response["source_documents"]
    response_source1 = response_sources[0].page_content.strip()
    response_source2 = response_sources[1].page_content.strip()
    response_source3 = response_sources[2].page_content.strip()
    response_source1_page = response_sources[0].metadata["page"] + 1
    response_source2_page = response_sources[1].metadata["page"] + 1
    response_source3_page = response_sources[2].metadata["page"] + 1
    #If you want the return in english leave it at :
    return response_answer

    #If you want the return in french
    #return pipe(response_answer)[0]['translation_text'] + " (Traduis d'anglais en français)"



gr.ChatInterface(conversation).launch()
