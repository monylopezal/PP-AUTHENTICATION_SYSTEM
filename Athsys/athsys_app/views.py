#Import methods to be used
from django.contrib.auth import hashers
from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .forms import UserRegisterForm
from .models import *
import datetime
from datetime import datetime
import json

# Function that displays all recorded events
def inicio(request): 
    if request.user.is_authenticated:
        eventlogin = EventLogin.objects.filter(user=request.user.pk)
        context = {'eventlogin' : eventlogin, 'user': request.user.pk}
        return render(request, 'main/inicio.html', context)
    else:
        return redirect('login')
#Function that displays the registration form and saves the record in the database once the information has been submitted.
def register(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = UserRegisterForm()
        context = { 'form' : form }
        return render(request, 'main/register.html', context)
#Function that sends an email to recover the password and updates the new password
def password_reset_request(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    else:
        if request.method == "POST":
            password_reset_form = PasswordResetForm(request.POST)
            if password_reset_form.is_valid():
                data = password_reset_form.cleaned_data['email']
                associated_users = User.objects.filter(Q(email=data))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "main/password/password_reset_email.txt"
                        c = {
                            "email":user.email,
                            'domain':'127.0.0.1:8000',
                            'site_name': 'Website',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        return redirect ("/password_reset/done/")
        password_reset_form = PasswordResetForm()
        return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})
#Function to obtain the records filtered by date
def events_get(request):
    if request.is_ajax():
        if request.method == 'POST':
            timestmp = datetime.strptime(request.POST['timestamp'], '%Y-%m-%d')
            idus = request.POST['id']
            list_event=EventLogin.objects.filter(timestamp__startswith=datetime.date(timestmp)).filter(user=idus)
            eventget = []
            for listeventlogin in list_event:
                data = {}
                date = listeventlogin.timestamp
                data['timestamp'] = date.strftime('%Y-%m-%d %H:%M:%S')
                eventget.append(data)
            eventlist = json.dumps(eventget)
            return HttpResponse(eventlist)