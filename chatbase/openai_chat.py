#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2023/12/5 13:29
File: openai_chat.py
Software: PyCharm
"""

import openai
#密钥获取https://platform.openai.com/api-keys
openai_api_key = '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'

class OpenaiChat:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.origin_model_conversation = [{"role": "system", "content": "你是用户user啊秋的好朋友，你们经常用中文聊天，你的名字叫喵喵."}]

    def chat_with_origin_model(self, text):
        openai.api_key = self.openai_api_key
        text = text.replace('\n', ' ').replace('\r', '').strip()
        if len(text) == 0:
            return
        self.origin_model_conversation.append({"role": "user", "content": text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.origin_model_conversation,
            max_tokens=2048,
            temperature=0.3,
        )
        reply = response.choices[0].message.content
        if reply and isinstance(reply,str):
            reply = reply.strip("喵喵：")
        print("reply:%s"%reply)
        self.origin_model_conversation.append({"role": "assistant", "content": reply})
        if len(self.origin_model_conversation) > 5:
            self.origin_model_conversation =self.origin_model_conversation[-5:]
        return reply

    def chat_with_agent(self,text):
        """
        Todo 基于代理实现对话，解决openai 2022年1月份的时候被训练，没有实时钟表功能
        """
        pass

chat = OpenaiChat(openai_api_key)
if __name__=="__main__":
    pass
    # chat_obj = OpenaiChat(openai_api_key)
    # print(chat_obj.chat_with_origin_model('今天是几月几号'))
