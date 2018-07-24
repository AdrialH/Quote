from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import *

import bcrypt

def index(request):

    return render(request, 'first_app/index.html')

def logged(request):
    errors = {}
    if 'user' not in request.session:
        errors['error'] = "Must register before you can log in."
        if (errors):
            for key, value in errors.items():
                messages.error(request, value)
        return redirect('/')
    else:
        context = {
            'user': Message.objects.all(),
            'like': User.objects.get(id = request.session['user'])
        }

    return render(request, 'first_app/logged_in.html', context)


def login(request):
    errors = User.objects.login_validator(request.POST)

    if(errors):
        for key, value in errors.items():
            messages.error(request, value)    
        return redirect('/')

    else:
        if not errors:
            success = {}
            user = User.objects.get(email = request.POST['email'])
            request.session['user'] = user.id
            for key, value in success.items():
                messages.success(request, value)
      
        return redirect('/logged')
        
    
        

def create(request):
    errors = User.objects.basic_validator(request.POST)

    if (errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        success = {}
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['firstname'],last_name=request.POST['lastname'], email=request.POST['email'], password = hash1)
        success['create'] = "Welcome! You have successfully registered " + request.POST['firstname']
        user = User.objects.get(email = request.POST['email'])
        request.session['user'] = user.id
        if (success):
            for key, value in success.items():
                messages.success(request, value)
        return redirect('/logged')


def createpost(request):
    errors = Message.objects.message_validator(request.POST)
    if 'user' not in request.session:
        errors['error'] = "Must register before you can log in."
        return redirect('/')
    else:
        
        if (errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/logged')
    
        else:
        
            user = User.objects.get(id = request.session['user'])
            item = Message.objects.create(item = request.POST['post'], user_post = user)
            user.post.add(item)
            return redirect('/logged')

def create3(request):
    user = User.objects.get(id = request.session['user'])
    item = Message.objects.get(id = request.POST['item'])
    user.likes.add(item)
    return redirect('/logged')

def view(request):
    
    return render(request, 'first_app/additem.html')

def viewitem(request, id):
    context = {
        'item': User.objects.get(id = id)
    }
    return render(request, 'first_app/item.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')

def goback(request):
    return redirect('/logged')

def edit(request, id):
    return render(request, 'first_app/edit.html', { 'user': User.objects.get(id=id)})
    
def update(request, id):
    
    errors = User.objects.update_validator(request.POST)
        
    if len(errors):
            
        for key, value in errors.items():
            messages.error(request, value)
            
        return redirect('/edit/'+id)
    else:
        success={}   
        user = User.objects.get(id = id)
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email = request.POST['email']
        user.save()
        success['success']="Acount updated successfully." 
        for key, value in success.items():
            messages.success(request, value)
            
        return redirect('/logged')

def delete(request):
    b= Message.objects.get(id = request.POST['item'])
    b.delete()
    return redirect('/logged')
