from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.create_listing, name="new"),
    path("listing/<str:listing_name>", views.view_listing, name="view_listing"),
    path("watchlist/<str:listing_name>", views.toggle_watchlist, name="toggle_watchlist"),
    path("<str:username>/watchlist", views.view_watchlist, name="view_watchlist"),
    path("categories", views.browse_categories, name="browse_categories"),
    path("<str:category_name>/listings", views.category_listings, name="category_listings"),
    path("bid/<str:listing_name>", views.bid, name="bid"),
    path("close/<str:listing_name>", views.close_listing, name="close"),
    path("comment/<str:listing_name>", views.comment_listing, name="comment")
]
