from django.shortcuts import render, redirect
from nopass_login.utility import get_html_context
from nopass_login.queries import remove_account, get_account, add_account
from nopass_login.forms import LoginForm

import time

def index(request):
    html_context = get_html_context()
    html_context["tab_index"] = "active" 

    if request.COOKIES.get('token', None) != None:
        html_context['token'] = request.COOKIES.get('token', None)
        html_context['username'], html_context['is_admin'] = get_account(request.COOKIES.get('token', ''))

    response = render(request, 'index.html', html_context)
    return response

def login(request):
    html_context = get_html_context()
    html_context["tab_login"] = "active"
    
    if request.COOKIES.get('token', None) == None:
        if request.method == "POST":
            response = redirect('index_page')
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                try:
                    new_token = add_account(login_form.data['username'])
                    response = redirect('index_page')
                    response.set_cookie('token', new_token, max_age=86400)
                    return response
                except:
                    html_context['error_msg'] = "Login failed: Already found token with the same username"
            else:
                html_context['error_msg'] = "Login failed: invalid data"
        
        response = render(request, 'login.html', html_context)
    else:
        response = redirect('index_page')
    return response

def logout(request):
    response = redirect('login_page')
    if request.COOKIES.get('token', None) != None:
        try:
            remove_account(request.COOKIES.get('token', ''))
        except:
            pass
        response.delete_cookie('token')
    return response

def flag(request):
    html_context = get_html_context()
    html_context["tab_flag"] = "active"
    
    if request.COOKIES.get('token', None) != None:
        html_context['token'] = request.COOKIES.get('token', None)
        html_context['username'], html_context['is_admin'] = get_account(request.COOKIES.get('token', ''))
        if html_context['username'] == '':
            response = redirect('login_page')
        else:
            response = render(request, 'flag.html', html_context)
    else:
        response = redirect('login_page')
    return response
