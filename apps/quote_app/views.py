from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, "quote_app/index.html")


def register(request):
    result = User.objects.register_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/success')


def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err,)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect('/success')

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    # read
    context = {
        'user': user,
        'quote': Quote.objects.all()
    }
    return render(request, "quote_app/welcome.html", context)
    
def addQuote(request):
    # result = Quote.objects.quote_validator(request.POST)
    # user = User.objects.get(id=request.session['user_id'])

    # if type(result) == list:
    #     for err in result:
    #         messages.error(request, err, extra_tags=addQuote)
    #     return redirect('/success')
    # messages.success(request, "Successfully added quote!")

    user = User.objects.get(id=request.session['user_id'])
    # create
    quote = Quote.objects.create(
        content = request.POST['content'],
        author = request.POST['author'],
        uploader = user,
        favBoolean = False 
    )
    return redirect('/quote')
    

def showuser(request, id):
    user = User.objects.get(id=id)
    quote = Quote.objects.filter(uploader=user)
    count = quote.count()
    context = {
        "user": user,
        "quotesMade": quote,
        "countQuotes": count,
    }
    return render(request, "quote_app/user.html", context)

def moveToFav(request, quote_id):
    # update
    quote = Quote.objects.get(id=quote_id)
    quote.favBoolean = "True"
    quote.save()
    return redirect('/success')

def moveToQuotes(request, quote_id):
    # update quote
    quote = Quote.objects.get(id=quote_id)
    quote.favBoolean = "False"
    quote.save()
    return redirect('/success')


def logout(request):
    context = {
        "logout" : request.session.pop("user_id")
        }
    return render(request, "quote_app/index.html", context)