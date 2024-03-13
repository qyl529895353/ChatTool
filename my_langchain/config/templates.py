#  -*- coding: utf-8 -*-
"""
Author: loong
Time: 2024/3/13 19:15
File: templates.py
Software: PyCharm
"""

# 机器人template
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://img2.baidu.com/it/u=766326307,4287015855&fm=253&fmt=auto&app=120&f=BMP?w=500&h=500" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

# 用户template
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img2.baidu.com/it/u=2666658595,3580480011&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=498" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''