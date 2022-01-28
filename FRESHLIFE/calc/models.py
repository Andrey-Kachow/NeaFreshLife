from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint


class Activity(models.Model):
    name = models.CharField(max_length=45)
    epkgh = models.FloatField()

    def __str__(self):
        return self.name


class Latest_inputs(models.Model):  # additional information related to user
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    weight = models.FloatField(null=True)
    calories = models.FloatField(null=True)

    @receiver(post_save, sender=User)
    def create_latest_inputs(sender, instance, created, **kwargs):
        if created:
            Latest_inputs.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_latest_inputs(sender, instance, **kwargs):
        instance.latest_inputs.save()

    def __str__(self):
        return "{}'s inputs".format(self.user.username)

    @staticmethod  # Just a temporary shit, to get random number for static urls
    def random_v():  # remove in production
        return str(randint(0, 2048))

