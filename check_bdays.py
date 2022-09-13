import asyncio
import telegram
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import datetime as dt
import argparse
import json

# parse cli arguments
parser = argparse.ArgumentParser(description="Send reminder birthday messages to telegram chat id if there's a birthday", formatter_class=argparse.RawTextHelpFormatter)

# language flag
parser.add_argument('-l', '--language', type=str, default="en", help="Language to use for the bot as an ISO 3166-1 alpha-2\n language code. Default is 'en' (English), not case sensitive.\n If the code is not present in the keys of 'language.json'\n you can translate it yourself and (ideally) submit a PR 😁:\n https://github.com/dreth/BdayReminderBot.")

# parse arguments
args = parser.parse_args()

# use args
if args.language:
    # load languages
    with open('languages.json') as f:
        LANGUAGES = json.load(f)

    # check if lang exists, otherwise just use 'en'
    args.language = 'en' if args.language not in LANGUAGES.keys() else args.language
    
    # set messages' language
    sentence = [LANGUAGES[args.language.lower()][x] for x in range(3)]

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
            messages.append(sentence[0].format(bdays_df.name[i],int(TODAY.year - bdays_df.year[i])))
        else:
            messages.append(sentence[1].format(bdays_df.name[i]))

    # return the messages
    if messages:
        return sentence[2].format(TODAY) + '\n'.join(messages)
    else:
        return None

# generate date but validate
def date_with_validation(y,m,d):
    try: return dt.date(y,m,d)
    except: return None

# bday checker
def check_bdays():
    # read data
    df = pd.read_csv("birthday_list.csv")

    # only keep elements that have at least month and day
    df = df[df["month"].notna() & df["day"].notna()]

    # parse dates in the dataset
    df["date"] = [date_with_validation(TODAY.year,int(m),int(d)) for m, d in zip(df["month"], df["day"])]

    # return who's bday is today
    return df[df["date"] == TODAY]


# main
async def main():
    # load bot to make requests
    bot = telegram.Bot(TELEGRAM_BOT_API_KEY)
    
    # get messages
    birthdays_message = prepare_reminder_message(check_bdays())

    async with bot:
        # send birthdays message
        if birthdays_message:
            await bot.send_message(text=birthdays_message, chat_id=YOUR_CHAT_ID)

# run main
asyncio.run(main())
