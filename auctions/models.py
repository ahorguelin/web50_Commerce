from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
     #referencing Listing model by string name so that it can be defined later in the file https://docs.djangoproject.com/en/3.2/ref/models/fields/#manytomanyfield
     watchlist = models.ManyToManyField('Listing', blank=True, related_name='user_watchlist')


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"Category name: {self.name}"
    

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listing")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_bought_items", null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="category_listing", null=True, blank=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    img = models.URLField(max_length=255, blank=True)
    active = models.BooleanField(default=None)

    def __str__(self):
        return f"Listing name: {self.title} owned by {self.owner}]"
    

class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid amount: {self.amount} on {self.listing}]"


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    date = models.DateTimeField(auto_now_add=True)
