from datetime import date, datetime, timedelta, time
import datetime
from django.utils import timezone
from django.core.mail import send_mail
import re

# check email function


def checkEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        return 'valid'

    else:
        return 'invalid'






def workDayFunction(dayOfWeek):
    timeList = []
    t1 = datetime.datetime.strptime('07:30', '%H:%M')
    if dayOfWeek in [d for d in range(5)]:
        for i in range(24):
            t1 = t1 + timedelta(minutes=30)
            timeList.append(datetime.datetime.strftime(t1, '%H:%M'))
        return timeList
    elif dayOfWeek == 5:
        for k in range(10):
            t1 = t1 + timedelta(minutes=30)
            timeList.append(datetime.datetime.strftime(t1, '%H:%M'))
        return timeList

def checkTime(time):
    t = time
    t1 = datetime.datetime.strftime(t, '%M')
    return str(t1)


t1 = datetime.datetime.strptime('07:30', '%H:%M')
k = datetime.datetime.now()
checkTime(k)



def createTime(dateCallback):
    time = datetime.datetime.strftime(dateCallback, '%H:%M')
    return time

def timeNow():
    t1 = datetime.datetime.now().date()
    if t1.weekday() == 6:
        t2 = datetime.datetime.now().date() + timedelta(days=1)
        return t2.weekday()
    else:
        return t1.weekday()

def nextDayTerm():
    listNext = []
    for i in range(1, 91):

        dateNext = datetime.datetime.now().date()
        day = dateNext.weekday()
        if day != 6:
            listNext.append(dateNext)
    return listNext

def nextDayTerm2():
    listNext = []
    for i in range(1, 91):

        dateNext = datetime.datetime.now().date() + timedelta(days=i)
        day = dateNext.weekday()
        if day != 6:
            listNext.append(dateNext)
    return listNext

def returnNextDay():
    t1 = datetime.datetime.now().date() + timedelta(days=1)
    if t1.weekday() == 6:
        t2 = datetime.datetime.now().date() + timedelta(days=2)
        return t2.weekday()
    else:
        return t1.weekday()

def dateExistFunction(date):
    if date:
        return date.weekday()

def capitalizeNamesFunc(name, lastName):
    name.lower()
    name.title()
    lastName.lower()
    lastName.title()
    return name, lastName

if '00' not in ['33', '58']:
    print('jeste')
