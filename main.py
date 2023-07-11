import time

import telebot
import requests
from threading import Thread
from DB import WorkingWithDB

TOKEN = ""
bot = telebot.TeleBot(TOKEN)
NAMES = ['зимина арина', 'губанов георгий', 'тропицын максим', 'суховеркова алина', 'яруллин ильшат', 'глазов сергей',
         'тихонов михаил', 'тузов артем', 'циунель елизавета', 'бодин артем', 'сайфетдиарова адиля',
         'калиниченко владислав', 'мурзин иван', 'новиков евгений', 'прокопьев дмитрий', 'сабиров раиль',
         'маматов наиль', 'костикова полина', 'присягин эдуард', 'залялеева диля', 'арина петухова',
         'дресвянников тимофей', 'ахметжанов риналь', 'пантюхина станислава', 'александрова дарья', 'крайнов родион',
         'латыпов данияр', 'лобов глеб', 'сибгатуллина айсылу', 'сайдуллин дамир', 'грешнов кирилл', 'торшин егор',
         'бакаев сергей', 'валиуллов руслан', 'гизамов рамазан', 'савельев иван', 'шумский кирилл', 'купцов сергей',
         'яшин дмитрий', 'чумейко владислав', 'панов артем', 'андрущенко валерия', 'ксенофонтов вадим', 'магзянов аяз',
         'салахов тимур', 'ахметзянова ильвина', 'синятуллина карина', 'сороквашина юлия', 'парубчишин егор',
         'илья - линь нгуен', 'иванова жанна', 'аленичев дмитрий', 'берендеев андрей', 'алексеев илья', 'лазуткин егор',
         'щендригин олег', 'меньшиков никита', 'паскаль владимир', 'глебов егор', 'агапов егор', 'мартынычева ксения',
         'бардина анна', 'михайлов александр', 'волостнов даниэль', 'файзуллин салават', 'серова анна',
         'николаева дарья', 'елагина софия', 'белугин арсений', 'гладышев михаил', 'кузьмин николай', 'алексеев андрей',
         "синягина алена"]

wwb = WorkingWithDB()


@bot.message_handler(content_types=['text'])
def text_handler(message):
    userID = message.chat.id
    try:
        if message.text.lower() == "/start":
            data = wwb.checkRegister(userID)
            if not data:
                msg = bot.send_message(userID, text="***Hi! Enter data like this:***\n___Name Surname___",
                                       parse_mode="Markdown")
                bot.register_next_step_handler(msg, registerUser)
            else:
                bot.send_message(userID, text="It seems like you are already registered :)")
        elif message.text.lower() == "/pomogite":
            wwb.erase(userID)
            bot.send_message(userID, text="***Done***", parse_mode="MarkdownV2")
        elif message.text.lower() == "/get" and userID in [2120704934, 921203559, 831753249, 592651306, 1028893821]:
            res = wwb.getStatistics()
            ans = ''
            for i in res:
                ans += i[1].capitalize() + " " + i[2].capitalize() + " " + i[3] + "\n"
            bot.send_message(userID, text=ans)
    except Exception:
        bot.send_message(userID, text="It will ***not work*** :)", parse_mode="Markdown")


def registerUser(message):
    try:
        userID = message.chat.id
        if message.text.lower() != "/start":
            text = message.text.split()
            name = text[0].replace("ё", "е").replace("Ё", "е")
            surname = text[1].replace("ё", "е").replace("Ё", "е")
            surnameName = surname.lower() + " " + name.lower()
            nameSurname = name.lower() + " " + surname.lower()
            if nameSurname in NAMES or surnameName in NAMES:
                if nameSurname in NAMES:
                    name, surname = surname, name
                alias = message.from_user.username
                checkAlready = wwb.checkNameSurname(name, surname)
                if checkAlready is None:
                    check = wwb.register(userID, name, surname, "@" + alias)
                    if check:
                        link = wwb.getLink()[0]
                        bot.send_message(userID, "***Success!***", parse_mode="Markdown")
                        msg = bot.send_message(userID, link)
                        time.sleep(20)
                        bot.edit_message_text(chat_id=userID, message_id=msg.message_id,
                                              text="__If the problem has occurred,"
                                                   " please contact @AzakiMan__\n***Good luck on exams!***",
                                              parse_mode="Markdown")
                else:
                    bot.send_message(userID, text="It seems like you are already registered :)")
            else:
                msg = bot.send_message(userID, "***You are not allowed to do this. Please, try again later.***",
                                 parse_mode="Markdown")
                bot.register_next_step_handler(msg, registerUser)
        else:
            data = wwb.checkRegister(userID)
            if not data:
                msg = bot.send_message(userID, text="***Hi! Enter data like this:***\n___Name Surname___",
                                       parse_mode="Markdown")
                bot.register_next_step_handler(msg, registerUser)
            else:
                bot.send_message(userID, text="It seems like you are already registered :)")


    except Exception:
        msg = bot.send_message(userID, text="***Try again :)***", parse_mode="Markdown")
        bot.register_next_step_handler(msg, registerUser)


bot.polling()
