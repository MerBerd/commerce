from django.contrib import admin
from .models import Listings, Comment, Bids, Category

# Register your models here.
admin.site.register(Listings)
admin.site.register(Comment)
admin.site.register(Bids)
admin.site.register(Category)

