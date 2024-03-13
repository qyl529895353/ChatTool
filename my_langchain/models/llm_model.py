#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2024/3/13 19:18
File: llm_model.py
Software: PyCharm
"""

from langchain.chat_models import ChatOpenAI
from config.keys import Keys

def get_openai_model():
    llm_model = ChatOpenAI(openai_api_key=Keys.OPENAI_API_KEY)
    return llm_model

