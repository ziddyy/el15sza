#**************Libraries********************#
import telegram

#******************SETUP********************#

bot = telegram.Bot(token="554215316:AAEEyHNk8JhLgLW1JYko9KdMSNkD98jDYvQ") #Private token key to connect to the bot


#******************MAIN********************#
updates=[] 
while not updates:
    updates=bot.getUpdates()             #Waiting for the incoming message

print updates[-1].message.text  
chat_id=updates[-1].message.chat_id      #Identification for the active chat
bot.sendMessage(chat_id=chat_id, text="Success!")
