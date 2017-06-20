from django.http import HttpResponse
# from django.utils import timezone
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from clixchat.settings import TOKEN
from queue import Queue
from .models import Element, User, Interaction
import datetime
import re
#import pytz
# from django.shortcuts import get_object_or_404
from telepot.loop import OrderedWebhook
import logging

"""
Webhook manually set command via curl:
curl -F "url=https://<YOURDOMAIN.EXAMPLE>/<WEBHOOKLOCATION>" https://api.telegram.org/bot<YOURTOKEN>/setWebhook
"""

links = {'course':'https://www.merriam-webster.com/dictionary/course',
	       'group':'https://www.merriam-webster.com/dictionary/group',
         'rick':'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
         'demox':'https://www.edx.org/course/demox-edx-demox-1',
         'joinchat':'https://t.me/joinchat/AAAAAEG40y2c6F1dyoQyDg'}

# Helper function for on_chat_message that
# gets the url and sends it accordingly
def geturl(ext, x, buttons, chat_id):
    # regex adapted from http://www.regextester.com/20
    result = re.search('((http[s]?):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(' + ext + ')', x)
    fileurl = result.group(0) # just the url
    caption_txt = x.replace(fileurl, "")
    
    if ext == ".pdf" or ext == ".gif":
        bot.sendDocument(chat_id, document = fileurl,
                         caption = caption_txt,
                         reply_markup=ReplyKeyboardMarkup(
                             keyboard=buttons))
    elif ext == ".mp3":
        bot.sendAudio(chat_id, audio = fileurl,
                      caption = caption_txt,
                      reply_markup=ReplyKeyboardMarkup(
                          keyboard=buttons))
    elif ext == ".jpg" or ext == ".png":
        bot.sendPhoto(chat_id, photo = fileurl,
                      caption = caption_txt,
                      reply_markup=ReplyKeyboardMarkup(
                          keyboard=buttons))
    return (result, fileurl, caption_txt)


def on_chat_message(msg):
    logger.info('on_chat_message called')
    # x = msg['chat']['id']
    logger.info(type(msg))
    logger.info(msg)
    msg = json.loads(msg)


    content_type, chat_type, chat_id = telepot.glance(msg)
    logger.info('Chat Message: ', content_type, chat_type, chat_id)

    user = (User.objects.get_or_create(id=chat_id))[0]
    userID = msg['from']['id']
    current_time = datetime.datetime.now() # now() does not include timezone
    # current_time = timezone.now()
    last = user.last_visit.replace(tzinfo=None) # set tzinfo to none so we can get difference
    hours = (current_time - last).seconds/3600
    seconds = (current_time - last).seconds
    buttons=[]
    chat_text = msg['text']
    msg_r = "" # message that user receives from bot
    button_list = []

    if content_type == 'text' and ( (chat_text == '/start') or (chat_text == 'Restart')):

        # Optional greeting graphic
        # bot.sendDocument(chat_id, document = "http://web.mit.edu/bhanks/www/robot.gif")
        if (seconds > 600):
            msg_r = "Welcome back!"
            bot.sendMessage(chat_id, "Welcome back!")
        msg_pk = 1
        # element = Element.objects.get(pk=1) # not a great idea to search via pk, should prob use filter instead
        top_level_elements = Element.objects.filter(level=0) # this is a string not an element object
        for x in top_level_elements:
            if str.lower(x.name) == "start":
                element = x

        
        # check that the queryset is not empty
        if (Element.objects.filter(level=1)).exists():
            children = (Element.objects.filter(level=1))
            print("children: ",children)
            for x in children:
                if x.name is not None:
                    button_list.append(x.name)
                    buttons.append([KeyboardButton(text=x.name)])
        #msg_r = "Welcome back! " + element.message_text
        message = Element.objects.filter(level=0).values("message_text")[0]["message_text"]
        msg_r = "Welcome back! " + message
        bot.sendMessage(chat_id,
                        message, # element.message_text
                        reply_markup=ReplyKeyboardMarkup(
                                    keyboard=buttons))

    elif chat_text == "Back":
        last_element = Element.objects.get(pk=user.last_node.pk)
        if last_element.is_root_node():
            parent = last_element
            children = last_element.get_children()
        else:
            parent = last_element.parent
            children = parent.get_children()
        msg_pk = user.last_node.pk
        print("buttons we want to display when we click back: ", children)
        found = True
        for x in children: 
           if x.name is not None:
               button_list.append(x.name)
               buttons.append([KeyboardButton(text=x.name)])

        if len(buttons) == 0:
            element = last_element
            for x in children:
                if x.name is not None:
                    button_list.append(x.name)
                    buttons.append([KeyboardButton(text=x.name)])
        if not parent.is_root_node():
            buttons.append([KeyboardButton(text='Back')])


        element = parent
        msg = parent.message_text
                
        bot.sendMessage(chat_id, msg,
                        parse_mode='Markdown',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=buttons))





    # not /start or back
    else:
        # print('user last node pk: ', user.last_node.pk)
        last_element = Element.objects.get(pk=user.last_node.pk)
        element = last_element
        msg_pk = user.last_node.pk
        print("last element: ", last_element)
        children = last_element.get_children()
        print("**regular buttons we want to display: ", children)
        found = False

        for x in children:
            if x.name == chat_text:
                found = True
                element = Element.objects.get(pk=x.pk)
                msg = element.message_text

                if msg.startswith("^"):
                    msg = msg[1:]
                    last_element = element

                grandchildren = element.get_children()
                for x in grandchildren:
                    if x.name is not None:
                        button_list.append(x.name)
                        buttons.append([KeyboardButton(text=x.name)])

                if len(buttons) == 0:
                    element = last_element
                    for x in children:
                        if x.name is not None:
                            #new line character doesn't work
                            #buttonName = x.name + '\n' + x.name
                            button_list.append(x.name)
                            buttons.append([KeyboardButton(text=x.name)])
                buttons.append([KeyboardButton(text='Back')])
                # print('buttons: ', buttons)
                    
                msg = msg.split("~")
                
                for x in msg:
                    msg_r = x
                    
                    if (".pdf" in x):
                        geturl(".pdf", x, buttons, chat_id)
                    elif (".mp3" in x):
                        geturl(".mp3", x, buttons, chat_id)                     
                    elif (".jpg" in x):
                        geturl(".jpg", x, buttons, chat_id)
                    elif (".png" in x):
                        geturl(".png", x, buttons, chat_id)                   
                    elif (".gif" in x):
                        geturl(".gif", x, buttons, chat_id)
                    else:
                        bot.sendMessage(chat_id, x,
                                    parse_mode='Markdown',
                            reply_markup=ReplyKeyboardMarkup(
                                        keyboard=buttons))


        if not found:

            print('last element name:',last_element.name)
            print('element name:',element.name)

            if last_element.message_text.startswith("^") or element.message_text.startswith("^"):
                msg_r = "Thank you for the feedback!"
            else:
                last_element = Element.objects.get(pk=user.last_node.pk)

                print("couldn't find chat text: ", chat_text)
                msg_r = "I'm sorry, I don't understand."
            # button_list = ["I'm sorry, I don't understand."]
            buttons.append([KeyboardButton(text='Back')])
            bot.sendMessage(chat_id, msg_r,
                    reply_markup=ReplyKeyboardMarkup(
                                keyboard=[[KeyboardButton(text='Back')]]))
            # else:
            #     if msg.startswith("^"):
            #         msg = msg[1:]
            #         print("carat found")
            #         last_element = element
            #
            # if last_element.message_text.startswith("^"):
            #     msg_r = "Thank you for your feedback. You can continue to message me to provide futher feedback, or click /start or Back to return."
            # else:


            #
            # if "^" in last_element.message_text:
            #     print("carat found")
                    # feedback = chat_text.split("^")[1] # get text after ^
                    # chat_text = feedback # save the message without the ^ in the database
                    # print("FEEDBACK: ",feedback)
                    # element = Element.objects.get(pk=user.last_node.pk)
                    # msg_pk = user.last_node.pk
                    # buttons.append([KeyboardButton(text='Restart')])
                    # button_list = ['Restart'] # this is for Interactions object
                    # msg_r = "Thank you for your feedback. You can enter another questions using the ^ character, or you can click Restart."
                    # bot.sendMessage(chat_id,
                    #                 msg_r,
                    #                 parse_mode='Markdown',
                    #                 reply_markup=ReplyKeyboardMarkup(
                    #                     keyboard=buttons))
        #
        #               feedback = chat_text.split("^")[1] # get text after ^
        # chat_text = feedback # save the message without the ^ in the database
        # print("FEEDBACK: ",feedback)
        # element = Element.objects.get(pk=user.last_node.pk)
        # msg_pk = user.last_node.pk
        # buttons.append([KeyboardButton(text='Restart')])
        # button_list = ['Restart'] # this is for Interactions object
        # msg_r = "Thank you for your feedback. You can enter another questions using the ^ character, or you can click Restart."
        # bot.sendMessage(chat_id,
        #                 msg_r,
        #                 parse_mode='Markdown',
        #                 reply_markup=ReplyKeyboardMarkup(
        #                     keyboard=buttons))
        #




    #print("user, msg_s, msg_r, msg_pk, button_list, start_time", userID, chat_text, msg_r, msg_pk, button_list, current_time)

    interaction = Interaction(user = user,
                              msg_s = chat_text,
                              msg_r = msg_r,
                              msg_pk = msg_pk,
                              btns = button_list,
                              start_time = current_time
    )
    interaction.save()

    # print('element: ', element)    
    user.last_node=element
    print('user last node save: ', element.name)
    user.save()

bot = telepot.Bot(TOKEN)
# update_queue = Queue()  # channel between `app` and `bot`
#
# bot.message_loop({'chat': on_chat_message #,
#                   # 'callback_query': on_callback_query,
#                   # 'inline_query': on_inline_query,
#                   # 'chosen_inline_result': on_chosen_inline_result
#                   }, source=update_queue)  # take updates from queue

webhook = OrderedWebhook(bot, {'chat': on_chat_message})
webhook.run_as_thread()
logger = logging.getLogger('bot')

import codecs



import json
def index(request):
    try:
        bod = request.body
        bod = bod.decode("utf-8")
        logger.info(bod)
        bod = json.loads(bod)

        logger.info('req')
        on_chat_message(bod)
        # webhook.feed(bod)
    except ValueError:
        logger.info('GET requested')

    # webhook.feed(request.body)
    return HttpResponse("Hello, world. You're at the bot index.")
