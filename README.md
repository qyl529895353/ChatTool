# ChatGpt智能语音对话

## TODO LIST
### ~~唤醒功能 picovoice 支持多平台 https://picovoice.ai~~
### ~~文本转语音 (TTS)~~
    1.open ai  (有限的免费额度) 优点：声音质量好 缺点:限额，频繁使用容易异常 ,这里我没使用它~~
    2.百度智能云 (免费使用额度大) 声音质量不错，可选声音模型也多 
    3.pyttsx3  (python库) 优点：不要钱，速度也快 缺点：声音就是机器人
    4.Piper 国外开源工具 转换速度很快，声音质量没 open ai的好；
      piper git地址https://github.com/rhasspy/piper 
      不过在安装依赖的时候piper-phonemize有冲突，后面有时间在去看看，我重新找到另外一个
      作者：natlamir 将piper编译了还有Ui界面使用 仓库地址：https://github.com/natlamir/PiperUI
### ~~语音识别（ASR）~~
    1.open ai  (有限的免费额度) 用whisper 模型就行 ,这里我没使用它
    2.百度智能云 (免费使用额度大) 有流式识别和普通识别，流式快一点
### ~~chat对话功能~~
    1.open ai  (有限的免费额度) 用的 gpt-3.5 模型 缺点openai 2022年1月份的时候被训练所以你问现在日期会有问题

## 搭建属于自己免费应用(优化版)
### 文本转语音 (TTS)
    1.Piper
    2.EmotiVoice 
    基于上面2选1，做文本转语音，同时训练自己的声音模型
### 语音识别（ASR）
    基于 faster-whisper 去实现语音识别
### chat对话功能
    基于ChatGLM3模型 + Langchain 实现

### PS：仅用于学习和交流