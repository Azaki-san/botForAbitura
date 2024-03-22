import time

import telebot
from DB import WorkingWithDB
from transliterate import translit

TOKEN = "6079864933:AAETye-fcdft-JebcdOhrat5Dly5jzUveJg"
bot = telebot.TeleBot(TOKEN)
wwb = WorkingWithDB()
registeredIds = [x[0] for x in wwb.getRegisteredIds()]
registerInProgress = []
NAMES = [[x[0], x[1]] for x in wwb.getAllNamesOnSelection()]
print(NAMES)
link = wwb.getLink()[0]


@bot.message_handler(content_types=["text"])
def text_handler(message):
    global registeredIds
    userID = message.chat.id
    if message.text.lower() == '/add_selection' and userID in [2120704934, 921203559, 831753249, 592651306, 1028893821]:
        msg = bot.send_message(userID, "*Ok\. Send me surnames and names\.*", parse_mode="MarkdownV2")
        bot.register_next_step_handler(msg, addSelection)
        return
    elif message.text.lower() == '/get_selection' and userID in [2120704934, 921203559, 831753249, 592651306,
                                                                 1028893821]:
        msg = 'List:\n'
        for i in NAMES:
            msg += f'{i[0]} {i[1]}\n'
        bot.send_message(userID, msg)
    elif message.text.lower() == '/add_name' and userID in [2120704934, 921203559, 831753249, 592651306, 1028893821]:
        msg = bot.send_message(userID, "*Enter surname and name\.*", parse_mode="MarkdownV2")
        bot.register_next_step_handler(msg, addName)
        return
    elif message.text.lower() == "/get" and userID in [2120704934, 921203559, 831753249, 592651306, 1028893821]:
        res = wwb.getStatistics()
        ans = ''
        for j in range(len(res)):
            i = res[j]
            name, surname, alias = i[1].capitalize(), i[2].capitalize(), i[3]
            final_list = [name, surname, alias]

            for r in range(3):
                for k in ['_', '*', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
                    tempp = final_list[r]
                    tempp = tempp.replace(k, f'\{k}')
                    final_list[r] = tempp
            ans += f"*{j + 1}\)* " + "_" + final_list[0] + " " + final_list[1] + " " + "@" + final_list[2] + "\n" + "_"

        if ans == '':
            ans = "There are no registrations yet\."
        bot.send_message(userID, text=ans, parse_mode="MarkdownV2")
    elif message.text.lower() == "/get_not" and userID in [2120704934, 921203559, 831753249, 592651306, 1028893821]:
        ans = ''
        res = wwb.getStatistics()
        namess = []
        for i in res:
            namess.append([i[1], i[2]])
        count = 1
        for j in range(0, len(NAMES), 2):
            flag = 0
            i = NAMES[j]
            for q in namess:
                if i == q or NAMES[j + 1] == q:
                    flag = 1
                    break
            if flag == 0:
                ans += f"*{count}\)* " + "_" + i[0].capitalize() + " " + i[1].capitalize() + "\n" + "_"
                count += 1
        if ans == '':
            ans = "Everybody is registered\."
        bot.send_message(userID, text=ans, parse_mode="MarkdownV2")
    elif message.text.lower() == "/pomogite":
        print(f'{userID} used /pomogite.')
        wwb.erase(userID)
        bot.send_message(userID, text="*Done*", parse_mode="MarkdownV2")
        registeredIds = [x[0] for x in wwb.getRegisteredIds()]
    elif userID in registeredIds:
        print(f'{userID} tried to register one more time.')
        bot.send_message(userID, "*It seems like you already registered :\)*", parse_mode="MarkdownV2")
    elif userID not in registerInProgress:
        registerInProgress.append(userID)
        msg = bot.send_message(userID, text="*Hi\! Enter data like this:*\n_Name Surname_",
                               parse_mode="MarkdownV2")
        bot.register_next_step_handler(msg, registerUser)
        return


def addSelection(message):
    global NAMES
    ADD_NAMES = []
    userID = message.chat.id
    names = message.text.split("\n")
    for i in names:
        i = i.replace('ё', 'е')
        i = i.replace('Ё', 'e')
        i = i.lower()
        surname, name = i.split()
        ADD_NAMES.append([name, surname])
        ADD_NAMES.append([translit(name, 'ru', reversed=True), translit(surname, 'ru', reversed=True)])
    wwb.addSelectionNames(ADD_NAMES)
    NAMES = [[x[0], x[1]] for x in wwb.getAllNamesOnSelection()]
    bot.send_message(userID, "Success!")


def addName(message):
    global NAMES
    userID = message.chat.id
    a = message.text.lower()
    a = a.replace('ё', 'е')
    a = a.replace('Ё', 'e')
    surname, name = a.split()
    wwb.addSelectionNames(
        [[name, surname], [translit(name, 'ru', reversed=True), translit(surname, 'ru', reversed=True)]])
    NAMES = [[x[0], x[1]] for x in wwb.getAllNamesOnSelection()]
    bot.send_message(userID, "Success!")


def getVariousNames(text):
    text = text.replace('ё', 'е')
    text = text.replace('Ё', 'e')
    name, surname = text.split()
    return [[name.lower(), surname.lower()], [surname.lower(), name.lower()]]


def registerUser(message):
    if message.text == "/start":
        try:
            registerInProgress.remove(message.chat.id)
        except Exception:
            pass
        bot.send_message(message.chat.id, 'Back to main...')
        return 0
    userID = message.chat.id
    try:
        alias = ''
        names = getVariousNames(message.text)
        smart = None
        for i in range(len(names)):
            if names[i] in NAMES:
                if i == 0:
                    smart = True
                elif i == 1:
                    smart = False
        if smart is None:
            bot.send_message(userID, "*You are not allowed to do this\. Please, try again later\.*",
                             parse_mode="MarkdownV2")
            msg = bot.send_message(userID, text="*Enter data like this:*\n_Name Surname_",
                                   parse_mode="MarkdownV2")
            bot.register_next_step_handler(msg, registerUser)
            return
        else:
            try:
                alias = message.from_user.username
            except Exception:
                msg = bot.send_message(userID, "Oops, you don\'t have alias\. Please, add it in settings\.")
                bot.register_next_step_handler(msg, registerUser)
                return

            name, surname = '', ''
            if smart:
                name, surname = names[0][0], names[0][1]
            elif not smart:
                name, surname = names[1][0], names[1][1]
            checkAlreadyRegistered = wwb.checkNameSurname(name, surname)
            if checkAlreadyRegistered is None:
                isSuccessful = wwb.register(userID, name, surname, alias)
                if isSuccessful:
                    bot.send_message(userID, "*Success\!*", parse_mode="MarkdownV2")
                    msg = bot.send_message(userID, link)
                    time.sleep(20)
                    bot.edit_message_text(chat_id=userID, message_id=msg.message_id,
                                          text="_If the problem has occurred,"
                                               " please contact @AzakiMan_\n*Good luck on exams\!*",
                                          parse_mode="MarkdownV2")
            else:
                bot.send_message(userID, text="*It seems like you are already registered :\)*", parse_mode="MarkdownV2")

        registerInProgress.remove(userID)
    except Exception:
        bot.send_message(userID, text="*Incorrect name or surname\. Try again*",
                         parse_mode="MarkdownV2")
        bot.register_next_step_handler(message, registerUser)
        return


bot.polling()