from django.shortcuts import render
from django.views import View
from .forms import UserRegisterForm, VerifyCodeForm
from random import randint
from utls import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.


class UserRegisterView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # generate random code
            random_code = randint(1000, 9999)

            # send otp code to user phone number
            send_otp_code(cd['phone'], random_code)
            OtpCode.objects.create(
                phone_number=cd['phone'],
                code=random_code
            )

            # create a session to save user info
            request.session['user_register_info'] = {
                'phone_number': cd['phone'],
                'email': cd['email'],
                'full_name': cd['full_name'],
                'password': cd['password'],
            }

            # send message to user
            messages.success(
                request, 'We sent you an activation code', 'success')

            return redirect('accounts:verify_code')
        return render(request, 'accounts/register.html', {'form': form})
        # return redirect('home:home')


class VerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/verify_code.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_register_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if code_instance.code == cd['code']:
                # create user 
                User.objects.create_user(
                    phone_number=user_session['phone_number'],
                    email=user_session['email'],
                    full_name=user_session['full_name'],
                    password=user_session['password']
                )
                code_instance.delete()
                messages.success(
                    request, 'Your account has been created successfully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'The entered code is incorrect', 'danger')
                return redirect('accounts:verify_code')
            
        return render(request, 'accounts/verify_code.html', {'form': form})    

        
