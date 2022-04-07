from this import d
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name




class Listings(models.Model):
    Title = models.CharField(max_length=64)
    Description = models.CharField(max_length=400)
    StartPrice = models.DecimalField(max_digits=10, decimal_places=2)
    PostedTime = models.DateTimeField(auto_now_add=True)
    Photo = models.URLField(max_length=1000, blank=True, null=True)
    Category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
    Author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    WatchedBy = models.ManyToManyField(User, blank=True, related_name='Watchlist')
    Active = models.BooleanField(default=True)

    def inList(self, user):
        return user.Watchlist.filter(pk=self.pk).exists()

    def numOfBids(self):
        pass

    def currentPrice(self):
        pass

    def winner(self):
        pass
    
    def __str__(self):
        return f"{self.Title}"
    
class Bid(models.Model):
    Listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="Bids")
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Bids")
    Amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.Amount)

class Comment(models.Model):
    Listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="Comments")
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Comments")
    Text = models.CharField(max_length=5000)
    PostedTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)
    





