from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import UserPwdForm
from . models import Profile
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        user = authenticate(username=uname, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, "Username and Password is Invalid")

    return render(request, 'Users/login.html')



@login_required
def password_change(request):
    if request.method == 'POST':
        form = UserPwdForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.DEBUG(request, f'Your password has successfully updated, please login.')
            return redirect('Login')

    else:
        form = UserPwdForm(request.user)

    return render(request, 'Users/password_change.html', {'form': form})


def Register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        cnumber = request.POST.get('cnumber')
        birthday = request.POST.get('birthday')
        address = request.POST.get('address')
        password = request.POST.get('password')
        
        ph = Profile.objects.filter(phoneno=cnumber)
        mail = User.objects.filter(email=email)

        if ph.exists():
            messages.warning(request, f'Phone number already exists, please provide your personal phone number')
        elif mail.exists():
            messages.warning(request, f'Email ID already exists, please provide your personal Email address')
        elif not (ph.exists() and mail.exists()):
            userdetail = User.objects.create(username=email, first_name=fname, last_name=lname, email=email)
            userdetail.set_password(password)
            userdetail.save()
            userprofile = Profile.objects.create(user=userdetail, BirthDate=birthday, phoneno=cnumber,
                                                   address=address, Department='public')
            userprofile.save()
            #send_mail('Registratoin', 'Thank you for registering to Job portal(Trial) Version', settings.EMAIL_HOST_USER, [email], fail_silently=False, )
            messages.DEBUG(request,
                             'Account created successfully for "{}" Please login and complete your profile'.format(
                                 email))
            return redirect('Login')
    return render(request, 'Users/Register.html')



@login_required
def Profile_Update(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        cnumber = request.POST.get('cnumber')
        birthday = request.POST.get('birthday')
        address = request.POST.get('address')
        qual = request.POST.get('Qualification')

        if request.FILES.__contains__('myprofile'):
            myprofile = request.FILES['myprofile']
            fs = FileSystemStorage()
            fs.save(myprofile.name, myprofile)
        else:
            myprofile = request.user.profile.profile_pic

        if birthday:
            pass
        else:
            birthday = request.user.profile.BirthDate

        mail = User.objects.filter(email=email)
        ph = Profile.objects.filter(phoneno=cnumber)

        if mail.exists() and email != request.user.email:
            messages.warning(request, f'Email ID already exists, please provide your official Email address')

        elif ph.exists() and cnumber != request.user.profile.phoneno:
            messages.warning(request, f'Phone number already exists, please provide your personal phone number')
        
        else:
            userupdate = request.user
            userupdate.email = email
            userupdate.username = email

            profileupdate = Profile.objects.get(user=request.user)
            if myprofile:
                profileupdate.profile_pic = myprofile

            profileupdate.phoneno = cnumber
            profileupdate.address = address
            profileupdate.BirthDate = birthday

            if qual:
                profileupdate.Qualification = qual

            userupdate.save()
            profileupdate.save()
            messages.warning(request, f'Profile Details updated successfully')
            return redirect('profile')



    return render(request, 'Users/Profile.html')