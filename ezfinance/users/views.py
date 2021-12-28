from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm,AccountUpdateForm,UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json
import requests


def register(request):
    if 'contactus' in request.POST:
        return redirect('contact_us')

    if 'reg_btn' in request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account had successfully created for {username}!')
            return redirect('register')
        else:
            messages.warning(request, f'Failed to Register. Please Try Again')
    else:
        form = UserRegisterForm()


    if 'login_btn' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        #Recaptcha stuff
        clientKey=request.POST['g-recaptcha-response']
        secretKey='6LeCW9oUAAAAACPE4wbi41IdBS8yZ-BzMSEOxIIT'
        capthchaData={
            'secret':secretKey,
            'response':clientKey
        }
        r=requests.post('https://www.google.com/recaptcha/api/siteverify',data=capthchaData)
        response=json.loads(r.text)
        verify=response['success']

        if user is not None:
            if user.is_active and verify:
                if user.is_staff:
                    login(request, user)
                    return redirect('admin_site_home')
                else:
                    login(request, user)
                    return redirect('EzFinance-Account-home')
            else:
                messages.warning(request, f'Your account currently inactive. Please contact Customer Service')
        else:
            messages.warning(request, f'Failed to Login. Please Try Again')

    return render(request, 'users/register.html', {'form': form})



