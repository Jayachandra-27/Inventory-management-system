from urllib import response
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView,View,UpdateView,DeleteView,CreateView
from django.shortcuts import redirect, render
from .models import InventoryItem,Category
from project.settings import low_quantity
from django.contrib import messages
from .forms import RegistrationForm,InventoryItemForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth import authenticate 
from django.contrib import auth

# Create your views here.
class home(TemplateView):
    template_name='inventory/home.html'

class dashboard(LoginRequiredMixin,View):
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
    



    
class edit_item(LoginRequiredMixin,UpdateView):
    model=InventoryItem
    form_class=InventoryItemForm
    template_name='inventory/editform.html'
    success_url = reverse_lazy('dashboard')

class delete_item(LoginRequiredMixin,DeleteView):
    model=InventoryItem
    # form_class=InventoryItemForm
    template_name='inventory/delete.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'

class add_item(LoginRequiredMixin,View):
    def get(self, request):
        form = InventoryItemForm()
        return render(request, 'inventory/editform.html', {'form': form})

    def post(self,request):
        form=InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return render(request,'inventory/editform.html',{'form':form})
	
class SignUpView(View):
    def get(self,request):
        form=RegistrationForm
        return render(request,'inventory/signup.html',{'form':form})



    def post(self,request):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created — please sign in.")
            return redirect('signin')
        
        return render(request,'inventory/signup.html',{'form':form})
    
    

class signinView(View):
    def get(self, request):
        form = AuthenticationForm()                  
        return render(request, 'inventory/signin.html', {'form': form})

    def post(self,request):
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                messages.success(request, "Account logged in.")
                return redirect('home')
            messages.error(request, "Invalid credentials.")

        
        return render(request,'inventory/signin.html',{'form':form})
    

class signoutView(View):
    def get(self,request):

        auth.logout(request)
        return redirect('signin')