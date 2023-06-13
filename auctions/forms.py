from django import forms
from .models import Category

#get all categories in the DB
categories = Category.objects.all()
choice=[]
for cat in categories:
    choice.append((cat.id,cat.name))

#create a django form that corresponds to the Listing model
class newListing(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Listing name', 'class': 'form-control'}), label='')
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Description', 'class': 'form-control'}), label='')
    starting_bid = forms.DecimalField(max_digits=8, decimal_places=2, widget=forms.TextInput(attrs={'placeholder':'Starting bid', 'class': 'form-control'}), label='')
    image = forms.URLField(widget=forms.TextInput(attrs={'placeholder':'Add a url for an image', 'class': 'form-control'}), required=False, label='')
    category = forms.MultipleChoiceField(choices=choice, required=False, widget=forms.ChoiceField, label='')
    category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), choices=choice, required=False, label='')

#create a django form so that users can bid on a listing
class newBid(forms.Form):
    amount = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.TextInput(attrs={'placeholder':'Enter your bid here...', 'class': 'form-control'}), label="")

#create a django form so that users can comment on a listing
class newComment(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter your comment here...', 'class': 'form-control'}), label="")