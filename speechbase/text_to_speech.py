#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2023/12/5 14:27
File: text_to_speech.py
Software: PyCharm
"""
import os
import time

import pyttsx3
import pygame
from aip import AipSpeech
class Pyttsx3TTS:
    """
    python text to speech 比较机械
    """
    def __init__(self):
        pass

    def text_to_speech_and_play(self, text=""):
        engine = pyttsx3.init()
        # for i in engine.getProperty('voices'):
        #     print(i)
        engine.say(text)
        engine.runAndWait()

class PiperTTS:
    """
    piper 文字转语音
    """
    def __init__(self):
        pass

    def text_to_speech_and_play(self, text="", out_dict=None):
        if out_dict == None:
            return
        tool_path = out_dict["tool_path"]
        model_path = out_dict["model_path"]
        out_file = out_dict["out_file"]
        cmd = """
        echo '%s' | %s -m %s -f %s
        """%(text, tool_path, model_path,out_file)
        os.system(cmd)
        if os.path.exists(out_file):
            self.play_audio(out_file)
            os.remove(out_file)
    def play_audio(self, audio_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

class BaiduTTS:
    """
    使用百度TTs sdk 接口，可以对硬件上要求不高
    """
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = str(APP_ID)
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def text_to_speech_and_play(self, text=""):
        result = self.client.synthesis(text, 'zh', 1, {
            'spd': 5,
            'vol': 5,
            'per': 4
        })

        file_audio ="./audio%s.mp3"%time.time()
        if not isinstance(result, dict):
            with open(file_audio, "wb") as f:
                f.write(result)
        else:
            raise EOFError("语音合成失败:%s"%result)
        self.play_audio(file_audio)

    def play_audio(self, audio_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        if os.path.exists(audio_file_path):
            os.remove(audio_file_path)

if __name__=="__main__":
    from common import const

    # piper_tts = PiperTTS()
    # tool_path = config_path['piper_path']
    # model_path = config_path["model_joe_path"]
    # print(tool_path,model_path)
    # out_file = "./test.wav"
    # out_dict = dict()
    # out_dict["tool_path"] = tool_path
    # out_dict["model_path"] = model_path
    # out_dict["out_file"] = out_file
    # piper_tts.text_to_speech_and_play("It adapts to long gaming sessions while reducing hand fatigue",out_dict)



    # pytts = Pyttsx3TTS()
    # pytts.text_to_speech_and_play("text_to_speech_and_play")

    baidu_tts = BaiduTTS(str(const.APPID), const.APPKEY, const.SECRETKEY)
    baidu_tts.text_to_speech_and_play("今天是几月几号")