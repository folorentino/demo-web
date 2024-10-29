from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import json
 
from app.models import CreateUserForm

# Create your views here.
def signup(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'app/signup.html', context)


def loginPage(request):
    #if request.user.is_authenticated:
        #return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: 
            messages.info(request,'user or password not correct!')
    context = {}
    return render(request,'app/login.html',context)



def home(request):
    return render(request,'app/base.html')


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = product.objects.get(id = productId)
    order, created = order.objects.get_or_create(customer= customer, complete=False)
    orderItem, created = orderItem.objects.get_or_create(order= order, product =product)
    if action =='add':
        orderItem.quantity += 1
    elif action =='remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
        
    return JsonResponse ('added', safe=False)

def cart(request):
    context= {}
    return render(request, 'app/home.html')
def checkout(request):
    context= {}
    return render (request,'app/checkout.html',context)