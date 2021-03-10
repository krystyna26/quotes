from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from models import User

def index(request):
    return render(request, "quote_app/index.html")


def register(request):
    result = User.objects.register_validator(request.POST)
    if len(result) == 0:
        password = request.POST['password']
        hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5))
        User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=hashed
            )
        request.session['user_id'] = result.id
        messages.success(request, "Successfully registered!")
        return redirect('/success')
    else:
        for err in result:
            messages.error(request, err)
            return redirect('/')


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
    # read
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'quote': Quote.objects.all(),
        # get all of the quotes liked by this user
        # "quote": Quote.objects.exclude(favorite=user),
        # 'favoritesQuote': user.objects.liked_quotes.all()
        "favoritesQuote": User.objects.filter(favorite=user)
    }
    return render(request, "quote_app/welcome.html", context)
    

def addQuote(request):
    result = Quote.objects.quote_validator(request.POST)
    # user = User.objects.get(id=request.session['user_id'])
    if type(result) == list:
        for err in result:
            messages.error(request, err, extra_tags=addQuote)
        return redirect('/success')
    messages.success(request, "Successfully added quote!")
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


def moveToFav(request, quote_id, user_id):
    # update
    this_quote = Quote.objects.get(id=quote_id)
    this_user = User.objects.get(id=user_id)
    this_quote.favorite.add(this_user)
    return redirect('/success')


def moveToQuotes(request, quote_id, user_id):
    # update quote
    this_user = User.objects.get(request.session['user_id'])
    this_quote = Quote.objects.filter(liked_quotes=this_user)
    Quote.objects.exclude(liked_quotes=this_user)
    # this_user.liked_quotes.remove(this_quote)
    return redirect('/success')


def logout(request):
    context = {
        "logout" : request.session.pop("user_id")
        }
    return render(request, "quote_app/index.html", context)