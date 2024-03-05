#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2023/12/5 15:45
File: speech_to_text.py
Software: PyCharm
"""
import const
from aip import AipSpeech
import speech_recognition as sr
class BaiduASR:
    def __init__(self, APP_ID, API_KEY, SECRET_KEY):
        self.APP_ID = str(APP_ID)
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        self.r = sr.Recognizer()

    # 从麦克风收集音频并写入文件

    def get_record(self, is_get_audio: bool = False, rate=16000,file_name="./speech.wav"):
        with sr.Microphone(sample_rate=rate) as source:
            print('请开始说话')
            try:
                audio = self.r.listen(source, timeout=10, phrase_time_limit=5)
            except:
                audio = None
        if audio == None:
            return audio
        with open(file_name, "wb") as f:
            f.write(audio.get_wav_data())

        if is_get_audio:
            return audio
        else:
            return self._get_file_content(file_name)

    # 从本地文件中加载音频 作为后续百度语音服务的输入
    def _get_file_content(self, file_name):
        with open(file_name, 'rb') as f:
            audio_data = f.read()
        return audio_data

    def speech_to_text(self, audio_path: str = "test.wav", is_mic: bool = True, mic_file="./speech.wav"):
        # 麦克风输入
        if is_mic:
            info = self.get_record(is_get_audio=False,file_name=mic_file)
            if info == None:
                return "语音识别失败："
            else:
                result = self.client.asr(info, 'wav', 16000, {
                    'dev_pid': 1537  # 识别中文普通话
                })
        # 从文件中读取
        else:
            result = self.client.asr(self._get_file_content(audio_path), 'wav', 16000, {
                'dev_pid': 1537  # 识别中文普通话
            })
        if result["err_msg"] != "success.":
            return "语音识别失败：" + result["err_msg"]
        else:
            return result['result'][0]

if __name__ == "__main__":
    import const
    obj = BaiduASR(const.APPID,const.APPKEY,const.SECRETKEY)
    print(obj.speech_to_text(mic_file='test1.wav'))