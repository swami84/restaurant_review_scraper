Google Maps Restaurant Review Scraper
=====================================

###  

Description:
------------

This is a web scraper to scrape restaurant reviews from Google Maps for restaurants
in high foot traffic census block groups

###  Steps

1.  Create a Google Places API using
    https://console.cloud.google.com/home/dashboard

2.  Write the api_key to a json (goog_api_keys: 'YOUR_API_KEY') and name it as
    `config.json` in the config folder

3.  Download the webdriver for Chrome ensuring the same version as current
    Chrome installation on your OS (I use Windows)

4.  Run the Review [Scraper
    Notebook](https://nbviewer.org/github/swami84/Google-Maps-Review-Scraper/blob/main/notebooks/Review%20Scraper.ipynb)

###  Data

- Restaurant data is acquired based on census block group foot traffic

-   Google Places API request requires location data (lat, lng) and radius of
    search. I have assumed that Census Block Group (CBG) are circular and calculated radius from the
    area of CBG (available)

-   Output data includes the Census Block Group (restaurants within radius of
    search), Restaurant Attributes (Restaurant type, Caption, Keywords) and
    Restaurant Reviews (User ID, Name, \# of Reviews)
    
    -   Raw reviews can be downloaded from https://drive.google.com/drive/folders/14Oz64knRQ8gE9fF4_FXrMmattQ6S11E3?usp=sharing. Please send an email to swami.me@gmail.com to request access
    -   Compiled CBGs and restaurant attributes can be found in `/data/output/` folder
    
    



