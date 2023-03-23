from django.http import HttpResponse
## from django.contrib import messages
from django.shortcuts import render,redirect,reverse,get_object_or_404
from barbers.models import Appointment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
#Login Requirements
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
# Create your views here.
def index(request):
    return render(request, "barbers/index.html")


def login_view(request):
    if request.method == 'POST':
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.add_message(request, messages.WARNING,
                                 'Invalid credentials, try again')
            return render(request, 'users/login.html', context,)

        login(request, user)

        messages.add_message(request, messages.SUCCESS,
                             f'Welcome  {user.username} ')

        return redirect(reverse('userPanel'))

    return render(request, 'users/login.html')


#dashboard
@login_required(login_url='login')
def userPanel(request):
    user = request.user
    appointments =Appointment.objects.filter(user=user).order_by('day', 'time')
    context={ 'user':user,'appointments':appointments }
    return render(request, 'barbers/dashboard.html',context)


@login_required(login_url='login')
def booking(request):
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        if service == None:
            messages.success(request, "Please Select A Service!")
            return redirect('booking')

        #Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect('bookingSubmit')


    return render(request, 'barbers/booking.html', {
            'weekdays':weekdays,
            'validateWeekdays':validateWeekdays,
        })


@login_required(login_url='login')
def bookingSubmit(request):
    user = request.user
    #Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(22)

    #Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)
    times = [
        "8 AM","8:30AM","10AM","12:30PM","1:30 PM", "2:30 PM","3 PM", "3:30 PM", "4 PM", "4:30 PM", "5 PM", "5:30 PM", "6 PM", "6:30 PM", "7 PM", "7:30 PM"
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    #Get stored data from django session:
    day = request.session.get('day')
    service = request.session.get('service')
    
    #Only show the time of the day that has not been selected before:
    hour = checkTime(times, day)
    if request.method == 'POST':
        time = request.POST.get("time")
        date = dayToWeekday(day)

        if service != None:
            if day <= maxDate and day >= minDate:
                if date == 'Monday' or date == 'Saturday' or date == 'Wednesday':
                    if Appointment.objects.filter(day=day).count() < 11:
                        if Appointment.objects.filter(day=day, time=time).count() < 1:
                            AppointmentForm = Appointment.objects.get_or_create(
                                user = user,
                                service = service,
                                day = day,
                                time = time,
                            )
                            messages.success(request, "Appointment Saved!")
                            return redirect('userPanel')
                        else:
                            messages.success(request, "The Selected Time Has Been Reserved Before!")
                    else:
                        messages.success(request, "The Selected Day Is Full!")
                else:
                    messages.success(request, "The Selected Date Is Incorrect")
            else:
                    messages.success(request, "The Selected Date Isn't In The Correct Time Period!")
        else:
            messages.success(request, "Please Select A Service!")


    return render(request, 'barbers/bookingsubmit.html', {
        'times':hour,
    })

def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y

def validWeekday(days):
    #Loop days you want in the next 21 days:
    today = datetime.now()
    weekdays = []
    for i in range (0, days):
        x = today + timedelta(days=i)
        y = x.strftime('%A')
        if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
            weekdays.append(x.strftime('%Y-%m-%d'))
    return weekdays
    
def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:
            validateWeekdays.append(j)
    return validateWeekdays

def checkTime(times, day):
    #Only show the time of the day that has not been selected before:
    x = []
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1:
            x.append(k)
    return x

def checkEditTime(times, day, id):
    #Only show the time of the day that has not been selected before:
    x = []
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
            x.append(k)
    return x