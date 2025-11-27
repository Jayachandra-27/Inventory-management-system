from urllib import response
from django.http import HttpResponse
from django.views.generic import TemplateView,View
from django.shortcuts import redirect, render
from .models import InventoryItem,Category
from project.settings import low_quantity
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import authenticate 
from django.contrib import auth

# Create your views here.
class home(TemplateView):
    template_name='inventory/home.html'

class dashboard(View):
    def get(self,request):
        items=InventoryItem.objects.all().order_by('-id')
        low_inventory=InventoryItem.objects.filter(quantity__lte=low_quantity)
        
        if low_inventory.count() > 1:
            messages.error(request, f'{low_inventory.count()} items have low inventory')
        else:
            messages.error(request, f'{low_inventory.count()} item has low inventory')

        low_inventory_ids=InventoryItem.objects.filter(quantity__lte=low_quantity).values_list('id',flat=True)

        context={
            'items':items,
            'low_inventory_ids':low_inventory_ids
        }
        return render(request,'inventory/dashboard.html',context)
    

class SignUpView(View):
    def get(self,request):
        form=RegistrationForm
        context={
            'form':form
        }
        return render(request,'inventory/signup.html',context)
    
    def post(self,request):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request, "Account created and logged in.")
                return redirect('dashboard')

        
        return render(request,'inventory/signup.html',{'form':form})