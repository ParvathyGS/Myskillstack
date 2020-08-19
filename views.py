from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from PGFinder.forms import UserForm,LoginForm,ContactPg,FindPg

from django.db import models
from PGFinder.models import ContactPG,FindPG,Notifications
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string


# Create your views here.

def introPage(request):
	return render(request,"PGFinder/index.html")

def userRegister(request):

	if request.method == 'POST':
		user_detail = UserForm(request.POST)
		if user_detail.is_valid():

			username = user_detail.cleaned_data['Username']	
			email = user_detail.cleaned_data['EmailId']	
			password = user_detail.cleaned_data['Password']	
			confirm_password = user_detail.cleaned_data['Confirm_Password']
				
			if (password != confirm_password):
				return HttpResponse("Please enter the same password..")
			elif User.objects.filter(username=username).exists():
				return HttpResponse("Username/Email Already Exists")
			else:	
				user = User.objects.create_user(username, email, password)
				user.save()
				# user = user_detail.save()
				user.is_active = False
				user.save()
				current_site = get_current_site(request)
				mail_subject = 'Activate your PGFinder account.'
				message = render_to_string('PGFinder/acc_active_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
					'token':account_activation_token.make_token(user),
					})
				to_email = user_detail.cleaned_data.get('EmailId')
				email = EmailMessage(mail_subject, message, to=[to_email])
				email.send()
				return HttpResponse('Please confirm your email address to complete the registration')
	else:
		user_detail = UserForm()
		return render(request,'PGFinder/register.html',{'myform' : user_detail})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
	
def userLogin(request):
	if request.user.is_authenticated:
		return HttpResponse('You Are already logged in')
	else:	
		if request.method == 'POST':
			login_form = LoginForm(request.POST)
			if login_form.is_valid():

				username = login_form.cleaned_data['username']
				password = login_form.cleaned_data['password']

				user = authenticate(username=username, password=password)
							
				if user is not None:
					if user.is_active:
						login(request, user)	
						return HttpResponse('Login Successful')
					else:
						return HttpResponse('Your account is not active')
				else:
					return HttpResponse('The Account does not exists')
			else:
				login_form = LoginForm()
				return render(request, "PGFinder/login.html",{"myform":login_form})
		else:
			login_form = LoginForm()
			return render(request, "PGFinder/login.html",{"myform":login_form})


def userLogout(request):
    logout(request)
    return HttpResponse('Log Out succesfully')

	
def Contact_PG(request):

	if request.method == "POST":
		
		contact_pg  = ContactPg(request.POST)
		
		if contact_pg.is_valid():
			
			name_from_user = contact_pg.cleaned_data['Name']
			email_from_user = contact_pg.cleaned_data['Email']
			subject_from_user = contact_pg.cleaned_data['Subject']
			message_from_user = contact_pg.cleaned_data['Message']

			contact_pg_object = ContactPG(Name=name_from_user,Email=email_from_user,Subject=subject_from_user,Message=message_from_user)
			contact_pg_object.save()

			return HttpResponse("Message send succesfully!!")

	else:
		contact_pg  = ContactPg()
		return render(request,'PGFinder/contact.html',{'myform':contact_pg})

def Find_pg(request):

	if request.method == "POST":
		rentPlan = request.POST['Rentplan']
		roomType = request.POST['Roomtype']
		mealPlan = request.POST['Mealplan']
		loc = request.POST['Location']
		find_pg_object = FindPG.objects.filter(rentchoice=rentPlan,roomchoice=roomType,mealchoice=mealPlan,location=loc)
		return render(request,'PGFinder/findpg.html',{'findpg':find_pg_object})
	else:
		find_pg_form  = FindPg()
		return render(request,'PGFinder/findpg.html',{'myform':find_pg_form})

def sample_ajax_view(request,pg_id):

	find_pg_object = FindPG.objects.filter(id=pg_id).first()
	print(find_pg_object)
	data = list(find_pg_object)

	notifications_object = Notifications()
	notifications_object.pgname = find_pg_object.pgname
	notifications_object.username = request.user
	notifications_object.notif_msg = "Viewed your conatct information"
	notifications_object.save()

	return JsonResponse(data,safe=False)
	
def listPG(request):
	list_PG = FindPG.objects.all()
	context = {'findpg' : list_PG}
	return render(request,'PGFinder/listpg.html',context)

def addPG(request):
	if request.method == 'POST':
		addpg_form = FindPg(request.POST)
		if addpg_form.is_valid():

			pg_name_user = addpg_form.cleaned_data['Pgname']
			pg_addr_user = addpg_form.cleaned_data['Pgaddress']
			pg_rent_user = addpg_form.cleaned_data['Rentplan']
			pg_room_user = addpg_form.cleaned_data['Roomtype']
			pg_meal_user = addpg_form.cleaned_data['Mealplan']
			pg_location_user = addpg_form.cleaned_data['Location']
			pg_contactno_user = addpg_form.cleaned_data['ContactNo']

			addpg_object = FindPG(pgname=pg_name_user,pgaddress=pg_addr_user,rentchoice=pg_rent_user,roomchoice=pg_room_user,mealchoice=pg_meal_user,location=pg_location_user,contactno=pg_contactno_user)
			addpg_object.save()

			return HttpResponseRedirect("/PGFinder/listpg/")

	else:
		addpg_form = FindPg()
		return render(request,'PGFinder/addpg.html',{'myform': addpg_form})

def viewPG(request,pg_id):

	view_PG = FindPG.objects.get(id=pg_id)
	context = {'viewpg' : view_PG}
	return render(request,'PGFinder/viewpg.html',context)

def editPG(request,pg_id):

	if request.method == 'POST':
		editpg_form = FindPg(request.POST)

		if editpg_form.is_valid():
			editpg_object = FindPG.objects.get(id=pg_id)
			editpg_object.pgname = editpg_form.cleaned_data['Pgname']
			editpg_object.pgaddress = editpg_form.cleaned_data['Pgaddress']
			editpg_object.rentchoice = editpg_form.cleaned_data['Rentplan']
			editpg_object.roomchoice = editpg_form.cleaned_data['Roomtype']
			editpg_object.mealchoice = editpg_form.cleaned_data['Mealplan']
			editpg_object.location = editpg_form.cleaned_data['Location']
			editpg_object.contactno = editpg_form.cleaned_data['ContactNo']
			editpg_object.save()

			return HttpResponseRedirect("/PGFinder/listpg/")

	else:
		editpg_object = FindPG.objects.get(id=pg_id)
		editpg_form = FindPg(initial={"Pgname":editpg_object.pgname,
						"Pgaddress":editpg_object.pgaddress,"Rentplan":editpg_object.rentchoice,"Roomtype":editpg_object.roomchoice,
						"Mealplan":editpg_object.mealchoice,"Location":editpg_object.location,"ContactNo":editpg_object.contactno})
		return render(request,'PGFinder/editpg.html',{'myform': editpg_form,'pgid':pg_id})

def deletePG(request,pg_id):
	editpg_object = FindPG.objects.get(id=pg_id)
	editpg_object.delete()
	return HttpResponseRedirect("/PGFinder/listpg/")

def changePassword(request,user_id):

	if request.method == 'POST':
		change_pswd_form = UserForm(request.POST)

		if change_pswd_form.is_valid():
			change_pswd_object = User.objects.get(id=user_id)
			change_pswd_object.username = change_pswd_form.cleaned_data['Username']
			change_pswd_object.email = change_pswd_form.cleaned_data['EmailId']
			change_pswd_object.password = change_pswd_form.cleaned_data['Password']
			change_pswd_object.password = change_pswd_form.cleaned_data['Confirm_Password']
			change_pswd_object.set_password("change_pswd_object.password")
			change_pswd_object.save()

			current_site = get_current_site(request)
			mail_subject = 'Password of your PGFinder account changed'
			message = render_to_string('PGFinder/chgpswdmail.html', {
				'user': change_pswd_object,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(change_pswd_object.pk)).decode(),
				'token':account_activation_token.make_token(change_pswd_object),
				})
			to_email = change_pswd_object.email
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			return HttpResponse('Password changed and a notification mail is send to your email id')

	else:
		change_pswd_form = UserForm()
		return render(request,'PGFinder/changepassword.html',{'myform': change_pswd_form})