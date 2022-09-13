#!/bin/bash

python3 -m venv ./bdaychecker
source ./bdaychecker/bin/activate
pip install -r requirements.txt
pip install python-telegram-bot -U --pre
echo -e "TELEGRAM_BOT_API_KEY=\"APIKEY\"\nYOUR_CHAT_ID=\"CHATID\"" > .env && rm .env.template
echo -e "name,year,month,day\n" > birthday_list.csv 
source ./bdaychecker/bin/activate
