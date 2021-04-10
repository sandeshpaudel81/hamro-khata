from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(default='default-avatar.png', upload_to="profile-pic/", null=True, blank=True)
    
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    # try:
    #     instance.profile.save()
    # except ObjectDoesNotExist:
    #     Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Party(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=10, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def amount(self):
        toPay = Transaction.objects.filter(action='sub', party=self)
        toGet = Transaction.objects.filter(action='add', party=self)
        totalToPay = 0
        totalToGet = 0
        for val in toPay:
            totalToPay = totalToPay + val.amount
        for val in toGet:
            totalToGet = totalToGet + val.amount
        total = int(totalToGet - totalToPay)
        return total


class Transaction(models.Model):
    ACTION_CHOICES = [
        ('add', '+'),
        ('sub', '-'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    description = models.CharField(max_length=255)
    action = models.CharField(max_length=3, choices=ACTION_CHOICES)
    datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return '%s, %s, %s %s' % (self.user.username, self.party.name, self.amount, self.datetime)