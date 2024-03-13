#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2024/3/13 19:17
File: embedding_model.py
Software: PyCharm
"""
from config.keys import Keys
from langchain.embeddings.openai import OpenAIEmbeddings
def get_openaiEmbedding_model():

    return OpenAIEmbeddings(openai_api_key=Keys.OPENAI_API_KEY)
