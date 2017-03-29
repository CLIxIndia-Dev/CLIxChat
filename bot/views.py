from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the bot index.")
#
# from django.core.context_processors import csrf
# from django.shortcuts import render_to_response
#
# def my_view(request):
#     c = {}
#     c.update(csrf(request))
#     # ... view code here
#     return render_to_response("a_template.html", c)



import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from clixchat.settings import TOKEN

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

"""
$ python2.7 flask_skeleton.py <token> <listening_port> <webhook_url>
Webhook path is '/abc', therefore:
<webhook_url>: https://<base>/abc
Webhook manual set command via curl:
curl -F "url=https://<YOURDOMAIN.EXAMPLE>/<WEBHOOKLOCATION>" https://api.telegram.org/bot<YOURTOKEN>/setWebhook
"""

links = {'course':'https://www.merriam-webster.com/dictionary/course',
	       'group':'https://www.merriam-webster.com/dictionary/group',
         'rick':'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
         'demox':'https://www.edx.org/course/demox-edx-demox-1',
         'joinchat':'https://t.me/joinchat/AAAAAEG40y2c6F1dyoQyDg'}

# later this function should access the database and grab
# the number of units in a given course.
# For now, this function just assumes the number of units is 5
def getNumUnits(course):
    return 5

def makeUnitKeyboard(course, numUnits):
    buttons = []
    for i in range(1,numUnits+1):
        button = [KeyboardButton(text=str(course) + " Unit " + str(i))]
        buttons.append(button)
    return ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True,)

# For now, this function assumes the number of sessions is the length of the string
def getNumSessions(course):
    return len(course)

def makeSessionsKeyboard(course, numSessions):
    buttons = []
    for i in range(1,numSessions+1):
        button = [KeyboardButton(text=str(course) + " Session " + str(i))]
        buttons.append(button)
    return ReplyKeyboardMarkup(keyboard=buttons, one_time_keyboard=True,)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat Message:', content_type, chat_type, chat_id)

    inline_links = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Architecture',
                                         url='https://www.edx.org/course/subject/architecture')],
                   [InlineKeyboardButton(text='Chemistry',
                                         url='https://www.edx.org/course/subject/chemistry')],
                   [InlineKeyboardButton(text='History',
                                         url='https://www.edx.org/course/subject/history')]
               ])

    if content_type == 'text' and msg['text'] in links.keys(): # if user enters key word
    	bot.sendMessage(chat_id, links[msg['text']])

    elif content_type == 'text' and msg['text'] == '/courses':
        bot.sendMessage(chat_id, 'Please select a course', reply_markup=inline_links)

    elif content_type == 'text' and msg['text'] == '/kbtest':
        bot.sendMessage(chat_id, 'testing custom keyboard',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Yes"), KeyboardButton(text="No")]]))
    elif content_type == 'text' and (msg['text'] == '/start'):
        bot.sendMessage(chat_id, 'Course Materials or FAQ?',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="Course Materials")],
                                      [KeyboardButton(text="FAQ")]],
                            one_time_keyboard=True))

    ### Course Materials ###

    elif content_type == 'text' and msg['text'] == 'Course Materials':
        print(chat_id)
        bot.sendMessage(chat_id,
                        'I am here to help you access course materials! What course are you taking?',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="ICT")],
                                      [KeyboardButton(text="English")],
                                      [KeyboardButton(text="Math")],
                                      [KeyboardButton(text="Science")]],
                            one_time_keyboard=True,))

    elif content_type == 'text' and (msg['text'] == 'ICT' or msg['text'] == 'English' or msg['text'] == 'Math' or msg['text'] == 'Science'):
        numUnits = getNumUnits(msg['text'])
        keyboard= makeUnitKeyboard(msg['text'], numUnits)
        bot.sendMessage(chat_id,
                        'Select your unit.',
                        reply_markup=keyboard)

    elif content_type == 'text' and ("Unit" in msg['text']):
        course = msg['text'].split(' ')[0] # get course name
        numSessions = getNumSessions(course)
        keyboard = makeSessionsKeyboard(course, numSessions)
        bot.sendMessage(chat_id,
                        'Select your session.',
                        reply_markup=keyboard)

    elif content_type == 'text' and ("Session 1" in msg['text']):
        bot.sendMessage(chat_id, 'To see that content you must log in to openedx on a computer.')

    # all other sessions for now have hardcoded activities
    elif content_type == 'text' and ("Session" in msg['text']):
        bot.sendMessage(chat_id,
                        'Select an activity.',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="Message text here!")],
                                      [KeyboardButton(text='Video: How edX Works')],
                                      [KeyboardButton(text="Activity4.pdf")],
                                      [KeyboardButton(text="CLIx Image")]],
                            ))

    elif content_type == 'text' and ("Video" in msg['text']):
        bot.sendMessage(chat_id, 'https://www.youtube.com/watch?v=B-EFayAA5_0')

    elif content_type == 'text' and ("pdf" in msg['text']):
        # Once we have a db, we could search through the db looking for
        # the pdf. However, sendDocument takes an a URL, so we might
        # have to look into other ways to deal with this.
        bot.sendDocument(chat_id, "https://courses.edx.org/c4x/LinuxFoundationX/LFS101x/asset/Introduction_to_Linux_Course_Outline.pdf")

    elif content_type == 'text' and ("Image" in msg['text']):
        bot.sendPhoto(chat_id, "http://clix.tiss.edu/dev/ver1.0/wp-content/uploads/2015/11/Clix-logo-600x1401.png")

    ### FAQ ###

    elif content_type == 'text' and (msg['text']=='FAQ'):
        bot.sendMessage(chat_id,
                        'Select a category.',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="Course FAQs")],
                                      [KeyboardButton(text="Discussion FAQs")]]
                            ))

    elif content_type == 'text' and (msg['text'].split(' ')[-1] == "FAQs"): # if the last word is FAQS
        cat =  msg['text'].split(' ')[0] # category of FAQs
        if cat == "Course":
            bot.sendMessage(chat_id,
                        'What is your question?',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="How many courses can I take?")],
                                      [KeyboardButton(text="How long is a course?")]]
                            ))
        elif cat == "Discussion":
            bot.sendMessage(chat_id,
                        'What is your question?',
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[KeyboardButton(text="How do I participate in discussions?")],
                                      [KeyboardButton(text="How are discussions graded?")]]
                            ))

    elif content_type == 'text' and msg['text'] == '/courses':
        bot.sendMessage(chat_id, 'Please select a course', reply_markup=inline_links)

    elif content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])

# def on_callback_query(msg):
#     query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
#     print('Callback query:', query_id, from_id, data)
#     bot.answerCallbackQuery(query_id, text='Got it')

# # need `/setinline`
# def on_inline_query(msg):
#     query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
#     print('Inline Query:', query_id, from_id, query_string)

#     # Compose your own answers
#     articles = [{'type': 'article',
#                     'id': 'abc', 'title': 'ABC', 'message_text': 'Good morning'}]

#     bot.answerInlineQuery(query_id, articles)

# # need `/setinlinefeedback`
# def on_chosen_inline_result(msg):
#     result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
#     print('Chosen Inline Result:', result_id, from_id, query_string)



# app = Flask(__name__)
bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.message_loop({'chat': on_chat_message #,
                  # 'callback_query': on_callback_query,
                  # 'inline_query': on_inline_query,
                  # 'chosen_inline_result': on_chosen_inline_result
                  }, source=update_queue)  # take updates from queue

def index(request):
    update_queue.put(request.data)  # pass update to bot
    return HttpResponse("Hello, world. You're at the bot index.")

# @app.route('/abc', methods=['GET', 'POST'])
# def pass_update():
#     update_queue.put(request.data)  # pass update to bot
#     return 'OK'
#
# if __name__ == '__main__':
#     bot.setWebhook(URL)
#     app.run(port=PORT, debug=True)

