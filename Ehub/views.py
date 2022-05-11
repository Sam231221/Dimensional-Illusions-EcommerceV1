from .models import *
from Mvfx.models import *
from Msfx.models import *
from Mgraphics.models import *

from django.shortcuts import render, redirect, HttpResponse
import requests
from django.views.generic import View


from django.http import JsonResponse, response
import json              # data = json.loads(request.body)
import datetime

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.contrib.auth.admin import Group

import uuid
# for sending email
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

from .forms import *

# Create your views here.


def Home(request):
    if request.user.is_authenticated:
        getprofile = request.user.profile
        # Imp note:-when payment is done of order a new order is created but no get from database
        order, created = Order.objects.get_or_create(
            profile=getprofile, complete=False)
        purchase, created = PurchasedProduct.objects.get_or_create(
            profile=getprofile, complete=False)

        getfreevfxproducts = FreeVfxProduct.objects.all()
        getpaidvfxproducts = PaidVfxProduct.objects.all()

        getfreesfxproducts = FreeSfxProduct.objects.all()
        getpaidsfxproducts = PaidSfxProduct.objects.all()

    else:
        getfreevfxproducts = FreeVfxProduct.objects.all()
        getpaidvfxproducts = PaidVfxProduct.objects.all()

        getfreesfxproducts = FreeSfxProduct.objects.all()
        getpaidsfxproducts = PaidSfxProduct.objects.all()

        order = {}

    context = {
        'order': order,
        'getfreevfxproducts': getfreevfxproducts,
        'getpaidvfxproducts': getpaidvfxproducts,

        'getfreesfxproducts': getfreesfxproducts,
        'getpaidsfxproducts': getpaidsfxproducts,

    }
    return render(request, 'frontend_base.html', context)


def ContactApi(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        title = request.POST['title']
        content = request.POST['content']
        if len(name) <= 2 and len(title) <= 4 and len(content) <= 9:
            messages.error(request, "Please fill the form correctly")
        else:
            instantcontact = Email(
                name=name, email=email, title=title, content=content)
            instantcontact.save()
            messages.success(
                request, "Your message has been successfully sent")

    return render(request, "E-HUB/contact.html")


def SearchEngine(request):
    if request.user.is_authenticated:
        getprofile = request.user.profile
        order, created = Order.objects.get_or_create(
            profile=getprofile, complete=False)
        TotalCartAmount = order.get_lightiningvfx_total+order.get_energyvfx_total+order.get_muzzleflashes_total+order.get_shockwaves_total+order.get_particles_total+order.get_environmentvfx_total+order.get_debrisandcracksvfx_total+order.get_lightiningsfx_total+order.get_energysfx_total+order.get_environmentalsfx_total+order.get_firesfx_total + \
            order.get_machinerysfx_total+order.get_weaponsfx_total+order.get_fightingsfx_total+order.get_landscapes_total+order.get_characters_total+order.get_opticallens_total + \
            order.get_audiopack_total+order.get_vfxpack_total+order.get_flimtransitionpack_total + \
            order.get_motiongraphicspack_total + \
            order.get_audiospectrum_total+order.get_lyricstemplate_total

    else:
        TotalCartAmount = 0
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}

    query = request.GET['query']
    if len(query) > 78 or len(query) < 3 or len(query) == 0:
      # SPECIAL PACKS
        getfreesoundpacks = SoundPack.objects.none()
        getpaidsoundpacks = SoundPack.objects.none()

        TotalCount = countVfxandSfx+countSpecialPacksAndOthers+countGraphicsElements

    else:
        getpaidsoundpacks = SoundPack.objects.filter(
            name__icontains=query, type="PAID")
        getfreesoundpacks = SoundPack.objects.filter(
            name__icontains=query, type="FREE")

    # GRAPHICS ELEMENT
        getfreelandscapes = Landscapes.objects.filter(
            name__icontains=query, type="FREE")
        getpaidlandscapes = Landscapes.objects.filter(
            name__icontains=query, type="PAID")

        getfreecharacters = Characters.objects.filter(
            name__icontains=query, type="FREE")
        getpaidcharacters = Characters.objects.filter(
            name__icontains=query, type="PAID")

        TotalCount = countVfxandSfx+countSpecialPacksAndOthers+countGraphicsElements
    print(TotalCount)
    print(countVfxandSfx)
    print(countSpecialPacksAndOthers)
    params = {
        'countVfxandSfx': countVfxandSfx,

        'getpaidDebrisAndCrackVfx': getpaidDebrisAndCrackVfx,

        'query': query,
        'TotalCartAmount': TotalCartAmount,

    }
    return render(request, 'search.html', params)


def YourCart(request):
    if request.user.is_authenticated:
        getprofile = request.user.profile
        order, created = Order.objects.get_or_create(
            profile=getprofile, complete=False)

        # OTHERS
        rendervfxpaidproducts = order.orderpaidvfxproduct_set.all()
        rendersfxpaidproducts = order.orderpaidsfxproduct_set.all()
        rendergraphicspaidproducts = order.orderpaidgraphicsproduct_set.all()

    else:
        rendersfxpaidproducts = {}
        rendergraphicspaidproducts = {}
        rendervfxpaidproducts = {}

        order = {}

    context = {
        'rendervfxpaidproducts': rendervfxpaidproducts,
        'rendersfxpaidproducts': rendersfxpaidproducts,
        'rendergraphicspaidproducts': rendergraphicspaidproducts,
        'order': order,


    }
    # for displaying no of item in red circle of cart icon
    return render(request, 'E-HUB/cart.html', context)


def getcoupon(request, getcode):
    try:
        coupon = DiscountCoupon.objects.get(discountcode=getcode)
        return coupon
    except:
        messages.ERROR('Coupon doesnot exist')
        return redirect('Ehub:Checkout')


@login_required(login_url='login')
def addcouponcode(request):
    if request.user.is_authenticated:
        print('hello')
        if request.method == "POST":
            getcode = request.POST['discountcode']
            getprofile = request.user.profile
            # we are setting the customer value on authebnticating the user
            order, created = Order.objects.get_or_create(
                profile=getprofile, complete=False)
            order.discountcoupon = getcoupon(request, getcode)
            order.save()
            return redirect('Ehub:Checkout')


def Checkout(request):
    if request.user.is_authenticated:
        getprofile = request.user.profile
        order, created = Order.objects.get_or_create(
            profile=getprofile, complete=False)

        rendervfxpaidproducts = order.orderpaidvfxproduct_set.all()
        rendersfxpaidproducts = order.orderpaidsfxproduct_set.all()
        rendergraphicspaidproducts = order.orderpaidgraphicsproduct_set.all()
    else:
        rendersfxpaidproducts = {}
        rendergraphicspaidproducts = {}
        rendervfxpaidproducts = {}
        order = {}

    context = {
        # VFX
        'rendervfxpaidproducts': rendervfxpaidproducts,
        'rendersfxpaidproducts': rendersfxpaidproducts,
        'rendergraphicspaidproducts': rendergraphicspaidproducts,
        'order': order,

    }

    return render(request, 'E-HUB/checkout.html', context)


class KhaltiVerifyView(View):

    def get(self, request, *args, **kwargs):
        print('Initaiting Khalti Verificatiion...')
        transaction_id = datetime.datetime.now().timestamp()

        token = request.GET.get("token")
        amount = request.GET.get("amount")
        o_id = request.GET.get("order_id")
        getprofile = request.user.profile
        print(o_id)
        print(token, amount, o_id)

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_de01b0c1f02b48759df0953a0dcfc8f0"
        }

        order = Order.objects.get(profile=getprofile, complete=False)
        purchase = PurchasedProduct.objects.get(
            profile=getprofile, complete=False)

        orderpaidvfxproduct = OrderPaidVfxProduct.objects.filter(
            profile=getprofile, complete=False)
        orderpaidsfxproduct = OrderPaidSfxProduct.objects.filter(
            profile=getprofile, complete=False)

        response = requests.post(
            url, payload, headers=headers)  # sending data to url
        resp_dict = response.json()
        print(resp_dict.get('idx'))

        total = amount
        if resp_dict.get("idx"):
            if total == amount:
                success = True
                order.complete = True
                order.transaction_id = transaction_id
                order.save()

                purchase.complete = True
                purchase.transaction_id = transaction_id
                purchase.save()

            # VFX
                for x in orderpaidvfxproduct:
                    if total == float(order.grand_totalamount):
                        x.complete = True
                    x.save()

            # SFX
                for x in orderpaidsfxproduct:
                    if total == float(order.grand_totalamount):
                        x.complete = True
                    x.save()

            else:
                success = False
            data = {
                "success": success
            }
            return JsonResponse(data)


def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        getprofile = request.user.profile
        total = float(data['form']['total'])
        # For clearing Cart
        order = Order.objects.get(profile=getprofile, complete=False)

        # For downloading items that are completed of particular Customer
        purchase = PurchasedProduct.objects.get(
            profile=getprofile, complete=False)

        order.transaction_id = transaction_id
        purchase.transaction_id = transaction_id

        if total == float(order.grand_totalamount):
            order.complete = True
        order.save()

        if purchase.complete == False:
            if purchase.profile == getprofile:
                purchase.complete = True
            purchase.save()

        # When the payment is completed,set all the order items to True of the logged in user only not others.
        # Note,We dont need to mention publisher_Id
        orderpaidvfxproduct = OrderPaidVfxProduct.objects.filter(
            profile=getprofile, complete=False)
        orderpaidsfxproduct = OrderPaidSfxProduct.objects.filter(
            profile=getprofile, complete=False)
        orderpaidgraphicsproduct = OrderPaidGraphicsProduct.objects.filter(
            profile=getprofile, complete=False)

  # VFX
        for x in orderpaidvfxproduct:
            if total == float(order.grand_totalamount):
                x.complete = True
            x.save()

  # SFX
        for x in orderpaidsfxproduct:
            if total == float(order.grand_totalamount):
                x.complete = True
            x.save()

  # GRAPHICS
        for x in orderpaidgraphicsproduct:
            if total == float(order.grand_totalamount):
                x.complete = True
            x.save()

    else:
        print('User not logged in')

    return JsonResponse('Payment Completed', safe=False)


def PurchasedProducts(request):
    if request.user.is_authenticated:
        getprofile = request.user.profile

        # If the order is not completed and customer visit downloadpage send empty dictionary so error wouldnot generate
        # Vfx
        rendervfxpaidproducts = {}
        rendersfxpaidproducts = {}
        rendergraphicspaidproducts = {}

        for i in PurchasedProduct.objects.filter(profile=getprofile, complete=True):
            # OTHERS
            rendervfxpaidproducts = i.orderpaidvfxproduct_set.all()
            rendersfxpaidproducts = i.orderpaidsfxproduct_set.all()
            rendergraphicspaidproducts = i.orderpaidgraphicsproduct_set.all()

        context = {
            # VFX
            'rendervfxpaidproducts': rendervfxpaidproducts,
            # SFX
            'rendersfxpaidproducts': rendersfxpaidproducts,
            # GRAPHICS
            'rendergraphicspaidproducts': rendergraphicspaidproducts,
        }

    else:
        rendervfxpaidproducts = {}
        rendersfxpaidproducts = {}
        rendergraphicspaidproducts = {}

        context = {
            # VFX
            'rendervfxpaidproducts': rendervfxpaidproducts,
            # SFX
            'rendersfxpaidproducts': rendersfxpaidproducts,
            # GRAPHICS
            'rendergraphicspaidproducts': rendergraphicspaidproducts,
        }

    return render(request, 'E-HUB/downloadpage.html', context)


# REGISTRATION AND LOGIN SECTION
def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request, 'User not found.')
            return redirect('Ehub:login-user')

        profile_obj = Profile.objects.filter(username=user_obj).first()

        if not profile_obj.is_verified:
            messages.error(
                request, 'Your account is not verified yet .Check your mail.')
            return redirect('Ehub:login-user')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Wrong password.')
            return redirect('Ehub:login-user')

        login(request, user)
        return redirect('Ehub:home')

    return render(request, 'Sign-Up/login.html')


def logoutUser(request):
    logout(request)
    return redirect('Ehub:home')


def registeruser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        try:
            # checking if the new one is using the same username or email
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username is taken.')
                return redirect('register')

            if User.objects.filter(email=email).first():
                messages.error(request, 'Email is taken.')
                return redirect('register')

            if password1 == password2:
                # create user  and saving it
                user_obj = User(username=username, email=email)
                user_obj.set_password(password1)
                user_obj.save()

                # When User clicks on SignIn
                # 1.we are generating an token and creating a profile based on the auth_token that was generated.
                # 2.sending the email through a function with email and auth_token as a paramter
                auth_token = str(uuid.uuid4())  # converting to string
                profile_obj = Profile.objects.create(
                    username=user_obj, email=email, auth_token=auth_token)
                profile_obj.save()

                # Now, We are sending the auth_token that was generated by uuid to gmail.We make a function.
                send_mail_after_registration(
                    email, auth_token)  # function call
                return redirect('token_send')
            else:
                messages.error(
                    request, 'Sorry,Password1 and Password2 did not match.')

        except Exception as e:
            print(e)

    return render(request, 'Sign-Up/registration.html')


def success(request):
    return render(request, 'Sign-Up/success.html')


def token_send(request):
    return render(request, 'Sign-Up/token_send.html')


def verify(request, auth_token):
    try:
        # checking if the profile exist through auth_token
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:  # if profile exists

            if profile_obj.is_verified:  # If the profile that exists has already been verified return User to login page
                messages.success(request, 'Your account is already verified.')
                return redirect('login')

            # If profile exists set the is_verified to True, save it and redirect to login page
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')

        # if the profile with the passed auth_token doesn;t exist throw error
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('home')


def error_page(request):
    return render(request, 'Sign-Up/error.html')


def send_mail_after_registration(email, token):
    subject = 'Your DI account need to be verified.'
    #message = f'Dear Sir/Madam paste the link to verify your DI account http://dimensionalillusions.herokuapp.com/account/verify/{token}'
    message = f'Dear Sir/Madam paste the link to verify your DI account http://127.0.0.1:8000/account/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]  # from args
    # a function that sends a email to gmail
    send_mail(subject, message, email_from, recipient_list)
