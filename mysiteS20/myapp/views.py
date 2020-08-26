from time import time,ctime

from django.core import mail
from django.shortcuts import render
# Create your views here.
# Import necessary classes
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta

from .forms import OrderForm, InterestForm, RegisterForm, ForgotPassword
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
'''def index(request):
    top_list = Course.objects.all().order_by('-price')[:5]
    response = HttpResponse()
    heading1 = '<p>' + 'List of Courses: ' + '</p>'
    response.write(heading1)
    for topic in top_list:

        if topic.for_everyone:
            para1 = '<p>' + str(topic.id) + ': ' + str(topic) + ':This Course is For Everyone!' + '</p>'
        else:
            para1 = '<p>' + str(topic.id) + ': ' + str(topic) + ':This Course is Not For Everyone!' + '</p>'
        response.write(para1)
    return response
'''


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})


'''def about(request):
    response = HttpResponse()
    #It will return coookie if found otherwise false
    if request.COOKIES.get('about_visits'):
        visit = request.COOKIES.get('about_visits') + 1
        response.set_cookie('about_visits', value = visit, expires = datetime.datetime.minute + 5)
    heading = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses.' + '</p>'
    # response.write(heading)
    return render(request, 'myapp/about.html', {'heading': heading})
'''


def about(request):
    heading = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses.' + '</p>'
    response = render(request, 'myapp/about.html', {'heading': heading})
    # It will return coookie if found otherwise false
    if request.COOKIES.get('about_visits', False):
        visit = int(request.COOKIES.get('about_visits')) + 1
        # dt = datetime.now() + timedelta(minutes=5)
        response.set_cookie('about_visits', value=visit, max_age=300)
    else:
        visit = int(1)
        # dt = datetime.now() + timedelta(minutes=5)
        response.set_cookie('about_visits', value=visit, max_age=300)
    # response.write(heading)
    return response


'''def detail(request, top_no):
    response = HttpResponse()
    #topic_category = Topic.objects.get(id = top_no).category
    topic_category = get_object_or_404(Topic, id = top_no).category
    para1 = '<p>' + 'Topic Category: ' + str(topic_category) + '</p>'
    response.write(para1)
    topic_name = Topic.objects.get(id=top_no).name
    course_list = Course.objects.filter(topic__name=topic_name)
    #print(course_list)
    heading = '<p>' + 'List of Courses for the above topic: ' + '</p>'
    response.write(heading)
    for cou in course_list:
        para1 = '<p>' + str(cou.name) + '</p>'
        response.write(para1)
    return response'''


def detail(request, top_no):
    topic_category = get_object_or_404(Topic, id=top_no).category
    topic_name = Topic.objects.get(id=top_no).name
    course_list = Course.objects.filter(topic__name=topic_name)
    return render(request, 'myapp/detail.html',
                  {'topic_category': topic_category, 'topic_name': topic_name, 'course_list': course_list})


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    '''text = '<p>' + 'You can place an order here' + '</p>'
    response = HttpResponse()
    response.write(text)
    return response'''

    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                # msg = 'Your course has been ordered successfully.'
                if order.course.price > 150:
                    order.course.discount()
                    msg = 'Your course has been ordered successfully with the discounted price.'
                else:
                    msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})


def coursedetail(request, cour_no):
    msg = ''
    courlist = get_object_or_404(Course, id=cour_no)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        # All the form data now is converted into dictonary
        if form.is_valid():
            if form.cleaned_data['interested'] == 'Yes':
                courlist.interested += 1
                courlist.save()
                msg = 'Your interest has been registered'
            else:
                msg = 'Thank you for your response'
        return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = InterestForm
    return render(request, 'myapp/coursedetail.html', {'form': form, 'msg': msg, 'courlist': courlist})


def user_login(request):
    request.session['last_login'] = ctime()
    #to expire after cetain seconds
    #request.session.set_expiry(3600)
    #to expire as the user closes the window
    request.session.set_expiry(0)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                request.session['username'] = username
                request.session['first_name'] = Student.objects.get(username__iexact=username).first_name
                request.session['last_name'] = Student.objects.get(username__iexact=username).last_name
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    #request.session.flush()
    return HttpResponseRedirect(reverse('myapp:index'))


def myaccount(request):
    if (request.user.is_authenticated):
        count = Student.objects.filter(username__iexact=request.user.username).count()
        if count == 1:
            student_details = Student.objects.get(username__iexact=request.user.username)
            course_order = Order.objects.filter(student__username__iexact=request.user.username)
            topic_interested = Student.objects.get(first_name__iexact=request.user.username).interested_in.all()
            return render(request, 'myapp/myaccount.html',
                          {'student_details': student_details, 'course_order': course_order,
                           'topic_interested': topic_interested})
        else:
            msg = 'You are not a registered student'
            return render(request, 'myapp/order_response.html', {'msg': msg})

    else:
        msg = 'Not Logged In'
        #return render(request, 'myapp/login.html', {'msg': msg})
        return HttpResponseRedirect(reverse('myapp:user_login'))


def register(request):
    msg = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            msg = 'Your data has been registered in our database'
            form.save()
            return render(request, 'myapp/order_response.html', {'msg': msg})
        else:
            msg = 'Please make sure data entered is correct'
            render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = RegisterForm
    return render(request, 'myapp/register.html',{'form':form,'msg':msg,})

def forgotPassword(request):
    msg = ''
    if request.method == 'POST':
        form = ForgotPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            count = Student.objects.filter(email=email).count()
            if count == 1:
                u = Student.objects.get(email=email)
                newpass = Student.objects.make_random_password(length=10)
                u.set_password(newpass)
                email1 = mail.EmailMessage(
                    'Password Reset',
                    'Your new password: ' + newpass,
                    'ramjaydeep@gmail.com',
                    [email],
                )
                email1.send()
                u.save()
                msg = 'Check your inbox for your new password'
                return render(request, 'myapp/order_response.html', {'msg': msg, })
            else:
                msg = 'Entered Email Address is not registered'
                return render(request, 'myapp/order_response.html',{'msg':msg,})
        else:
            msg = 'Email field is required'
            return render(request, 'myapp/order_response.html', {'msg': msg, })
    else:
        form = ForgotPassword
    return render(request, 'myapp/forgotPass.html', {'form': form, 'msg': msg, })
