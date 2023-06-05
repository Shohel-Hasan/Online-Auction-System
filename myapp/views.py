from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Auctions, Bid
from django.utils import timezone
from .forms import BidForm, UserCreate, AuctionForm, ProfileEdit
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# Create your views here.
def index(request):
    query = Auctions.objects.filter(end_time__gt=timezone.now()).order_by('-start_time')
    context = {
        'auctions': query
    }
    if query.count() < 1:
        context['empty'] = True
    return render(request, template_name='index.html', context=context)


def all_auction(request):
    query = Auctions.objects.all().order_by('-start_time')
    context = {
        'all_auctions': query
    }
    return render(request, template_name='auctions.html', context=context)


@login_required(login_url='login')
def bid(request, id):
    auction = get_object_or_404(Auctions, id=id)
    min_amount = auction.min_amount
    if request.method == "POST":
        form = BidForm(request.POST, user=request.user, auction=auction)
        if form.is_valid():
            if min_amount > form.cleaned_data['amount']:
                messages.warning(request, f'Minimum Bid Amount: {min_amount}')
            else:
                form.save()
                return redirect('all_bids', id=id)
    else:
        form = BidForm(request.POST, user=request.user, auction=auction, initial={'amount': min_amount})
    context = {
        'forms': form,
        'auction': auction
    }
    return render(request, template_name='bid.html', context=context)

def all_bids(request, id):
    all_bids = Bid.objects.filter(auction=id).order_by('-amount')
    top_bid = all_bids.first()
    context = {
        'bids': all_bids,
        'top_bid': top_bid,
        'auction': id
        }
    if all_bids.count() > 0:
        context['image'] = all_bids[0].auction.image.url

    return render(request, template_name='all_bids.html', context=context)


def login_user(request):
    if request.method == "POST":
        uname = request.POST['username']
        pasw = request.POST['password']
        user = authenticate(request, username=uname, password=pasw)
        if user is not None:
            login(request, user)
            messages.success(request, f"Successfully Login As {request.user}")
            return redirect('index')
        else:
            messages.warning(request, "Wrong Credentials!")

    return render(request, template_name='login.html')

def user_logout(request):
    logout(request)
    messages.info(request, "Logout!")
    return redirect('index')

def CreateUser(request):
    if request.method == "POST":
        forms = UserCreate(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Registration Succesfull!")
            return redirect('login')

    else:
        forms = UserCreate()
    context = {
        'forms': forms
    }
    return render(request, template_name='user_create.html', context=context)

def create(request):
    if request.method == "POST":
        forms = AuctionForm(request.POST or None, request.FILES or None, user=request.user)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Auction Created!")
            return redirect('index')
    else:
        forms = AuctionForm(request.POST or None, request.FILES or None, user=request.user)
    context = {
        'forms': forms
    }
    return render(request, template_name='create.html', context=context)


def profile(request, user):
    user = User.objects.get(username=user)
    context = {
        'user': user
    }
    return render(request, template_name='profile.html', context=context)

def profile_edit(request, user):
    user = User.objects.get(username=user)
    forms = ProfileEdit(user=user)
    if request.method == "POST":
        forms = ProfileEdit(request.POST, request.FILES, user=user)
        if forms.is_valid():
            forms.save()
            return redirect('profile', user=user)

    context = {
        'forms': forms
    }
    return render(request, template_name='profile_edit.html', context=context)
