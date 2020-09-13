from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Data
from django.contrib import messages
from .forms import DataForm
from Forms import settings
from  django.core.mail import EmailMessage
import random


# Create your views here.
def home(request):
	return render(request,'MyApp/home.html')

def register(request):
	form = DataForm(request.POST,request.FILES)
	if form.is_valid():
		form.save()
		messages.success(request,request.POST['first_name']+' is added successfully')
	form = DataForm()
	return render(request,'MyApp/register.html',{'form':form})

def status(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		try:
			data = Data.objects.get(email=email)
		except:
			return HttpResponse("Invalid Email")
		return redirect('show',id=data.id)
	return render(request,'MyApp/status.html')

def show(request,id):
	data = Data.objects.get(id=id)
	return render(request,'MyApp/show.html',{'data':data})

def edit(request,id):
	data = Data.objects.get(id=id)
	if request.method == 'POST':
		data.first_name = request.POST.get('fname')
		data.last_name = request.POST.get('lname')
		data.date_of_birth = request.POST.get('dob')
		data.save()
		return redirect('home')
	return render(request,'MyApp/edit.html',{'data':data})

def delete(request,id):
	data = Data.objects.get(id=id)
	return render(request,'MyApp/delete.html',{'data':data})

def confirm(request,id):
	data = Data.objects.get(id=id)
	data.delete()
	return redirect('home')