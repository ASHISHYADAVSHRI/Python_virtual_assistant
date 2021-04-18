from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import time
import speech_recognition as sr
# import playsound # you can use google playsound module to speak your assistant  to you but i am using pyttsx3 choose as you wish !
# from gtts import gTTS
import pyttsx3
import pytz
import subprocess
import re 
from bs4 import BeautifulSoup as soup 
import wikipedia
import random
import urllib3
from urllib.request import urlopen
import json
from time import strftime
import sys
import re 
import webbrowser
import smtplib
import requests 
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import socket



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "February", "March", "April", "May", "Jun", "July", "August", "September", "October", "November","December"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAY_EXTENTIONS = ['rd', "th", "st", "nd"]



def said(write):
    engine = pyttsx3.init()
    engine.say(write)
    engine.runAndWait()



#this function for recognize our voice
def g_audio():
    s_r = sr.Recognizer()
    with sr.Microphone() as source:
    	au = s_r.listen(source)
    	told = ''

    	try:
    		told = s_r.recognize_google(au)
    		print(told)
    	except Exception as e:
    		print("Exception: " + str(e))


    return told.lower()


#function for getting voice from the user
def google_calender():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
   
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_992583032381-0bokbpnlfhq3tlfrumr10art8fv71292.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service



def events(day, service):
    # Call the Calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print(f'Getting the upcoming {a} events')
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    e_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    e_date = e_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=e_date.isoformat(),
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    else:
        said(f"you have {len(events)} events on this day")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            s_time = str(start.split("T")[1].split("+")[0])
            if int(s_time.split(":")[0]) < 12:
                s_time = s_time + "am"
            else:
                s_time = str(int(s_time.split(":")[0])-12) + s_time.split(":")[1]
                s_time = s_time + "pm"

            said(event["summary"] + "at" + s_time)

def date(write):
    write = write.lower()
    today = datetime.date.today()

    if write.count("today") > 0:
        return today
    day = -1
    week = -1
    month = -1
    year = today.year


    for text in write.split():
        if text in MONTHS:
            month = MONTHS.index(text) + 1
        elif text in DAYS:
            week = DAYS.index(text)
        elif text.isdigit():
            day = int(text)
        else:
            for ext in DAY_EXTENTIONS:
                fon = text.find(ext)
                if fon > 0:
                    try:
                        day = int(word[:fon])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    '''if month == -1 and day != -1:# this statement take more time to run then the next one of it
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month''' 

    if day < today.day and month == -1 and day != -1:#you can use either this statement or the commented one, that statement run faster then the one above it! 
        month = month + 1

    if month == -1 and day == -1 and week != -1:
        present_week = today.weekday()
        diff = week - present_week

        if diff < 0:
            diff += 7
            if write.count("next") >= 1:
                diff += 7

        return today + datetime.timedelta(diff)

        if day != -1:
            return datetime.date(month=month, day=day, year=year)


#function for make note
def note_pad(write):
    date = datetime.datetime.now()
    f_name = str(date).replace(":", "-") + ".note-txt"
    with open(f_name, "w") as f:
        f.write(write)

    subprocess.Popen(['notepad.exe', f_name])



wake = "tom"
#this loop is all about date, time, month, year!
S = google_calender()
while True:
    said("hey, say tom to activted me!")
    print("say tom")
    write = g_audio()
       
    if write.count(wake) > 0:
        said("hey i am up")
        write = g_audio()


        #this loop is for open reddit
        li_st = ["reddit", "open"]
        for l in li_st:
            if "reddit" in write.lower():
                reg_ex = re.search('open reddit(.*)', write)
                url = 'https://www.redditinc.com/'
                if reg_ex:
                    subreddit = reg_ex.group(1)
                    url = url + 'r/' + subreddit
                webbrowser.open(url)
                said("the reddit web has opend for you sir")
                break

            elif "open" in write.lower():
                reg_ex = re.search("open(.+)", write)
                if reg_ex:
                    domain = reg_ex.group(1)
                    print(domain)
                    url1 = 'https://www.' + domain
                    webbrowser.open(url1)
                    said(f"the{domain}, has opend for you sir")
                    break
                else:
                    pass



        # this loop is for sending email
        # hint: your google account can show error so you can use other account e.g. Yahoo, outlook etc !
        em = ['email']    
        for Gmail in em:
            if Gmail in write.lower(): 
                said("who is the recipient sir?")
                recipient = g_audio()
                emails = 'yyxx@gmail.com' #provide your email with your variables or list
                for gmail in email:
                    if ashish or shri in gmail:
                        said("What whould you want to me to send sir")
                        content = g_audio()
                        socket.getaddrinfo('localhost', 8080)
                        mail = smtplib.SMTP("smtp.gmail.com", 587)
                        mail.ehlo()
                        mail.starttls()
                        username = 'xxx@gmail.com' #write your email, which email you wanna use to sent a message to another email
                        possword = '12345689' # provide that email password
                        mail.login(username, possword)
                        sender_email = "xxx@gmail.com"# provide email that you give to your username variable or just write down your variable
                        reciver_email = "yyy@gmail.com"# give email, name which email you are targeting to send message
                        mail.sendmail(sender_email, reciver_email, content)# sender_email, reciver_email were string here and it didn't work out for me so i made variables, you can use string or variables and check what is working for you !
                        mail.close()
                        said("email has been set successfuly, you can cheak your inbox sir")
                        break
                    else:
                        said("i don\'t know what do you mean")
                        break # actually it's looping so you need to break mathod after every loop

                            
        

        #this loop is for knowing your schedule
        calen = ["do i have a plans", "which events on"]
        for phrase in calen:
            if phrase in write.lower():
                date_var = date(write)
                if date_var:
                    events(date_var, S)
                else:
                    said("i don't understand")


        #this loop is for making note in our syestem
        Note = ['make a note', 'write it down']
        for phrase in Note:
            if phrase in write.lower():
                said("what are we gonna write about")
                note = g_audio().lower()
                note_pad(note)
                said("i've made note of that")

        