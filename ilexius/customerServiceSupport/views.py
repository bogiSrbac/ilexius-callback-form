from django.shortcuts import render
from .models import Customer, Archive
from .forms import CreateCusomerForm, AddCommentForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from datetime import datetime, date
import datetime
from django.utils import timezone
from django.views.generic import ListView, UpdateView, DetailView
import re
from django.core import serializers
import phonenumbers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from django.core.validators import validate_email
from.additional_functions import workDayFunction, createTime, timeNow, nextDayTerm, checkTime, capitalizeNamesFunc, nextDayTerm2, checkEmail


def index(request):
    context ={
    }
    return render(request, 'customerServiceSupport/index.html', context)

# customerCallbackForm
def createCustomerView(request):
    formCustomer = CreateCusomerForm(request.POST or None)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        if formCustomer.is_valid():
            dateTimeSave = formCustomer.save(commit=False)

            # covert to first letter uppercase

            capitalizeNamesFunc(dateTimeSave.last_name, dateTimeSave.first_name)
            dateTimeSave.email.lower()

            # if time is not in 30 minutes steps
            if dateTimeSave.date_and_time_for_callback != None:
                listOfsteps = ['30', '00']
                if checkTime(dateTimeSave.date_and_time_for_callback) not in listOfsteps:
                    return JsonResponse({'steps': 'Please, choose proper time from calendar.'})



            # if statement to chack if term is booked
            if dateTimeSave.date_and_time_for_callback != None:
                if dateTimeSave.date_and_time_for_callback < timezone.now():
                    return JsonResponse({'error': 'Requested date is less than current time. Please choose another date.'})
            if Customer.objects.filter(date_and_time_for_callback=dateTimeSave.date_and_time_for_callback, date_and_time_for_callback__isnull=False):
                return JsonResponse({'error': 'That term is reservd.'})
            # elif to chach does customer have alredy rezerved term
            elif Customer.objects.filter(first_name__iexact=dateTimeSave.first_name, last_name__iexact=dateTimeSave.last_name, email=dateTimeSave.email, first_name__isnull=False):
                name = Customer.objects.filter(first_name__iexact=dateTimeSave.first_name, last_name__iexact=dateTimeSave.last_name, email=dateTimeSave.email, first_name__isnull=False)


                for firstName in name:
                    date = firstName.date_and_time_for_callback.strftime('%d-%m-%Y')
                    time = firstName.date_and_time_for_callback.strftime('%H:%M')
                    name = firstName.first_name.lower()
                    last = firstName.last_name.lower()
                    message = f'You are already reserved term. </br>{name.title()} {last.title()} has callback term on {date} at {time}'
                    return  JsonResponse({'message':message})

            else:
                # if customer left datetime field blank with automatically give first not reserved term by system
                if dateTimeSave.date_and_time_for_callback == None:
                    defaultTerm = Customer.objects.filter(date_and_time_for_callback__year=datetime.datetime.now().year, date_and_time_for_callback__month=datetime.datetime.now(tz=timezone.utc).month,
                                                          date_and_time_for_callback__day=datetime.datetime.now().day,)
                    listBooked = []
                    listFreeTerms = []
                    for day in defaultTerm:
                        listBooked.append(createTime(day.date_and_time_for_callback))
                    dayOfWeek = datetime.datetime.now(tz=timezone.utc).weekday()

                    for i in workDayFunction(timeNow()):
                        if i not in listBooked:
                            if datetime.datetime.strptime(i, '%H:%M').time() > datetime.datetime.now().time() and datetime.datetime.now().time() < datetime.datetime.strptime(i, '%H:%M').time() and datetime.datetime.now(tz=timezone.utc).weekday() != 6:
                                listFreeTerms.append(i)
                                addCallbackTime = datetime.datetime.combine(
                                    datetime.datetime.now(tz=timezone.utc).date(),
                                    datetime.datetime.strptime(listFreeTerms[0], '%H:%M').time())
                                dateTimeSave.date_and_time_for_callback = addCallbackTime
                            else:
                                for data in nextDayTerm():
                                    defaultTerm1 = Customer.objects.filter(
                                        date_and_time_for_callback__year=data.year,
                                        date_and_time_for_callback__month=data.month,
                                        date_and_time_for_callback__day=data.day, )
                                    listBooked1 = []
                                    listFreeTerms1 = []
                                    listDate = []
                                    for day in defaultTerm1:
                                        listBooked1.append(createTime(day.date_and_time_for_callback))
                                        listDate.append(day.date_and_time_for_callback)
                                    t = data.weekday()
                                    for j in workDayFunction(t):
                                        if j not in listBooked1:
                                            listFreeTerms1.append(j)
                                    if len(listFreeTerms1) > 0:
                                        addCallbackTime1 = datetime.datetime.combine(
                                            data,
                                            datetime.datetime.strptime(listFreeTerms1[0], '%H:%M').time())
                                        dateTimeSave.date_and_time_for_callback = addCallbackTime1
                                        break

                                    else:
                                        pass
                yourDate = dateTimeSave.date_and_time_for_callback
                date = yourDate.strftime('%d-%m-%Y')
                time = yourDate.strftime('%H:%M')
                submitDate = datetime.datetime.now()
                dateTimeSave.submit_date_and_time = submitDate
                dateTimeSave.save()


                messageToCustomer = f'Dear {dateTimeSave.first_name} {dateTimeSave.last_name}. We recived your request for callback term which is on {date} at {time}!'
                send_mail(dateTimeSave.subject, messageToCustomer, dateTimeSave.email, [dateTimeSave.email], fail_silently=False)

                return JsonResponse({'success': f'You submit callback successfully! <br> Your term is on {date} at {time}! <br> You will recive an email with term data.'})

        else:
            # if email is in proper format regex check
            email = request.POST.get('email')
            if checkEmail(str(email)) != 'valid':
                return JsonResponse({'email': 'Please, insert valid email address.'})
            # if phone number in proper format
            phone_number = request.POST.get('phone_number')
            phoneNum = phonenumbers.parse(phone_number, 'SR')
            if not phonenumbers.is_valid_number(phoneNum):
                return JsonResponse({'phone': 'Please, insert valid phone number format for Serbia.'})


            return JsonResponse({'failure': 'Your message was not submitted!'})

    else:
        formCustomer = CreateCusomerForm()
    return render(request, 'customerServiceSupport/customerServiceSupport.html', {'formCustomer': formCustomer})

# check for free terms by calendar function
def checkFreeTermsFunction(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        dateCheck = request.POST.get('checkFreeTerms')
        date = datetime.datetime.strptime(dateCheck, '%Y-%m-%d')
        if date < timezone.now():
            return JsonResponse({'error': 'Requested date is less than current time. Please choose another date.'})
        dateDict = Customer.objects.select_related('customer')
        data = Customer.objects.filter(date_and_time_for_callback__year=date.year, date_and_time_for_callback__month=date.month,
                                               date_and_time_for_callback__day=date.day)
        dictOfTerms = {}
        listOfDate = []
        listOfTerms = []
        listOfFreeTerms = []
        for d in data:
            listOfDate.append(d.date_and_time_for_callback)
            listOfTerms.append(createTime(d.date_and_time_for_callback))

        t = date.weekday()
        for j in workDayFunction(t):
            if j not in listOfTerms:
                listOfFreeTerms.append(j)
        for j in range(len(listOfFreeTerms)):
            dictOfTerms[f'terms_{j}'] = listOfFreeTerms[j]
        keys = [dateCheck]
        values = [dictOfTerms]
        dictOfDates = dict(zip(keys, values))
        return JsonResponse({'dates': dictOfDates})

    return JsonResponse({})

# Free terms in next 10 days
def tenDaysFunction(request):
    counter = 0
    counter1 = 0
    listBooked1 = []

    listDate = []
    dictOfTerms = {}
    dictOfFreeTerms = {}
    dictList = []
    for data in nextDayTerm2():
        listFreeTerms1 = []
        defaultTerm1 = Customer.objects.filter(
            date_and_time_for_callback__year=data.year,
            date_and_time_for_callback__month=data.month,
            date_and_time_for_callback__day=data.day, )
        for day in defaultTerm1:
            listBooked1.append(createTime(day.date_and_time_for_callback))
        listDate.append(data)
        t = data.weekday()
        for j in workDayFunction(t):
            if j not in listBooked1:
                listFreeTerms1.append(j)
        dictList.append(f'dictOfTerms_{counter}')
        dictList[-1] = {}
        for j in range(len(listFreeTerms1)):
            dictList[-1][f'terms_{counter1}'] = listFreeTerms1[j]
            counter1 = counter1 + 1

        dictOfFreeTerms[f'{data}'] = dictList[-1]

        counter = counter + 1
        dictOfTerms.clear()
        listBooked1 = []

        if counter == 10:
            break
    return JsonResponse({'dataTenDays': dictOfFreeTerms})

# admin section
class CustomerCallbackList(ListView, LoginRequiredMixin):
    model = Customer
    template_name = 'customerServiceSupport/customerServiceSupport_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CustomerCallbackList, self).get_context_data(**kwargs)
        datum = Customer.objects.all().filter(date_and_time_for_callback__isnull=False, realized=False).order_by('date_and_time_for_callback')
        listOfdates = []
        for d in datum:
            t = d.date_and_time_for_callback
            t1 = t.date()
            if t1 not in listOfdates:
                listOfdates.append(t1)
        listOfHeadingId = []
        collapseId = []
        for i in range(len(listOfdates)):
            id = f'header_{i}'
            id1 = f'collapse_{i}'
            listOfHeadingId.append(id)
            collapseId.append(id1)
        context['dates'] = listOfdates
        context['headersId'] = listOfHeadingId
        context['collapseId'] = collapseId
        context['form'] = AddCommentForm()
        return context

# get list of customer information in admin panel
@login_required
def getCustomerInformation(request, pk):
    customer = Customer.objects.values().get(id=pk)
    user = str(request.user.username)
    customer['admin'] = user
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {
            'customer':customer
        }
        return JsonResponse(context)

# update comment and archive customer callback
@login_required
def updateComment(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        comment = request.POST.get('comment')
        realized = request.POST.get('realized')
        if realized == 'true':
            customer.realized = True
            customer.save()
        admin = request.user
        customer.comment = comment

        customer.administrator = str(admin)
        customer.save()
        if not Archive.objects.filter(realizedCallbacks_id=customer.pk):
            archive = Archive.objects.create(realizedCallbacks_id=customer.pk)
            archive.save()
        return JsonResponse({'message':'You successfully added comment'})







# function to set callbaks to realized and archive tham as un realized
@login_required
def makeCallbacksRealized(request):
    getData = Customer.objects.all()

    dateTimeNow = timezone.now()
    for data in getData:
        if data.date_and_time_for_callback < dateTimeNow and data.realized == False:
            data.realized = True
            data.administrator = 'By sistem'
            data.comment = 'This callback was not realized.'
            data.save()
            if not Archive.objects.filter(realizedCallbacks_id=data.pk):
                archive = Archive.objects.create(realizedCallbacks_id=data.pk)
                archive.save()
    return JsonResponse({'message':'Archiving of unrelized callback has been done!'})
