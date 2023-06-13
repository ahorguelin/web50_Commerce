# web50_Commerce
My submission of the second project in Web 50 on edX. Project brief [here](https://cs50.harvard.edu/web/2020/projects/2/commerce/).

## Features

This web app is a basic recreation of a bidding website such as Ebay. Users can create listing, comment on them, bid on listing and win an auction if they are the highest bidder. 

### Data model

All of the data model was created using the models class from Django.

1. Listings: allows users to create listing records with an image, a starting price, a name, a category and a description.
2. Bids: records bidding made by users on listing. Each bid is related to a User, and a listing. Bidding date is also automatically generated upon record creation.
3. Comments: allows user to comment on listings if they are authenticated. Comments are related to users and to listings. Datetime field is automatically generated on record creation.
4. User: basic user model from Django was used. An additional field 'watchlist' was added so that Users can add listing to their watchlist and reference it in the future.

### Listing creation

This feature allows user to create a listing with all the information mentionned in the Model part. The listing creation form was created using Django Forms class. Data validity is checked on both the frond and the back-end. 

### Listing page

Clicking on any listing will redirect users to a specific page for this listing. From here, users will be able to see all information related to the listing, the highest bid, as well as the comments. If users are the listing owners, they have the possibility to close it. 

### Biding

From any open listing pages, users can bid on the listing as long as their bid is higher than the previous highest bid. 

### Comments

Users can comment on a listing. Comments will be displayed on the bottom page of the listing from most recent to oldest. 

### Watchlist

From a listing page, users can add the item to their watchlist. They will then have the possibility to check their watchlist which will display all open listings that were watchlisted.

### Categories

Listing can optionaly have a category. Users can use those categories to browse by categories and only be shown the listing that have this category.

### Register, login, logout

Implementation already made in the distribution code of the project. 

### Front-end

Front-end created HTML templates, Jinja and Bootstrap.
