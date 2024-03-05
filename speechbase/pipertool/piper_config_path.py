#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2023/12/5 15:32
File: piper_config_path.py
Software: PyCharm
"""
import os
p_path = os.path.dirname(__file__)

config_path = {
    "model_joe_path": os.path.join(os.path.join(p_path,'models'), "en_US-joe-medium.onnx"),
    "piper_path": os.path.join(p_path,"piper.exe")
}