from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

def userlogin(request):  
    if 'user' in request.session:
        return redirect('home')
    if 'a_user' in request.session:
        return redirect('admin')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:                
                messages.success(request,("You Are Unauthorized"))  
                return redirect('login')
            else:
                request.session['user'] = username
                auth.login(request, user)           
                return redirect('home')  
               
        else:
            messages.success(request,("Enter  Username and Password Correctly...."))  
            return redirect('login')  
        # Return an 'invalid login' error message.
       
    else:
        return render(request,'signup/login.html')

        

def usersignup(request): 

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
                return redirect('signup')

            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exist')
                return redirect('signup')
        
            else:
                if username == '' and password1 == '' :
                    messages.info(request,'Enter All Fields to Continue')
                    return redirect ('signup')
                else:

                    user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                    user.save()
                    messages.info(request,'User Created Sucessfully')
                    return redirect( 'login' ) 

        else:
            messages.info(request,'Password Not Matching')
            return redirect('signup')
        
        
    return render(request,'signup/signnup.html')    


def home(request):
    if 'user' in request.session:
        return render(request,'signup/home.html')           
    else:
        return redirect('login')


def userlogout(request):
    if 'user' in request.session:
        request.session.flush()      
    logout(request)
    messages.info(request,'User Logout Sucessfully')
    return redirect( 'login' )

def ihome(request):
    return render(request,'signup/ihome.html')
        

# def dashboard(request):
#     users = User.objects.all()
#     context = {'users':users}
    

#     return render(request,'signup/dashboard.html',context)          

# def userlogout(request):
#     logout(request)
#     return redirect('login')    