#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2024/3/13 19:28
File: main.py
Software: PyCharm
"""
import streamlit as st
from utils.utils_file import extract_text_from_PDF, split_content_into_chunks,read_pdf,split_dos
from utils.utils_file import save_chunks_into_vectorstore, get_chat_chain, process_user_input
from models.embedding_model import get_openaiEmbedding_model


def main():
    # 配置界面
    st.set_page_config(page_title="基于PDF文档的 QA ChatBot",
                       page_icon=":robot:")

    st.header("LLM ChatBot PDF")
    user_input = st.text_input("基于上传的PDF文档，请输入你的提问: ")
    # 处理用户输入，并返回响应结果

    if user_input:
        process_user_input(user_input)

    # 初始化
    # session_state用于存储会话状态的功能
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    vector_store = None
    with st.sidebar as g:
        # 设置子标题
        st.subheader("你的PDF文档")
        # 上传文档
        files = st.file_uploader("上传PDF文档，然后点击'提交并处理'",
                                 accept_multiple_files=True)

        if st.button("提交并处理"):
            with st.spinner("请等待，处理中..."):
                # 获取PDF文档内容
                texts = extract_text_from_PDF(files)
                # 将获取到的文档内容进行切片
                content_chunks = split_content_into_chunks(texts)

                embedding_model = get_openaiEmbedding_model()
                # 创建向量数据库对象，并将文本embedding后存入
                vector_store = save_chunks_into_vectorstore(content_chunks, embedding_model)
                # 创建对话chain

                st.session_state.conversation = get_chat_chain(vector_store)


if __name__ == "__main__":
    main()