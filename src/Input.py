#
# [Harvey]
#
# Josh Nissenbaum 2017
# The plan was just to mess around and create a personal assistant similar to Jarvis from Iron Man
# and I was inspired by Mark Zuckerberg's AI bot for his house. Harvey can retrieve the weather, keep track
# of notes and information. Harvey will learn new trees, and new ways to reach certain commands. Harvey will
# store information about anything and retrieve it later (basic memory).
#
# There's no knowing really how far it will go
#


#
# Python Package Imports
#

import sys
import random
import datetime
from time import strftime, gmtime
import schedule

# The input is taken from the Facebook Messenger Bot Node.js app
#
# The app loop through the output from this script (each print or return called)
# The print's are returned and dealt with as an object

sender = sys.argv[1]
message = sys.argv[2].lower()
message_split = message.split()

phrase_tree = {
    'what': 'whatTree',
    'whats': 'whatTree',
    'when': 'whenTree',
    'why': 'whyTree',
    'where': 'whereTree',
    'how': 'howTree',
    'hows': 'howTree',
    'i': 'personalTree',
    "hey": 'greetingTree',
    "hello": 'greetingTree'
}

phrase_branch = {
    'whatTree': {
        'are you': ['answer_who'],
        'time is it': ['answer_time'],
        'day is it': ['answer_day'],
        'do i have on today': ['todo_list'],
        'the weather': ['weather_cmd'],
        'is the weather': ['weather_cmd'],
        'is the weather like': ['weather_cmd'],
        'happening in the world': ['news_cmd']
    },
    'howTree': {
        'are you': ['answer_small_talk_1'],
        'is the weather': ['weather_cmd'],
        'the weather': ['weather_cmd'],
        'the weather today': ['weather_cmd']
    },
    'personalTree': {
        'have to': 'takeParameter'
    },
    'greetingTree': {
        '': ['greeting']
    }
}

phrase_command = {
    'find': ['location'], 'weather': ['location']
}

responses = {
    'positiveResponses':
        ['Yes', 'Of course', 'No problem'],

    'questionResponses':
        ['Okay, are you sure?', 'Are you sure?', 'That doesn\'t seem right'],

    'replyResponses':
        ['Good as always, and you?', 'Good today, and yourself?'],

    'greetingResponses':
        ['Hello Josh!', 'How\'s it going, Josh?', 'How are you Josh?'],

    'unsureResponses':
        ['I don\'t understand, Josh', 'What do you mean?']
}

todos = []

response = ""


def main():
    if message_split[0] in phrase_tree:
        if phrase_tree[message_split[0]] in phrase_branch:
            response = branch_created(phrase_branch[phrase_tree[message_split[0]]])
        else:
            response = "I'm not sure, Josh. What are you referring to?"
    else:
        pass

    print(response)


def branch_created(tree):
    message_reset = message.split(message_split[0])[1].strip()
    if message_reset in tree:
        respond(tree[message_reset], message_reset)
    else:
        #message_reset = message_split[1::]
        speech_parameter = message.split(message_split[2])[1]
        message_reset = message.split(message_split[2])
        print(message_reset)


def respond(response_type, message_reset):
    if response_type[0] == "greeting":
        greeting_response()
    if response_type[0] == "answer_small_talk_1":
        reply_response()
    elif response_type[0] == "answer_time":
        print("It is %s." % strftime("%H:%M", gmtime()))
    elif response_type[0] == "answer_day":
        print("It is %s." % strftime("%A, the %d of %B", gmtime()))
    elif response_type[0] == "todo_list":
        for todo in todos:
            print(todo)
    elif response_type[0] == "todo_add":
        print(message_reset)
    elif response_type[0] == "weather_cmd":
        retrieve_weather()
    elif response_type[0] == "news_cmd":
        import newspaper
        cnn = newspaper.build('http://cnn.com')
        for article in cnn_paper.articles:
            print(article.url)

#
# Method definitions for generating a random response
#


def happy_response():
    print(responses['positiveResponses'][random.randrange(len(responses['positiveResponses']))])


def reply_response():
    print(responses['replyResponses'][random.randrange(len(responses['replyResponses']))])


def unsure_response():
    print(responses['unsureResponses'][random.randrange(len(responses['unsureResponses']))])


def greeting_response():
    print(responses['greetingResponses'][random.randrange(len(responses['greetingResponses']))])


#
# Method definitions for commands trigger by a users recognised input
#


def retrieve_weather():
    import forecastio
    api_key = "29ec2715eb098cd1fd63358928e8b7ba"
    lat = -28.016667
    lng = 153.400000
    time = datetime.datetime(2015, 2, 27, 6, 0, 0)
    forecast = forecastio.load_forecast(api_key, lat, lng, time=time)
    print(forecast.hourly().summary + " It is " + str(round(forecast.currently().temperature)) + " degrees outside.")



if __name__ == '__main__':
    sys.exit(main())
