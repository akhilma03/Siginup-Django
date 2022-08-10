from ast import Not
from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from . forms import UserForm
from django.db.models import Q


# Create your views here.
def useradmin(request):
    if 'a_user' in request.session:
        return redirect('main')
    
    if 'user' in request.session:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username , password = password )

        if user is not None:
           if user.is_superuser:
                request.session['a_user']=username
                login(request,user)
                return redirect ('main')
        else:
            messages.info(request,'Usernanme or Password is Incorrect')
            return redirect('admin')

    else :
        return render(request,'adminz/admin.html')

   
   


def userlogout(request):
    if 'a_user' in request.session:
        request.session.flush()
    logout(request)
    return redirect('admin')


 

def dashboard(request):  
    if 'a_user' in request.session:       
        if 'q' in request.GET:
            q = request.GET['q']
            # user = User.object.filter(first_name__icontains= q)
            multiple_q = Q(Q(first_name__icontains=q) | Q(last_name__icontains=q))
            user = User.objects.filter(multiple_q)
        else:
            user = User.objects.all()
            # context = {
            # 'users':user
            #      }        
        return render(request,'adminz/dashboard.html', {'users':user})

    # else:
    #     return redirect('admin')

def siginn(request):
    if 'a_user' in request.session:
        return redirect('main')
    if 'user' in request.session:
        return redirect('login')
    if request.method == 'POST':
        first_name = request.POST['first_name'] 
        last_name = request.POST['last_name'] 
        username = request.POST['username'] 
        email = request.POST['email'] 
        password1 = request.POST['password1'] 
        password2 = request.POST['password2'] 


        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exist')
                return redirect('signup2')

            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exist')
                return redirect('signup2')
        
            else:
                if username == '' and password1 == '' :
                    messages.info(request,'Enter All Fields to Continue')
                    return redirect ('signup2')

                else:

                    user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                    user.save()              
                    messages.info(request,'User Added Sucessfully')

        else:
            messages.info(request,'Password Not Matching')
            return redirect('signup2')
        return redirect( 'main' ) 

    return render(request,'adminz/signinn.html')     


def destroy(request, id):

    if 'a_user' in request.session:
        user = User.objects.get(id=id)  
        user.delete()  
        return redirect('main')

    else:   
        return redirect('main')         
        
   
      
# @login_required(login_url='admin')
def update(request, id):  
    if 'a_user' in request.session: 
        try:
            user = User.objects.get(id=id)
            form=UserForm (instance=user)
            if request.method == 'POST':
                form=UserForm(request.POST,instance=user)
                if form.is_valid():
                    form.save() 
                    return redirect('main')
            context={'forms':form}
            return render (request,'adminz/update.html',context)
        except:
            messages.info(request,'User Not Exist')
            return redirect('main')
    else:
        return redirect('admin')



    