from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import Item
from ..login_and_reg.views import print_errors
from ..login_and_reg.models import User

# Create your views here.
def check_session(request):
    return 'user' in request.session

def index(request):
    if not check_session(request):
        return redirect(reverse('users:index'))
    id = request.session['user']['id']
    context = {
        'my_wishlist': Item.objects.filter(user_added=id),
        'other_wishlist': Item.objects.exclude(user_added=id)
    }
    return render(request, 'wishlist/index.html', context)

def add(request):
    if not check_session(request):
        return redirect(reverse('users:index'))
    return render(request, 'wishlist/new.html')

def create(request):
    if not check_session(request):
        return redirect(reverse('users:index'))

    user = User.objects.get(id=request.session['user']['id'])
    result = Item.objects.create_item(request.POST, user)

    if result[0] == True:
        return redirect(reverse('wishlist:show', kwargs={'id': result[1].id}))
    else:
        print_errors(request, result[1])
        return redirect(reverse('wishlist:add'))

def show(request, id):
    if not check_session(request):
        return redirect(reverse('users:index'))

    context = {
        'item': Item.objects.get(id=id)
    }
    return render(request, 'wishlist/show.html', context)

def delete(request, id):
    if not check_session(request):
        return redirect(reverse('users:index'))

    Item.objects.delete(id, request.session['user']['id'])
    return redirect(reverse('wishlist:index'))

def join(request, id):
    if not check_session(request):
        return redirect(reverse('users:index'))

    Item.objects.join(id, request.session['user']['id'])
    return redirect(reverse('wishlist:index'))

def unjoin(request, id):
    if not check_session(request):
        return redirect(reverse('users:index'))

    Item.objects.unjoin(id, request.session['user']['id'])
    return redirect(reverse('wishlist:index'))
