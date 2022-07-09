from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .secondary_functions import get_box_orders, get_season_orders, get_storages_context
from nais_storage.models import BoxOrder, Storage, SeasonOrder, SeasonItem, Box
from django.conf import settings
from django.db import transaction
import qrcode
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

YANDEX_GEOCODER_API_TOKEN = settings.YANDEX_GEOCODER_API_TOKEN


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return move_to_profile(request)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = LoginForm()
    return render(request, 'account/account_login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'base.html')

@transaction.atomic
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        print("USERFORM", dir(user_form))

        if user_form.is_valid():
            user_raw = dict(request.POST.dict())
            date_of_birth = f"{user_raw['date_of_birth_year']}-{user_raw['date_of_birth_month']}-{user_raw['date_of_birth_day']}"
            new_user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            try:
                validate_password(password, new_user)
            except ValidationError as password_error:
                user_form.add_error("password", password_error)
                return render(request, 'account/register.html', {'user_form': user_form})
            new_user.set_password(password)
            new_user.save()
            profile = Profile.objects.create(user=new_user, first_name=user_raw["first_name"],
                                             last_name=user_raw["last_name"],
                                             date_of_birth=date_of_birth, patronymic=user_raw["patronymic"],
                                             contact_phone=user_raw["contact_phone"],
                                             passport=user_raw["passport"], address=user_raw["address"],
                                             email=user_raw["email"])
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return move_to_profile(request)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user)
        return render(request,
                      'account/edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})


@transaction.atomic
@login_required
def make_box_order(request):
    order_raw = dict(request.POST.lists())
    client = Profile.objects.get(user=request.user)
    storage_raw = order_raw["storage"][0]
    storage_name = storage_raw.split("-")[0].rstrip()
    storage = Storage.objects.get(name=storage_name)
    box = Box.objects.get(size=order_raw["box"][0].split("-")[0].rstrip())
    new_box_order = BoxOrder.objects.create(storage=storage, date_from=order_raw["date_from"][0],
                                        date_to=order_raw["date_to"][0], client=client,
                                        price=box.price, box=box)
    return render(request, "payment.html")


@transaction.atomic
@login_required
def make_season_order(request):
    order_raw = dict(request.POST.lists())
    print("ORDER RAW", order_raw)
    client = Profile.objects.get(user=request.user)
    storage_raw = order_raw["storage"][0]
    storage_name = storage_raw.split("-")[0].rstrip()
    storage = Storage.objects.get(name=storage_name)
    season_item_name = order_raw["season_item"][0]
    season_item = SeasonItem.objects.get(name=season_item_name)
    season_item_price = season_item
    new_season_order = SeasonOrder.objects.create(storage=storage, date_from=order_raw["date_from"][0],
                                        date_to=order_raw["date_to"][0], client=client,
                                        item=season_item, quantity=order_raw["quantity"][0], price=0)
    new_season_order = SeasonOrder.objects.get(id=new_season_order.id)
    new_season_order.annotate_price()
    new_season_order.save()
    return render(request, "payment.html")


@login_required()
def move_to_profile(request):
    profile = Profile.objects.get(user=request.user)
    box_orders = get_box_orders(profile)
    season_orders = get_season_orders(profile)
    boxes = Box.objects.values("price")
    boxes_price = [box["price"] for box in boxes]
    storages = Storage.objects.all()
    storages_context = get_storages_context(storages, profile)
    user_qrcode = qrcode.make(f"{profile.first_name} {profile.last_name} {profile.patronymic} {profile.passport}")
    user_qrcode_path = f"media/user_qr_codes/{request.user}.png"
    user_qrcode.save(user_qrcode_path)
    profile.qr_code = f"user_qr_codes/{request.user}.png"
    profile.save()
    profile = {"first_name": profile.first_name,
               "last_name": profile.last_name,
               "patronymic": profile.patronymic,
               "email": profile.user.email,
               "date_of_birth": profile.date_of_birth,
               "contact_phone": profile.contact_phone,
               "passport": profile.passport,
               "address": profile.address,
               "qr_code": profile.qr_code}
    context = {"profile": profile, "box_orders": box_orders, "season_orders": season_orders,
               "boxes_price": boxes_price, "storages": storages_context}
    return render(request, "profile.html", context=context)


def make_payment(request):
    return render(request, "payment.html")


def show_success_payment(request):
    return HttpResponse("Заказ сделан")
