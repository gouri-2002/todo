from django.shortcuts import render, redirect
from django.views.generic import View
from task.forms import SignUpForm, SignInForm, TodoForm
from django.contrib.auth import authenticate, login, logout
from task.models import Todo
from task.decorators import signin_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.

decorators = [signin_required, never_cache]

class SignUpView(View):
    
    template_name = 'signin_signup.html'
    form_class = SignUpForm
    
    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return redirect('index')
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form, 'action':'Signup', 'text':'Already have an account?', 'alt_action':'Login'})
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)

        if form.is_valid():
            
            form.save()
            print('Account created successfully')
            return redirect('signin')
        
        print('Failed to create user!!')
        return render(request, self.template_name, {'form':form, 'action':'Signup', 'text':'Already have an account?', 'alt_action':'Login'})   


@method_decorator(never_cache, name='dispatch')
class SignInView(View):
    
    template_name = 'signin_signup.html'
    form_class = SignInForm
    
    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return redirect('index')
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form, 'action':'Login', 'text':'Don\'t have an account?', 'alt_action':'Signup'})

    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)

        if form.is_valid():
            
            data = form.cleaned_data
            
            uname = data.get('username')
            pwd = data.get('password')
            
            user_obj = authenticate(request, username=uname, password=pwd)
            
            if user_obj:
                
                login(request, user_obj)
                
                print('session started')
                return redirect('index')
            
        print('invalid credential')
        return render(request, self.template_name, {'form':form, 'action':'Login', 'text':'Don\'t have an account?', 'alt_action':'Signup'})

  
@method_decorator(decorators, name='dispatch')
class SignOutView(View):
    
    def get(self, request, *args, **kwargs):
        
        logout(request)
        print('session ended')
        return redirect('signin')

  
@method_decorator(decorators, name='dispatch')  
class IndexView(View):
    
    template_name = 'index.html'
    form_class = TodoForm

    def get(self, request, *args, **kwargs):
        
        qs = Todo.objects.filter(owner=request.user.id)
        
        form = self.form_class()
        
        return render(request, self.template_name, {'form':form, 'data':qs})
    
    
    def post(self, request, *args, **kwargs):
        
        form_data = request.POST
        form = self.form_class(form_data)
        
        if form.is_valid():
            
            # form.instance => TodoForm
            # form.instance.owner => model of TodoForm - Todo
            
            # Adding user to form instance
            form.instance.owner = request.user
            form.save()
            return redirect('index')
        
        return render(request, self.template_name, {'form':form})

 
@method_decorator(decorators, name='dispatch')    
class TodoDeleteView(View):
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        Todo.objects.get(id=id).delete()
        return redirect('index')


@method_decorator(decorators, name='dispatch')   
class TodoUpdateView(View):
    
    def get(self, request, *args, **kwargs):
        
        id = kwargs.get('pk')
        Todo.objects.filter(id=id).update(status=True)
        return redirect('index')
    

@method_decorator(decorators, name='dispatch') 
class TodoResetView(View):
    
    def get(self, request, *args, **kwargs):
        
        Todo.objects.filter(owner=request.user.id).delete()
        return redirect('index')


