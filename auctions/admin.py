from django.contrib import admin
from .models import Listings, Category, Bid, Comment

# Register your models here.
admin.site.register(Listings)

admin.site.register(Category)

admin.site.register(Bid)

admin.site.register(Comment)



