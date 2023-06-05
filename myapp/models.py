from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save

# Create your models here.
class Auctions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, )
    image = models.ImageField(upload_to='images')
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, default=00)

    def save(self, *args, **kwargs):
        self.end_time = timezone.now() + timezone.timedelta(minutes=120)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def remain_time(self):
        rtime = self.end_time - timezone.now()
        minutes = rtime.seconds // 60
        seconds = rtime.seconds % 60
        return str(minutes) + ' minutes ' + str(seconds) + ' seconds'

    class Meta:
        verbose_name_plural = 'Auctions'


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='winner_user')

    def __str__(self):
        return self.user.username + ' ' + self.auction.name + ' ' + str(self.amount)

    def save(self, *args, **kwargs):
        existing_bid = Bid.objects.filter(auction=self.auction)
        if existing_bid.exists():
            existing_bid_amount = existing_bid.order_by('-amount').first()
            if self.amount > existing_bid_amount.amount:
                self.winner = self.user
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Bid'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=50, blank=True)
    about = models.TextField(blank=True)
    fb = models.URLField(blank=True)
    linkedIn = models.URLField(blank=True)
    ins = models.URLField(blank=True)
    google = models.URLField(blank=True)
    image = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username