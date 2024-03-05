#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2023/12/5 19:11
File: main.py
Software: PyCharm
"""
import os
from speechbase.wakeword import PicoWakeWord
from speechbase.speech_to_text import BaiduASR
from speechbase.speech_to_text_real_time_asr import BaiduTTS as BaiduTTSRealTime
from speechbase.text_to_speech import Pyttsx3TTS,PiperTTS, BaiduTTS
from chatbase.openai_chat import chat
from speechbase import const
import asyncio
import struct
PICOVOICE_API_KEY = ""  # 你的picovoice key
keyword_path = './speechbase/Hey-Murphy_en_mac_v2_1_0.ppn'  # 你的唤醒词检测离线文件地址




def lisen_run(picowakeword, asr, tts,real_time):
    while True:  # 常驻唤醒词的监听
        audio_obj = picowakeword.stream.read(picowakeword.porcupine.frame_length, exception_on_overflow=False)
        audio_obj_unpacked = struct.unpack_from("h" * picowakeword.porcupine.frame_length, audio_obj)
        keyword_idx = picowakeword.porcupine.process(audio_obj_unpacked)
        if keyword_idx >= 0:
            picowakeword.porcupine.delete()
            picowakeword.stream.close()
            picowakeword.myaudio.terminate()  # 需要对取消对麦克风的占用!

            print("嗯,我在,请讲！")
            asyncio.run(tts.text_to_speech_and_play("嗯,老大我在,请讲！"))
            while True:
                file_name = "real_time.wav"
                if real_time:
                    asr.get_record(file_name=file_name)
                    if os.path.getsize(file_name) > 0:
                        asr.run_forever(file_name)
                else:# 进入一次对话
                    q = asr.speech_to_text(mic_file=file_name)
                    res = chat.chat_with_agent(q)
                    asyncio.run(tts.text_to_speech_and_play(res))
                if os.path.exists(file_name):
                    os.remove(file_name)


def clean_picowakeword(picowakeword):
    if picowakeword.porcupine is not None:
        picowakeword.porcupine.delete()
    if picowakeword.stream is not None:
        picowakeword.stream.close()
    if picowakeword.myaudio is not None:
        picowakeword.myaudio.terminate()
def star_func():
    picowakeword = PicoWakeWord(PICOVOICE_API_KEY, keyword_path)
    asr = BaiduASR(const.APPID,const.APPKEY,const.SECRETKEY)
    tts = BaiduTTS(const.APPID,const.APPKEY,const.SECRETKEY)
    real_time = False
    # asr_real_time = BaiduTTSRealTime(const.APPID,const.APPKEY,const.SECRETKEY)
    # real_time =  True


    try:
        lisen_run(picowakeword, asr, tts, real_time)
    except KeyboardInterrupt:
            clean_picowakeword(picowakeword)
            exit(0)
    finally:
        asyncio.run(tts.text_to_speech_and_play('老大，没事我退下啦'))
        clean_picowakeword(picowakeword)

        star_func()

if __name__ == '__main__':
    star_func()
