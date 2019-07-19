# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 19:44:55 2018

@author: xiaozhe
"""
import wxpy
import pickle
import os
import logging
import time
logging.basicConfig(level=logging.DEBUG, format='%(msg)s')
logging.disable(level=logging.DEBUG)
logging.warning('logging in...')
# 导入聊天记录
if os.path.exists('wechatrobotmsgrecord.pkl'):
    with open('wechatrobotmsgrecord.pkl', 'rb') as file:
        chatRecord = pickle.load(file)
else:
    chatRecord = {'ask': [], 'answer': []}

bot = wxpy.Bot(cache_path=True)
bot.enable_puid('wxpy_puid.pkl')

auto_reply_persons_1 = ['xx', 'xx']
auto_friends_1 = []
for person in auto_reply_persons_1:
    auto_friends_1.append(wxpy.ensure_one(bot.chats().search(person)))

xiaomo = wxpy.ensure_one(bot.chats().search('xx'))
sansan = wxpy.ensure_one(bot.chats().search(''))

tuling = wxpy.Tuling(api_key='xxxxxxxxxxxxxxxxxx')
# global auto_friends
auto_friends = auto_friends_1


@bot.register(auto_friends)
def auto_reply_1(msg):
    # global auto_friends
    if msg.type in [wxpy.TEXT]:
        if msg.sender == xiaomo and msg.text == 'LOGOUT':
            bot.logout()
            return
        # elif msg.sender == xiaomo and msg.text == 'STOP':
        #     auto_friends = [sansan]
        #     return 'stop tuling'
        # elif msg.sender == xiaomo and msg.text == 'START':
        #     auto_friends = auto_friends_1
        #     return 'start tuling'
        else:
            reply_text = tuling.do_reply(msg)
            chatRecord['answer'].append(reply_text.strip())
            chatRecord['ask'].append(msg.text.strip())
            logging.warning('ask: ' + msg.text + '\nanswer: ' + reply_text)
    #        return '{}'.format('ok')
    elif msg.type == wxpy.RECORDING:
        return '{}'.format('啥？不方便语音，发文字')
    else:
        return '干嘛呢？'


logging.warning('listening...')
while bot.alive:
    time.sleep(0.5)

# logging.warning('saving chat history...')
# with open('wechatrobotmsgrecord.pkl', 'wb') as file:
#     pickle.dump(chatRecord, file)
# logging.warning('exit')
