from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="newListing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlistChange/<int:listing_id>", views.listingChange, name="listingChange"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("removeWatchlist/<int:listing_id>", views.removeWatchlist, name="removeWatchlist")
]
