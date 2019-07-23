# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import requests
import json
from collections import namedtuple
import unicodedata
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import time
import re
from objdict import ObjDict
from datetime import datetime
from psycopg2 import sql
from django.utils.encoding import smart_str, smart_unicode
import psycopg2

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3831.602 Safari/537.36',
    'Cookie': 'datr=HpntWUrc0QawJrdvP6Ynw7kN; sb=W5ntWROUmZlYjysKseKep_91; pl=n; dpr=1.5; c_user=100009855792024; xs=35%3AUXgh6AceOVeGvw%3A2%3A1508743515%3A20772%3A8699; fr=09kK2tX9Vuz0OSrn7.AWUcfLFMyKAy2sEScE_co9LLnUk.BZ7Zke.Q_.FpM.0.0.BaU5YP.AWUFt5Ae; wd=1280x561; act=1515430580572%2F1; presence=EDvF3EtimeF1515430601EuserFA21B09855792024A2EstateFDutF1515430601519CEchFDp_5f1B09855792024F15CC'
}
class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)

def index(request):
    res = apiCall(request)
    return HttpResponse('complete')

def repl(m):
    if m.group(1) in ('(', ',') or m.group(2) in (',', ')'):
        return m.group(0)
    return m.group(1) + "''" + m.group(2)

def setupDB(db,mode):
    conn = None
    if mode == 1:
        inSQL = "INSERT INTO Location (locationID,address,longitude,latitude)VALUES('"+str(db.locationID)+"','"+db.address+"','"+str(db.longitude)+"','"+str(db.latitude)+"');"
    elif mode == 2:
        inSQL = "INSERT INTO Cuisine (cuisineType,restaurantID)VALUES('"+db.cuisineType+"','"+db.restaurantID+"');"
    elif mode == 3:
        inSQL = "INSERT INTO Photo (pictureURL,restaurantID)VALUES('"+db.pictureURL+"','"+db.restaurantID+"');"
    elif mode == 4:
        inSQL = "INSERT INTO Restaurant (restaurantID,priceRange,website,phoneNumber,locationID)VALUES('"+db.restaurantID+"','"+db.priceRange+"','"+db.website+"','"+db.phoneNumber+"','"+str(db.locationID)+"');"
    elif mode == 5:
        inSQL = "INSERT INTO RestaurantFeature (featureName,restaurantID,description)VALUES('"+db.featureName+"','"+db.restaurantID+"','"+db.description+"');"
    elif mode == 6:
        inSQL = "INSERT INTO RestaurantRating (scale,restaurantID,overallRating,source)VALUES('"+db.scale+"','"+db.restaurantID+"','"+str(db.overallRating)+"','"+db.source+"');"
    elif mode == 7:
        inSQL = "INSERT INTO UserReview (comment,restaurantID,reviewRating,reviewDate)VALUES('"+db.comment+"','"+db.restaurantID+"','"+str(db.reviewRating)+"','"+str(db.reviewDate)+"');"
        #print ("old SQL : " + inSQL)
        inSQL = re.sub("(.)'(.)", repl, inSQL)
        #print ("new SQL : "+ inSQL)
    # createSql = "CREATE TABLE Restaurant ( ResID int, Address varchar(255), Coordinate varchar(255), Price varchar(255), City varchar(255) );"
    # insertSql = "INSERT INTO Location (address,longitude,latitude)VALUES('test','10.2','10.1');"
    selectSql = "select * from Restaurant"
    try:
        #inSQL = "INSERT INTO Location (locationID,address,longitude,latitude)VALUES('test','test','10.2','10.1');"
        conn = psycopg2.connect("dbname='aim1' user='admin' host='localhost' password='1234'")
        print('PostgreSQL database:')
        cur = conn.cursor()
        #cur.execute(open("/home/p/django/aim1/mysite/polls/restaurant_schema_truncate.sql", "r").read())
        cur.execute(inSQL)
        print(inSQL)
        conn.commit()
        
        cur.execute(selectSql)
        print(cur.rowcount)
        row = cur.fetchone()
        while row is not None:
         print(row)
         row = cur.fetchone()
        
    except (Exception, psycopg2.DatabaseError) as error:
     print(error)
    conn.commit()

def get_info(url):

    wb_data = requests.get(url, headers=headers)
 #   time.sleep(2)
    soup = BeautifulSoup(wb_data.text,'lxml')
    websites= soup.select('span.biz-website.js-add-url-tagging > a')
    if websites:
        website=websites[0].get_text()
    else:
       website="None"

    
    phones=soup.select('span.biz-phone')
    if phones:
        phone=phones[0].get_text().strip()
    else:
        phone="None"
        
    feature=0
    features=soup.select('div.short-def-list')
    if features:
        feature_a=features[0].get_text()
        # print(feature_a)
        import re
        feature = re.sub(r"\s{2,}", " ", feature_a)
        print(feature)
        featureName=soup.select('div.short-def-list > dl > dt')
        featureDescription=soup.select('div.short-def-list > dl > dd')
        feature=[]
        for featureName,featureDescription in zip(featureName,featureDescription):
            feature.append(re.sub(r"\s{2,}", " ", featureName.get_text()).strip()+':'+re.sub(r"\s{2,}", " ", featureDescription.get_text()).strip())
    else:
        feature=None
    info={"website":website,"phone":phone,"feature":feature}
    return info


def apiCall(request):
    checkerYelp = True
    checkerGoo = True
    #684 last index
    offset = 253
    responseData = []
    while (checkerYelp):
        ### call yelp api
        resp = requests.get(
            'https://api.yelp.com/v3/businesses/search?term=restaurant&location=berlin&limit=1&offset=' + str(offset),
            headers={
                'Authorization': 'Bearer sfNwLics9lPqpWB7916BaiwHJTYVw7a2jlWbcxbwJuvdmvCB4flz1Hv0tPL3tZQpgl88DoGytEUEJCRrtChhSAU7rZ5KBOlidyyVY24TzREO_yc0IiX3iLWpnAw5WnYx'}, )
        offset = offset + 1
        if resp.status_code != 200:
            checkerYelp = False
            raise APIError(resp.status_code)
        data = resp.text
        x = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
       
        
        ### get review for each place
        for i in xrange(0, len(x.businesses)):
            locationId = x.businesses[i].id
            yelpUrl = x.businesses[i].url
            #print("Price : " + x.businesses[i].price)
            #print("Location : ")
            #print(x.businesses[i].location)
            #####Insert Location DB
            fullAddress = "".join(e for e in x.businesses[i].location.display_address)
            locationD = ObjDict()
            locationD.locationID = offset
            locationD.address = fullAddress
            locationD.longitude = x.businesses[i].coordinates.longitude
            locationD.latitude = x.businesses[i].coordinates.latitude
            cuisine = ObjDict()
            setupDB(locationD,1)
            
            ####Insert RestaurantRating
            RestaurantRat = ObjDict()
            RestaurantRat.scale = "1.0-5.0"
            RestaurantRat.overallRating = x.businesses[i].rating
            RestaurantRat.source = "Yelp"
            RestaurantRat.restaurantID = x.businesses[i].id
            #print("================")
            setupDB(RestaurantRat,6)
            #print(RestaurantRat)
            #print("================")
            
            ####Insert CUISINE DB
            for d in xrange(0, len(x.businesses[i].categories)):
                #print("================")
                cuisine.cuisineType = x.businesses[i].categories[d].title
                cuisine.restaurantID = x.businesses[i].id
                setupDB(cuisine,2)
                #print(cuisine)
                #print("================")
            
            #locationDB = {"locationID":i,"address":fullAddress,"longitude":x.businesses[i].coordinates.longitude,"latitude":x.businesses[i].coordinates.latitude}
            
            print("================")
            print (yelpUrl)
            print("================")
            info = get_info(yelpUrl)
           
            #####Insert RestaurantDB
            restuarant = ObjDict()
            restuarant.restaurantID = x.businesses[i].id
            if hasattr(x.businesses[i], 'price') :
              restuarant.priceRange = x.businesses[i].price
            else : restuarant.priceRange = "Unknown"
            restuarant.website = info.get("website")
            restuarant.phoneNumber = info.get("phone")
            restuarant.locationID = offset
            setupDB(restuarant,4)
            
            ####Insert RestaurantFeature
            if info.get("feature") is not None :
              resFeature = ObjDict()
              for feat in xrange(0, len(info.get("feature"))):
                #print("================+++")
                
                resFeature.featureName,resFeature.description = info.get("feature")[feat].split(":")
                resFeature.restaurantID = x.businesses[i].id
                #print(resFeature)
                setupDB(resFeature,5)
                #print("================+++")

            
            # print(locationId)
            
            respR = requests.get('https://api.yelp.com/v3/businesses/' + locationId + '/reviews',
                                 headers={
                                     'Authorization': 'Bearer sfNwLics9lPqpWB7916BaiwHJTYVw7a2jlWbcxbwJuvdmvCB4flz1Hv0tPL3tZQpgl88DoGytEUEJCRrtChhSAU7rZ5KBOlidyyVY24TzREO_yc0IiX3iLWpnAw5WnYx'}, )
            if respR.status_code != 200:
                raise APIError(respR.status_code)
            dataR = respR.text
            r = json.loads(dataR, object_hook=lambda d: namedtuple('R', d.keys())(*d.values()))
            # print(r)
            ####Insert PhotoDB
            ####Insert Review
            UserRev = ObjDict()
            photoDB = ObjDict()
            for p in xrange(0, len(r.reviews)):
                photoDB.pictureURL = r.reviews[p].user.image_url
                photoDB.restaurantID = x.businesses[i].id
                UserRev.comment = r.reviews[p].text
                UserRev.reviewRating = r.reviews[p].rating
                UserRev.reviewDate = r.reviews[p].time_created
                UserRev.restaurantID = x.businesses[i].id
                #print("================+++")
                #print(UserRev)
                setupDB(UserRev,7)
                #print("================+++")
                if photoDB.pictureURL is not None :
                    setupDB(photoDB,3)
                #print("Review from yelp : " + r.reviews[p].text)
                #print("Author (yelp) : " + r.reviews[p].user.name)
            lat = x.businesses[i].coordinates.latitude
            # print(lat)
            long = x.businesses[i].coordinates.longitude
            # print(long)
            ### check that place exist in google map or not by given lat long
            
            respG = requests.get(
                'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(lat) + ',' + str(
                    long) + '&radius=5&type=restaurant&key=AIzaSyB_pmY_DHLOEzAeyq6YeVNk1XEugx-5ZfM', )
            if respG.status_code != 200:
                raise APIError(respG.status_code)
            data2 = respG.text
            y = json.loads(data2, object_hook=lambda d: namedtuple('Y', d.keys())(*d.values()))
            #### Get google review
            if len(y.results) > 0:
                placeId = y.results[0].place_id
                # print(placeId)
                respGDetail = requests.get(
                    'https://maps.googleapis.com/maps/api/place/details/json?placeid=' + placeId + '&key=AIzaSyB_pmY_DHLOEzAeyq6YeVNk1XEugx-5ZfM', )
                if respGDetail.status_code != 200:
                    raise APIError(respGDetail.status_code)
                data3 = respGDetail.text
                z = json.loads(data3, object_hook=lambda d: namedtuple('Z', d.keys())(*d.values()))
                RestaurantRatG = ObjDict()
                RestaurantRatG.scale = "1.0-5.0"
                if hasattr(z.result, 'rating') :
                   RestaurantRatG.overallRating = z.result.rating
                else : RestaurantRatG.overallRating = 0.0
                RestaurantRatG.source = "Google Map"
                RestaurantRatG.restaurantID = x.businesses[i].id
                #print("================+++///")
                #print(RestaurantRatG)
                #print("================+++///")
                setupDB(RestaurantRatG,6)
                # print(z.result.reviews)
                if hasattr(z.result, 'reviews') :
                  for k in xrange(0, len(z.result.reviews)):
                    print(" ")
                    timeS = datetime.fromtimestamp(z.result.reviews[k].time)
                    ReviewG = ObjDict()
                    ReviewG.comment = z.result.reviews[k].text
                    ReviewG.reviewRating = z.result.reviews[k].rating
                    ReviewG.reviewDate = timeS.strftime('%Y-%m-%d')
                    ReviewG.restaurantID = x.businesses[i].id
                    #print("===========<<<<<<")
                    #print(ReviewG)
                    setupDB(ReviewG,7)

          
    return HttpResponse('complete')



