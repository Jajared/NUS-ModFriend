import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import NUSBot as nus
from Group import Group
from Student import Student
import Error as e

API_token = '5738711983:AAE5qf6nLnmzwwoNBpNiulG0q-WkGpnHvYQ'
allGroups = {}
admin_ID = "964015471"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#Send a message when the command /start is issued + Creates Group object
def start(update: Updater, context: CallbackContext):
    message = """Hi! Welcome to ModFriend, helping you to find a common free time with your friends! 
    \nPlease copy and paste your NUSMods timetable link!
    \nFor help, use /help"""
    update.message.reply_text(message)
    group_id = getGroupID(update)
    if group_id not in allGroups:
        createGroup(group_id)

#Send a message when the command /help is issued
def getHelp(update: Updater, context: CallbackContext):
    message = """Step 1: Go to www.nusmods.com/timetable
        \nStep 2: After entering all of your modules, click share/sync and copy and paste the given link onto the chat
        \nStep 3: Enter /show to view all of the available timings with your friends!
        \nFor any other queries, please PM @jajabonks"""
    update.message.reply_text(message)

#Updates user modlink when a valid NUSMod link is sent
def updateLink(update, context):
    logger.info(update)
    link = getMessage(update)
    group_id = getGroupID(update)
    studentID = getUserID(update)
    currentGroup = allGroups[group_id]
    if studentID in currentGroup.users:
        affectedStudent = currentGroup.users[studentID]
        if affectedStudent.getNextAction() == "edit":
            affectedStudent.changeLink(link)
            update.message.reply_text("Link changed!")
            affectedStudent.completeAction()
            currentGroup.recalculateFreeTime()
    else:
        update.message.reply_text("Link uploaded!")
        newStudent = Student(link, currentGroup, getUsername(update), studentID)
        currentGroup.add_user(newStudent)
        

#Send a message when the command /edit is issued
def editLink(update, context):
    update.message.reply_text("Please send your new NUSMod Link!")
    studentID = getUserID(update)
    group_id = getGroupID(update)
    if group_id in allGroups:
        currentGroup = allGroups[group_id]
        if studentID in currentGroup.users:
            affectedStudent = currentGroup.users[studentID]
            affectedStudent.addAction("edit")
    
#Handles errors
def errorHandler(update, context):
    logger.error(msg="Something went wrong", exc_info = context.error)
    message = str(context.error)
    #Sends error message to group/user
    context.bot.send_message(
    chat_id = getGroupID(update),
    text = message
    )

def getMessage(update):
    return update.message.text

def getUsername(update):
    return update.message.from_user.username

def getUserID(update):
    try:
        return update.message.from_user.id
    except:
        raise e.UserError

def getFreeTime(update, context):
    group_id = getGroupID(update)
    currentGroup = allGroups[group_id]
    context.bot.send_message(chat_id = update.effective_chat.id, text= currentGroup.showFreeTime())

def createGroup(group_id):
    newGroup = Group(group_id)
    allGroups[group_id] = newGroup
    return newGroup

def getGroupID(update):
    try:
        return update.message.chat.id
    except:
        raise e.GroupError

#Start the bot
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_token, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", getHelp))
    dp.add_handler(CommandHandler("show", getFreeTime))
    dp.add_handler(CommandHandler("edit", editLink))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.regex("^https:\/\/nusmods.com/timetable/sem-(1|2)/share?"), updateLink))
    # log all errors
    dp.add_error_handler(errorHandler)
    # Start the Bot
    updater.start_polling(drop_pending_updates=True)

    updater.idle()


if __name__ == '__main__':
    main()