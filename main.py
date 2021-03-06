from email import message
from typing import Text
import telebot
from dotenv import load_dotenv
import os 
import requests
from bs4 import BeautifulSoup
import json

api="2010690749:AAEc3sPXTP4YrVnCSxxI2oUvlz5j6LNFS2g"
bot=telebot.TeleBot(api)


def getMeaning(word):
    url=f"https://www.myordbok.com/definition?q={word}"
    webpage=requests.get(url)
    soup=BeautifulSoup(webpage.content,"html.parser")
    formatted=""""""
    try:
        meaningList=soup.find("div",class_="meaning")
        pos=meaningList.find_all("div",class_="pos")
        for i in pos:
            letter_type=i.find_all("h2")[0].getText()
            formatted+=f"\n {letter_type} \n\n"
            text=i.find_all("p")
            for elem in text:
                myanmar_meaning=elem.getText()
                formatted+=f"{myanmar_meaning}"
        print(formatted)
    except:
        formatted="Can't Find Your Wrods"
    return formatted

@bot.message_handler(commands="start")
def start(message):
    text="Welcom to Eng-MM Dictionary Bot.\n Here are the command\n/search word \n/inspire \n/about "
    bot.send_message(message.chat.id,text)
    print(message.chat.id)

@bot.message_handler(commands=["search"])
def search(message):
    text = message.text
    text = text.replace("/search ","")
    print(text)
    meaning=getMeaning(text)
    bot.send_message(message.chat.id,meaning)
    print(message.chat.id)


@bot.message_handler(content_types=["sticker", "video", "photo", "audio", "voice", "location", "contact", "document"])
def forward(message):
    data = "From {} {}({})".format(message.from_user.first_name, message.from_user.last_name,message.from_user.username)
    bot.forward_message(-1001680314281, message.chat.id, message.message_id)
    bot.send_message(-1001680314281, data)

@bot.message_handler(commands=["about"])
def about(message):
    us="Creaed on 18 Sep 2021 and Modified on 13 April 2022. \n Creator : HNM"
    bot.send_message(message.chat.id,us)

@bot.message_handler(content_types=["text"])
def browse(message):
    text=message.text
    if text=="/inspire":
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " - " + json_data[0]['a']
        bot.send_message(message.chat.id,quote)
    else :
        meaning=getMeaning(text)
        user_data="{} {}({}) searched '{}'".format(message.from_user.first_name, message.from_user.last_name,message.from_user.username,text)
        bot.send_message(-1001680314281, user_data)
        bot.send_message(message.chat.id,meaning)


bot.polling()
