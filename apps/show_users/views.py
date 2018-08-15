from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'show_users/index.html', { 'users': User.objects.all() })

def new(request):
    return render(request, 'show_users/new.html')

def edit(request, id):
    return render(request, 'show_users/edit.html', { 'user': User.objects.get(id = id) })

def show(request, id):
    return render(request, 'show_users/show.html', { 'user': User.objects.get(id = id) })

def create(request):
    print('came here!')
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'])
        return redirect('/')

def destroy(request, id):
    User.objects.get(id = id).delete()
    return redirect('/')

def update(request, id):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        # return redirect('/users/' + id + '/edit/')
        return redirect(f'/${id}/edit')
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the blog to be updated, make the changes, and save
        user = User.objects.get(id = id)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        messages.success(request, "user successfully updated")
        # redirect to a success route
        return redirect('/')