from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from contacts.models import Contact


# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")

            return redirect('dashboard')

        else:
            messages.error(request, "Invalid login")
            return redirect('login')

    else:
        return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            # check username
            if User.objects.filter(username=user_name).exists():
                messages.error(request, "Username is already exists")
                return redirect("register")

            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Username is already exists")
                    return redirect("register")
                else:
                    # looks good
                    user = User.objects.create_user(username=user_name, email=email, password=password,
                                                    first_name=first_name, last_name=last_name)

                    user.save()
                    messages.success(request, "You are now registered and can log in")
                    return redirect('login')

        else:
            messages.error(request, "password does not match")
            return redirect("register")

    else:
        return render(request, 'accounts/register.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are now logout")
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    print(context)
    return render(request, 'accounts/dashboard.html', context)
