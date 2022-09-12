import asyncio
import telegram
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import datetime as dt

# load env vars
load_dotenv()
TELEGRAM_BOT_API_KEY = os.environ["TELEGRAM_BOT_API_KEY"]
YOUR_CHAT_ID = os.environ["YOUR_CHAT_ID"]
TODAY = dt.date.today()

# reminder message prepare
def prepare_reminder_message(bdays_df):
    # messages list
    messages = []
    
    # loop over bdays df and append the message if the person has a bday today
    for i in range(bdays_df.shape[0]):
        if ~np.isnan(bdays_df.year[i]):
            messages.append(f"Today is {bdays_df.name[i]}'s birthday - They turn {TODAY.year - bdays_df.year[i]} today")
        else:
            messages.append(f"Today is {bdays_df.name[i]}'s birthday")

    # return the messages
    return '\n'.join(messages)

# bday checker
def check_bdays():
    # read data
    df = pd.read_csv("birthday_list.csv")

    # parse dates in the dataset
    df["date"] = [dt.date(TODAY.year,m,d) for m, d in zip(df["month"], df["day"])]

    # return who's bday is today
    return df[df["date"] == TODAY]

# main
async def main():
    # load bot to make requests
    bot = telegram.Bot(TELEGRAM_BOT_API_KEY)
    
    # get messages
    birthdays_message = prepare_reminder_message(check_bdays())

    async with bot:
        # send "bdays for today" message
        await bot.send_message(text=f"Birthdays for today: {TODAY}", chat_id=YOUR_CHAT_ID)

        # send birthdays message
        await bot.send_message(text=birthdays_message, chat_id=YOUR_CHAT_ID)

# run main
asyncio.run(main())
