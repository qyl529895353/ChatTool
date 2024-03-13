#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2024/3/13 19:19
File: utils_file.py
Software: PyCharm
"""

from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from models.llm_model import get_openai_model
import streamlit as st
from config.templates import bot_template, user_template

from config.keys import Keys
from PyPDF2 import PdfReader,PdfFileReader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pinecone
import base64
def extract_text_from_PDF(files):
    # 加载多个PDF文件
    text = ""
    for pdf in files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def read_pdf(files):

    loader = PyPDFLoader(files)
    return loader.load_and_split()

def split_content_into_chunks(text):
    text_spliter = CharacterTextSplitter(separator="\n",
                                         chunk_size=500,
                                         chunk_overlap=80,
                                         length_function=len)
    chunks = text_spliter.split_text(text)
    return chunks




def split_dos(pages):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap = 50)
    docs = text_splitter.split_documents(pages)
    return docs


def save_chunks_into_vectorstore(content_chunks, embedding_model):
    vectorstore = FAISS.from_texts(texts=content_chunks,
                                      embedding=embedding_model)
    return vectorstore


def get_chat_chain(vector_store):
    #获取 LLM model
    llm = get_openai_model()

    # 用于缓存或者保存对话历史记录的对象
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    # 对话链
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain



def process_user_input(user_input):
    if st.session_state.conversation is not None:
        # 调用函数st.session_state.conversation，并把用户输入的内容作为一个问题传入，返回响应。
        # result = vector_store.similarity_search(user_input ,k = 3)
        # source_know = "\n".join([x.page_content for x in result])
        # question = f"""
        # 基于这块内容{source_know}回答问题下面的问题
        # Query:{user_input}
        # """
        response = st.session_state.conversation({'question': user_input})
        st.session_state.chat_history = response['chat_history']
        # chat_history : 一个包含之前聊天记录的列表
        for i, message in enumerate(st.session_state.chat_history):
            # 用户输入
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                # 机器人响应
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
    else:
        st.write(user_template.replace(
            "{{MSG}}", user_input), unsafe_allow_html=True)
        st.write(bot_template.replace(
            "{{MSG}}", "不知道你说的问题"), unsafe_allow_html=True)


