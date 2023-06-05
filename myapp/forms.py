from django import forms
from .models import Auctions, Bid, Profile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BidForm(forms.ModelForm):
    amount = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Bid
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.auction = kwargs.pop('auction')
        super().__init__(*args, **kwargs)


    def save(self, commit=False):
        amount = self.cleaned_data['amount']
        try:
            bid = Bid(user=self.user, auction=self.auction, amount=amount)
            bid.save()
        except Bid.DoesNotExist:
            pass

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        if Bid.objects.filter(auction=self.auction, amount=amount).exists():
            raise ValidationError("Another Bid of same amount already exists")
        return cleaned_data

class UserCreate(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auctions
        fields = ['name', 'desc', 'image', 'min_amount']

    def __init__(self, *args, **kwargs):
        self.username = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['desc'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['min_amount'].widget.attrs['class'] = 'form-control mb-2'

    def save(self, commit=True):
        self.name = self.cleaned_data['name']
        self.desc = self.cleaned_data['desc']
        self.img = self.cleaned_data['image']
        self.min_am = self.cleaned_data['min_amount']
        try:
            auction = Auctions(user=self.username, name=self.name, desc=self.desc, image=self.img, min_amount=self.min_am)
            auction.save()
        except Auctions.DoesNotExist:
            auction = Auctions.objects.create(user=self.username, name=self.name, desc=self.desc, image=self.img, min_amount=self.min_am)
        return auction


class ProfileEdit(forms.Form):
    user = forms.CharField(required=False, widget=forms.HiddenInput())
    first_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class':'form-control'}))
    designation = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    about = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}))
    facebook = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    instagram = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    linkedIn = forms.URLField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(required=False)


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = self.user
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email
        try:
            self.fields['designation'].initial = self.user.profile.designation
            self.fields['about'].initial = self.user.profile.about
            self.fields['facebook'].initial = self.user.profile.fb
            self.fields['instagram'].initial = self.user.profile.ins
            self.fields['linkedIn'].initial = self.user.profile.linkedIn
            self.fields['image'].initial = self.user.profile.image
        except:
            pass


    def save(self):
        self.first_name = self.cleaned_data['first_name']
        self.last_name = self.cleaned_data['last_name']
        self.email = self.cleaned_data['email']
        self.designation = self.cleaned_data['designation']
        self.about = self.cleaned_data['about']
        self.facebook = self.cleaned_data['facebook']
        self.instagram = self.cleaned_data['instagram']
        self.linkedIn = self.cleaned_data['linkedIn']
        self.image = self.cleaned_data.get('image')
        try:
            user = User.objects.get(username=self.user.username)
            user.first_name = self.first_name
            user.last_name = self.last_name
            user.email = self.email
            user.save()

            profile = Profile.objects.get(user=user)
            profile.designation = self.designation
            profile.about = self.about
            profile.fb = self.facebook
            profile.linkedin = self.linkedIn
            profile.ins = self.instagram
            profile.image = self.image
            profile.save()
        except Profile.DoesNotExist:
            profile = Profile(user=user, about=self.about, designation = self.designation, fb = self.facebook, linkedIn = self.linkedIn,
                        ins = self.instagram, image = self.image )
            profile.save()

        return user

