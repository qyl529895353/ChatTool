#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2023/12/5 17:50
File: bak_speech_to_text.py
Software: PyCharm
"""
import os
import websocket
import asyncio
import logging
import uuid
import json
import threading
import time
from functools import partial
import const
from text_to_speech import BaiduTTS
from chatbase.openai_chat import chat

logger = logging.getLogger()

class SpeechRecognitionClient:
    def __init__(self):
        self.ws = None

    def send_start_params(self):
        req = {
            "type": "START",
            "data": {
                "appid": const.APPID,
                "appkey": const.APPKEY,
                "dev_pid": const.DEV_PID,
                "cuid": "yourself_defined_user_id",
                "sample": 16000,
                "format": "pcm"
            }
        }
        body = json.dumps(req)
        self.ws.send(body, websocket.ABNF.OPCODE_TEXT)
        logger.info("send START frame with params:" + body)

    def send_audio(self,pcm_file):
        chunk_ms = 160
        chunk_len = int(16000 * 2 / 1000 * chunk_ms)
        with open(pcm_file, 'rb') as f:
            pcm = f.read()

        index = 0
        total = len(pcm)
        logger.info("send_audio total={}".format(total))
        while index < total:
            end = index + chunk_len
            if end >= total:
                end = total
            body = pcm[index:end]
            logger.debug("try to send audio length {}, from bytes [{},{})".format(len(body), index, end))
            self.ws.send(body, websocket.ABNF.OPCODE_BINARY)
            index = end
            time.sleep(chunk_ms / 1000.0)

    def send_finish(self):
        req = {
            "type": "FINISH"
        }
        body = json.dumps(req)
        self.ws.send(body, websocket.ABNF.OPCODE_TEXT)
        logger.info("send FINISH frame")

    def send_cancel(self):
        req = {
            "type": "CANCEL"
        }
        body = json.dumps(req)
        self.ws.send(body, websocket.ABNF.OPCODE_TEXT)
        logger.info("send Cancel frame")

    def on_open(self, pcm_file,ws):
        def run(*args):
            self.send_start_params()
            self.send_audio(pcm_file)
            self.send_finish()
            logger.debug("thread terminating")

        threading.Thread(target=run).start()

    def on_message_wrapper(self,ws, message):
        # logger.info("Response: " + message)
        message_json = json.loads(message)
        if message_json["type"] == "FIN_TEXT":
            print(message_json["result"])
            baidu_tts = BaiduTTS(const.APPID,const.APPKEY,const.SECRETKEY)
            reply = chat.chat_with_origin_model(message_json["result"])
            if reply != None:
                asyncio.run(baidu_tts.text_to_speech_and_play(reply))
            return

    def on_error(self, ws,error):
        logger.error("error: " + str(error))

    def on_close(self, ws,close_status_code, close_msg):

        logger.info("ws close ...")
        ws.close()

    def run_forever(self,pcm_file):
        uri = const.URI + "?sn=" + str(uuid.uuid1())
        logger.info("uri is " + uri)
        self.ws = websocket.WebSocketApp(uri,
                                         on_open=partial(self.on_open,pcm_file),
                                         on_message=self.on_message_wrapper,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.run_forever()

    def get_record(self, is_get_audio: bool = False, rate=16000,file_name="./speech.wav"):
        import speech_recognition as sr
        r = sr.Recognizer()

        with sr.Microphone(sample_rate=rate) as source:
            print('请开始说话')
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=5)
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
    def _get_file_content(self, file_name):
        with open(file_name, 'rb') as f:
            audio_data = f.read()
        return audio_data

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)-15s] [%(funcName)s()][%(levelname)s] %(message)s')
    logger.setLevel(logging.DEBUG)
    logger.info("begin")
    speech_client = SpeechRecognitionClient()
    file_name = "test3.wav"
    speech_client.get_record(file_name=file_name)
    if os.path.getsize(file_name) > 0:
        speech_client.run_forever(file_name)
