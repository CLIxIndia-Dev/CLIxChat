from django.http import HttpResponse
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from clixchat.settings import TOKEN
from queue import Queue
from .models import Element, User, Interaction
import datetime
import re
#import pytz
# from django.shortcuts import get_object_or_404


"""
Webhook manually set command via curl:
curl -F "url=https://<YOURDOMAIN.EXAMPLE>/<WEBHOOKLOCATION>" https://api.telegram.org/bot<YOURTOKEN>/setWebhook
"""

links = {'course':'https://www.merriam-webster.com/dictionary/course',
	       'group':'https://www.merriam-webster.com/dictionary/group',
         'rick':'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
         'demox':'https://www.edx.org/course/demox-edx-demox-1',
         'joinchat':'https://t.me/joinchat/AAAAAEG40y2c6F1dyoQyDg'}

def makeUnitKeyboard(course, numUnits):
    buttons = []
    for i in range(1,numUnits+1):
        button = [KeyboardButton(text=str(course) + " Unit " + str(i))]
        buttons.append(button)
    return ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True,)

def makeSessionsKeyboard(course, numSessions):
    buttons = []
    for i in range(1,numSessions+1):
        button = [KeyboardButton(text=str(course) + " Session " + str(i))]
        buttons.append(button)
    return ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True,)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message: ', content_type, chat_type, chat_id)

    user = (User.objects.get_or_create(id=chat_id))[0]
    userID = msg['from']['id']
    current_time = datetime.datetime.now() # now() does not include timezone
    last = user.last_visit.replace(tzinfo=None) # set tzinfo to none so we can get difference
    hours = (current_time - last).seconds/3600
    seconds = (current_time - last).seconds
    buttons=[]
    chat_text = msg['text']
    msg_r = "" # message that user receives from bot


    # if content_type == 'text' and ( (msg['text'] == '/start') or (msg['text'] == 'Restart') or (seconds > 60) ):
    if content_type == 'text' and ( (msg['text'] == '/start') or (msg['text'] == 'Restart')):

        bot.sendDocument(chat_id, document = "http://web.mit.edu/bhanks/www/robot.gif")

        if (seconds > 60):
            bot.sendMessage(chat_id, "Welcome back!")

        element = Element.objects.get(pk=1) # not a great idea to search via pk, should prob use filter instead
        #children = element.get_children()
        #for x in children:
         #   if x.name is not None:
          #      buttons.append([KeyboardButton(text=x.name)])
        
        # check that the queryset is not empty
        if (Element.objects.filter(level=1)).exists():
            children = (Element.objects.filter(level=1))
            print("**children: ",children)
            for x in children:
                if x.name is not None:
                    print("**x.name: ",x.name)
                    buttons.append([KeyboardButton(text=x.name)])

        bot.sendMessage(chat_id, element.message_text,
                        reply_markup=ReplyKeyboardMarkup(
                                    keyboard=buttons))


    # not /start
    else:
        # print('user last node pk: ', user.last_node.pk)
        last_element = Element.objects.get(pk=user.last_node.pk)
        children = last_element.get_children()
        # print("children: ", children)
        # print("last element: ", last_element)
        found = False
        for x in children:
            # print('msg text: ', chat_text)
            # # print('pk: ', x.pk)
            print('**obj name: ', x.name)
            if x.name == chat_text:
                found = True
                # print('msg name: ', x.name)
                # print('pk: ', x.pk)
                element = Element.objects.get(pk=x.pk)
                # print('element: ', element)
                msg = element.message_text

                grandchildren = element.get_children()
                for x in grandchildren:
                    if x.name is not None:
                        buttons.append([KeyboardButton(text=x.name)])

                if len(buttons) == 0:
                    element = last_element
                    for x in children:
                        if x.name is not None:
                            #new line character doesn't work
                            #buttonName = x.name + '\n' + x.name
                            buttons.append([KeyboardButton(text=x.name)])


                buttons.append([KeyboardButton(text='Restart')])
                # print('buttons: ', buttons)

                msg = msg.split("~")
                msg_r = msg
                for x in msg:
                    if (".pdf" in x):
                        # regex adapted from http://www.regextester.com/20
                        result = re.search('((http[s]?):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.pdf)', x)
                        fileurl = result.group(0) # just the url
                        caption_txt = x.replace(fileurl, "")
                        bot.sendDocument(chat_id, document = fileurl,
                                         caption = caption_txt,
                                         reply_markup=ReplyKeyboardMarkup(
                                             keyboard=buttons))
                    elif (".mp3" in x):
                        result = re.search('((http[s]?):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.mp3)', x)
                        audiourl = result.group(0) # just the url
                        caption_txt = x.replace(audiourl, "")
                        bot.sendAudio(chat_id, audio = audiourl,
                                      caption = caption_txt,
                                      reply_markup=ReplyKeyboardMarkup(
                                             keyboard=buttons))
                    elif (".jpg" in x):
                        result = re.search('((http[s]?):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.jpg)', x)
                        picurl = result.group(0) # just the url
                        caption_txt = x.replace(picurl, "")
                        bot.sendPhoto(chat_id, photo = picurl,
                                      caption = caption_txt,
                                      reply_markup=ReplyKeyboardMarkup(
                                             keyboard=buttons))
                    elif (".png" in x):
                        result = re.search('((http[s]?):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.png)', x)
                        picurl = result.group(0) # just the url
                        caption_txt = x.replace(picurl, "")
                        bot.sendPhoto(chat_id, photo = picurl,
                                      caption = caption_txt,
                                      reply_markup=ReplyKeyboardMarkup(
                                             keyboard=buttons))

                    elif (".gif" in x):
                        result = re.search('((http[s]?):\/)?\/?([^:\/\s]+)((\/\w+)*\/)([\w\-\.]+[^#?\s]+)(.gif)', x)
                        picurl = result.group(0) # just the url
                        caption_txt = x.replace(picurl, "")
                        bot.sendDocument(chat_id, document = picurl,
                                      caption = caption_txt,
                                      reply_markup=ReplyKeyboardMarkup(
                                             keyboard=buttons))

                    else:
                        bot.sendMessage(chat_id, x,
                                    parse_mode='Markdown',
                            reply_markup=ReplyKeyboardMarkup(
                                        keyboard=buttons))
                    
        if not found:
            print("couldn't find chat text: ", chat_text)
            msg_r = "I'm sorry, I don't understand."
            bot.sendMessage(chat_id, "I'm sorry, I don't understand.",
                    reply_markup=ReplyKeyboardMarkup(
                                keyboard=[[KeyboardButton(text='Restart')]]))

    print("user, msg_s, msg_r, msg_pk, btns, start_time", user, chat_text, msg_r, chat_id, buttons, current_time)

    #interaction = Interaction(User = userID,
     #                         msg_s = chat_text,
     #                         msg_r = msg_r,
      #                        msg_pk = chat_id,
       #                       btns = buttons,
        #                      start_time = current_time
         #                     )
    #interaction.save()

    # print('element: ', element)    
    user.last_node=element
    user.save()

    # obj, created = AppSettings.objects.get_or_create(name='DEFAULT_LANG')
    # obj.value = request.POST.get('DEFAULT_LANG')
    # obj.save()



    # element = Element.objects.get(pk=3)
    # bot.sendMessage(chat_id, element.get_children())


    # # command = get_object_or_404(Command, command_text=msg['text'])
    # command = Command.objects.get(command_text=msg['text'])
    #
    # print('cmd:', command)
    # response = Response.objects.filter(command_id=command.id)
    # print('response:', response)
    # for x in response:
    #     print('resp:', x)
    #     bot.sendMessage(chat_id, x.response_text)

    #
    #
    # inline_links = InlineKeyboardMarkup(inline_keyboard=[
    #                [InlineKeyboardButton(text='Architecture',
    #                                      url='https://www.edx.org/course/subject/architecture')],
    #                [InlineKeyboardButton(text='Chemistry',
    #                                      url='https://www.edx.org/course/subject/chemistry')],
    #                [InlineKeyboardButton(text='History',
    #                                      url='https://www.edx.org/course/subject/history')]
    #            ])
    #
    # if content_type == 'text' and msg['text'] in links.keys(): # if user enters key word
    # 	bot.sendMessage(chat_id, links[msg['text']])
    #
    # elif content_type == 'text' and msg['text'] == '/courses':
    #     bot.sendMessage(chat_id, 'Please select a course', reply_markup=inline_links)
    #
    # elif content_type == 'text' and msg['text'] == '/kbtest':
    #     bot.sendMessage(chat_id, 'testing custom keyboard',
    #                         reply_markup=ReplyKeyboardMarkup(
    #                             keyboard=[
    #                                 [KeyboardButton(text="Yes"), KeyboardButton(text="No")]]))
    # elif content_type == 'text' and (msg['text'] == '/start'):
    #     bot.sendMessage(chat_id, 'Course Materials or FAQ?',
    #                     reply_markup=ReplyKeyboardMarkup(
    #                         keyboard=[[KeyboardButton(text="Course Materials")],
    #                                   [KeyboardButton(text="FAQ")]],
    #                         one_time_keyboard=True))
    #
    # ### Course Materials ###
    #
    # elif content_type == 'text' and msg['text'] == 'Course Materials':
    #     print(chat_id)
    #     bot.sendMessage(chat_id,
    #                     'I am here to help you access course materials! What course are you taking?',
    #                     reply_markup=ReplyKeyboardMarkup(
    #                         keyboard=[[KeyboardButton(text="ICT")],
    #                                   [KeyboardButton(text="English")],
    #                                   [KeyboardButton(text="Math")],
    #                                   [KeyboardButton(text="Science")]],
    #                         one_time_keyboard=True,))
    #
    # elif content_type == 'text' and (msg['text'] == 'ICT' or msg['text'] == 'English' or msg['text'] == 'Math' or msg['text'] == 'Science'):
    #     numUnits = getNumUnits(msg['text'])
    #     keyboard= makeUnitKeyboard(msg['text'], numUnits)
    #     bot.sendMessage(chat_id,
    #                     'Select your unit.',
    #                     reply_markup=keyboard)
    #
    # elif content_type == 'text' and ("Unit" in msg['text']):
    #     course = msg['text'].split(' ')[0] # get course name
    #     numSessions = getNumSessions(course)
    #     keyboard = makeSessionsKeyboard(course, numSessions)
    #     bot.sendMessage(chat_id,
    #                     'Select your session.',
    #                     reply_markup=keyboard)
    #
    # elif content_type == 'text' and ("Session 1" in msg['text']):
    #     bot.sendMessage(chat_id, 'To see that content you must log in to openedx on a computer.')
    #
    # # all other sessions for now have hardcoded activities
    # elif content_type == 'text' and ("Session" in msg['text']):
    #     bot.sendMessage(chat_id,
    #                     'Select an activity.',
    #                     reply_markup=ReplyKeyboardMarkup(
    #                         keyboard=[[KeyboardButton(text="Message text here!")],
    #                                   [KeyboardButton(text='Video: How edX Works')],
    #                                   [KeyboardButton(text="Activity4.pdf")],
    #                                   [KeyboardButton(text="CLIx Image")]],
    #                         ))
    #
    # elif content_type == 'text' and ("Video" in msg['text']):
    #     bot.sendMessage(chat_id, 'https://www.youtube.com/watch?v=B-EFayAA5_0')
    #
    # elif content_type == 'text' and ("pdf" in msg['text']):
    #     # Once we have a db, we could search through the db looking for
    #     # the pdf. However, sendDocument takes an a URL, so we might
    #     # have to look into other ways to deal with this.
    #     bot.sendDocument(chat_id, "https://courses.edx.org/c4x/LinuxFoundationX/LFS101x/asset/Introduction_to_Linux_Course_Outline.pdf")
    #
    # elif content_type == 'text' and ("Image" in msg['text']):
    #     bot.sendPhoto(chat_id, "http://clix.tiss.edu/dev/ver1.0/wp-content/uploads/2015/11/Clix-logo-600x1401.png")
    #
    # ### FAQ ###
    #
    # elif content_type == 'text' and (msg['text']=='FAQ'):
    #     bot.sendMessage(chat_id,
    #                     'Select a category.',
    #                     reply_markup=ReplyKeyboardMarkup(
    #                         keyboard=[[KeyboardButton(text="Course FAQs")],
    #                                   [KeyboardButton(text="Discussion FAQs")]]
    #                         ))
    #
    # elif content_type == 'text' and (msg['text'].split(' ')[-1] == "FAQs"): # if the last word is FAQS
    #     cat =  msg['text'].split(' ')[0] # category of FAQs
    #     if cat == "Course":
    #         bot.sendMessage(chat_id,
    #                     'What is your question?',
    #                     reply_markup=ReplyKeyboardMarkup(
    #                         keyboard=[[KeyboardButton(text="How many courses can I take?")],
    #                                   [KeyboardButton(text="How long is a course?")]]
    #                         ))
    #     elif cat == "Discussion":
    #         bot.sendMessage(chat_id,
    #                     'What is your question?',
    #                     reply_markup=ReplyKeyboardMarkup(
    #                         keyboard=[[KeyboardButton(text="How do I participate in discussions?")],
    #                                   [KeyboardButton(text="How are discussions graded?")]]
    #                         ))
    #
    # elif content_type == 'text' and msg['text'] == '/courses':
    #     bot.sendMessage(chat_id, 'Please select a course', reply_markup=inline_links)
    #
    # elif content_type == 'text':
    #     bot.sendMessage(chat_id, msg['text'])




bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.message_loop({'chat': on_chat_message #,
                  # 'callback_query': on_callback_query,
                  # 'inline_query': on_inline_query,
                  # 'chosen_inline_result': on_chosen_inline_result
                  }, source=update_queue)  # take updates from queue

def index(request):
    print('request post:', request.body)
    update_queue.put(request.body)  # pass update to bot
    return HttpResponse("Hello, world. You're at the bot index.")
