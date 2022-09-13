# Telegram Birthday reminder bot

birthday reminder bot to run as a simple cron job with a CSV file containing birthdays because i always forget birthdays

0. Create a telegram bot using @botfather and get your api key 

1. Create venv

```bash
python3 -m venv ./bdaychecker
```

2. Activate the new env

```bash
source ./bdaychecker/bin/activate
```

3. Install requirements

```bash
pip install -r requirements.txt
```

As well as the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library version v20.x:

```bash
pip install python-telegram-bot -U --pre
```

4. Add telegram API to the .env file, I provided a template, but this command will create a new one with the needed environment variables, just replace  `APIKEY` with your telegram bot API key and `CHATID` with your chat ID (this [thread](https://stackoverflow.com/questions/41664810/how-can-i-send-a-message-to-someone-with-my-telegram-bot-using-their-username) in stackoverflow details how you can get that)

```bash
echo -e "TELEGRAM_BOT_API_KEY=\"APIKEY\"\nYOUR_CHAT_ID=\"CHATID\"" > .env && rm .env.template
```

5. Create a csv file with your birthdays in the format shown below.

Example:

| **name** | **year** | **month** | **day** |
| --- | --- | --- | --- |
| Carlos | 1967 | 11  | 7   |
| Michael | 1983 | 3   | 2  |
| George | 1988 | 9   | 15  |

You can skip the year if you don't know it, but the **name**, **month** and **day** must be populated, otherwise that row will be skipped.

```bash
echo -e "name,year,month,day\n" > birthday_list.csv 
```

6. Add a cron job to run this once a day every day, when it runs, you should receive a message from the bot if there's a birthday

```bash
crontab -e
```

And add (change the 6 with whatever hour you want this to run at):

```bash
0 6 * * * /path/to/cloned/repo/bdaychecker/bin/python /path/to/cloned/repo/check_bdays.py
```

I added a bash script to the root of the repo (`initial_setup.sh`) which runs all commands before step 6, you can run this script with `source initial_setup.sh` or `. initial_setup.sh` in bash.
