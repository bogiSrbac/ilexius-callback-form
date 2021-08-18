from django.shortcuts import render
from .models import Customer, CallbackTableActive
from .forms import CreateCusomerForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from datetime import datetime, date
import datetime
from django.utils import timezone
from.additional_functions import workDayFunction, createTime, timeNow, nextDayTerm, returnNextDay


def base(request):

    datum = Customer.objects.all()
    for i in datum:
        print(i.date_and_time_for_callback)
    context = {
        'datum': datum
    }
    return render(request, 'customerServiceSupport/index.html', context)


def createCustomerView(request):
    formCustomer = CreateCusomerForm(request.POST or None)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        if formCustomer.is_valid():
            print('poslano1')
            dateTimeSave = formCustomer.save(commit=False)
            if Customer.objects.filter(date_and_time_for_callback=dateTimeSave.date_and_time_for_callback, date_and_time_for_callback__isnull=False):
                return JsonResponse({'error': 'That term is booked'})
            elif Customer.objects.filter(first_name__exact=dateTimeSave.first_name, last_name__exact=dateTimeSave.last_name, email=dateTimeSave.email, first_name__isnull=False):
                name = Customer.objects.filter(first_name__exact=dateTimeSave.first_name, last_name__exact=dateTimeSave.last_name, email=dateTimeSave.email, first_name__isnull=False)
                for firstName in name:
                    date = firstName.date_and_time_for_callback.strftime('%d-%m-%Y')
                    time = firstName.date_and_time_for_callback.strftime('%H:%M')
                    message = f'You are already reserved term. </br>{firstName.first_name} {firstName.last_name} has callback term on {date} at {time}'
                    return  JsonResponse({'message':message})

            else:
                if dateTimeSave.date_and_time_for_callback == None:
                    defaultTerm = Customer.objects.filter(date_and_time_for_callback__year=datetime.datetime.now(tz=timezone.utc).year, date_and_time_for_callback__month=datetime.datetime.now(tz=timezone.utc).month,
                                                          date_and_time_for_callback__day=datetime.datetime.now(tz=timezone.utc).day,)
                    listBooked = []
                    listFreeTerms = []
                    for day in defaultTerm:
                        listBooked.append(createTime(day.date_and_time_for_callback))
                    dayOfWeek = datetime.datetime.now(tz=timezone.utc).weekday()
                    dayOfWeek2 = 6
                    for i in workDayFunction(dayOfWeek):
                        if i not in listBooked:
                            if datetime.datetime.strptime(i, '%H:%M').time() > datetime.datetime.now().time() and datetime.datetime.now().time() < datetime.datetime.strptime(i, '%H:%M').time() and dayOfWeek2 != 6:
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


                                    def returnDayOfWeek(listOfDays):
                                        if len(listOfDays) < 24 and len(listOfDays) > 0 and listOfDays[0].weekday() != 6:
                                            dayOfWeek1 = listOfDays[0].weekday()
                                            return dayOfWeek1
                                        else:
                                            print(returnNextDay())
                                            return returnNextDay()
                                    t = returnDayOfWeek(listDate)
                                    t2 = datetime.datetime.now().date().weekday()
                                    for j in workDayFunction(t):
                                        if j not in listBooked1:
                                            listFreeTerms1.append(j)
                                    if len(listFreeTerms1) > 0 and t2 != 6 and t2 != 5:
                                        print(listDate[0].weekday())
                                        addCallbackTime1 = datetime.datetime.combine(
                                            data,
                                            datetime.datetime.strptime(listFreeTerms1[0], '%H:%M').time())
                                        dateTimeSave.date_and_time_for_callback = addCallbackTime1
                                        print(addCallbackTime1, 'provjera nova')
                                        break
                                    elif len(listFreeTerms1) > 0 and t2 == 5:
                                        addCallbackTime1 = datetime.datetime.combine(
                                            data + datetime.timedelta(days=1),
                                            datetime.datetime.strptime(listFreeTerms1[0], '%H:%M').time())
                                        dateTimeSave.date_and_time_for_callback = addCallbackTime1
                                        print(addCallbackTime1, 'provjera nova subota')
                                        break
                                else:
                                        pass





                yourDate = dateTimeSave.date_and_time_for_callback
                date = yourDate.strftime('%d-%m-%Y')
                time = yourDate.strftime('%H:%M')
                dateTimeSave.save()
                callbackAktivetable = CallbackTableActive.objects.create(customer_id=dateTimeSave.id)
                callbackAktivetable.save()
                formCustomer = CreateCusomerForm()
                return JsonResponse({'success': f'You submit callback successfully! <br> Your term is on {date} at {time}!'})

            # mail = Customer.objects.filter(email__isnull=False).order_by('-pk')[0]
            # attach_emil = 'Email posiljaoca = [' + str(mail.vas_email) + '] ' + str(mail.vasa_poruka)
            # send_mail(mail.naziv_poruke, attach_emil, mail.vas_email, ["realauto.polovniautomobili@gmail.com"], fail_silently=False)


        else:
            return JsonResponse({'failure': 'Your message was not submitted!'})

    else:
        formCustomer = CreateCusomerForm()
        print('poslano4')


    return render(request, 'customerServiceSupport/customerServiceSupport.html', {'formCustomer': formCustomer})