from typing import Text
import telebot
from dotenv import load_dotenv
import os 
import requests
from bs4 import BeautifulSoup

load_dotenv()
api=os.getenv("API")
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
    text="Welcom to Eng-MM Dictionary Bot.\n Here are the command\n/search word \n/about"
    bot.send_message(message.chat.id,text)
    print(message.chat.id)

@bot.message_handler(commands=["search"])
def search(message):
    text = message.text
    text = text.replace("/search ","")
    print(text)
    meaning=getMeaning(text)
    bot.send_message(message.chat.id,meaning)
    

@bot.message_handler(func=lambda message: True)
def forward(message):
    data = "From {} {}".format(message.from_user.first_name, message.from_user.last_name)
    bot.forward_message(-510713803, message.chat.id, message.message_id)
    bot.send_message(-510713803, data)



bot.polling()
