from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from random import randint
from django.core.mail import EmailMessage
from tryDjango import settings
from .forms import MyForm
from .models import ConfUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):

	return render(request,'profiles/home.html')

def register(request):
	if request.method == "POST":
		data = MyForm(request.POST)
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		if not password1 == password2 :
		    messages.error(request,"Passwords doesn't match")
		pwd = str(randint(100000,999999))
		try :
			if data.is_valid and first_name!='' and last_name!='' and email!='' :
				data.save()
				ConfUser.objects.create(user_name=username,email=email,vercode=pwd)
			else :
				return HttpResponse("Please enter valid data")
			sub = "Verification Code"
			body = """Hello {}\n\nThis is your username : {}\nYour verification code is : {}\n""".format(first_name+' '+last_name,username,pwd)
			sender = settings.EMAIL_HOST_USER
			receiver = email
			EmailMessage(sub,body,sender,[receiver]).send()
			data = User.objects.get(username=username)
			return redirect('confirmreg',id=data.id)
		except :
			messages.error(request,"User already exists.")
	form = MyForm()
	return render(request,'profiles/register.html',{'form':form})

def confirmreg(request,id):
    data = User.objects.get(id=id)
    data1 = ConfUser.objects.get(user_name=data.username)
    username = data1.user_name
    data = User.objects.filter(username=username)
    if 'ver_code' in request.GET:
        ver_code = request.GET.get('ver_code')
        if int(data1.vercode) == int(ver_code):
            data1.vercode = "confirmed"
            data1.save()
            return redirect('register')
        else:
            data.delete()
            return HttpResponse("Invalid code entered")
    return render(request,'profiles/confirmreg.html',{'id':id})

@login_required
def profile(request,id):
	data = User.objects.get(id=id)
	data1 = ConfUser.objects.get(user_name=data.username)
	if not data1.vercode == "confirmed":
	    messages.error(request,"Your account is not verified")
	return render(request,'profiles/profile.html',{'data':data})

@login_required
def loginhome(request):
    return render(request,'profiles/loginhome.html')

@login_required
def edit(request,id):
	data = User.objects.get(id=id)
	if request.method == 'POST':
		data.first_name = request.POST.get('fname')
		data.last_name = request.POST.get('lname')
		data.save()
		return redirect('loginhome')
	return render(request,'profiles/edit.html',{'data':data})

@login_required
def delete(request,id):
    data = User.objects.get(id=id)
    return render(request,'profiles/delete.html',{'data':data})

@login_required
def confirm(request,id):
	data = User.objects.get(id=id)
	data1 = ConfUser.objects.get(user_name=data.username)
	data.delete()
	data1.delete()
	return redirect('home')