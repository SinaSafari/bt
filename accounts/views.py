from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required

def register(request): #If POST, then register user and redirect, otherwise render template
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check for new username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'نام کابری قبلا ثبت شده است')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'ایمیل در سامانه موجود است')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(
                        username=username, 
                        password=password, 
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                    )
                    #Login after register
                    #auth.login(request, user)
                    #messages.success(request, 'You are now logged in')
                    #return redirect('index')
                    
                    #redirect to login page to login for first time
                    user.save()
                    messages.success(request, 'ثبت نام با موفقیت همراه بود. لطفا وارد شوید')
                    return redirect('login')
        else:
            messages.error(request, 'رمز های وارد شده منطبق نیستند')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'شما با موفقیت وارد شدید')
            return redirect('dashboard')
        else:
            messages.error(request, 'مشخصات ورودی صحیح نیست')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'شما با موفقیت خارج شدید')
        return redirect('index')


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')
    
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    
    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)