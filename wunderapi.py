"""
wunderapi.py
Python module for JSON requests to the Wunderground.com Weather API
author: Alicia Barnash
author_email: a.barnash@gmail.com
date: 03-13-2012
version: 1.0
"""

import urllib2,json

WunderFeatures = ['geolookup','conditions','forecast',
                  'astronomy','radar','satellite',
                  'webcams','history','alerts','hourly',
                  'hourly10day','forecast10day','yesterday',
                  'planner','autocomplete','almanac','lang']
    
class WunderQuest():
    """
        Generic class for requesting JSON data from the Weather API
        Requires API Key from http://www.wunderground.com/weather/api/
    """
    def __init__(self,apikey,features = ['conditions']):
        self.apikey = apikey
        self.features = features
        self.featureString = ''
        self.getFeatureString()
        self.baseURL = 'http://api.wunderground.com/api/%s/%s'%(self.apikey,self.featureString)
        
    def byZip(self,zipcode):
        "Request weather data by Zip Code"
        self.requestURL = self.baseURL + 'q/%s.json'%zipcode
        return self.byURL(self.requestURL)
        
    def byUSCity(self,city,state):
        "Request weather data by US City"
        city = city.replace(' ','_')
        self.requestURL = self.baseURL + 'q/%s/%s.json'%(state,city)
        self.byURL(self.requestURL)
    
    def byWorldCity(self,city,country):
        "Request weather data by International City"
        city = city.replace(' ','_')
        country = country.replace(' ','_')
        self.requestURL = self.baseURL + 'q/%s/%s.json'%(country,city)
        self.byURL(self.requestURL)

    def byAirport(self,airportcode):
        "Request weather data by Airport Code"
        self.requestURL = self.baseURL + 'q/%s.json'%(airportcode)
        self.byURL(self.requestURL)

    def byLatLong(self,latitude,longitude):
        "Request weather data by Latitude and Longitude"
        self.requestURL = self.baseURL + 'q/%s,%s.json'%(latitude,longitude)
        self.byURL(self.requestURL)

    def byPWS(self,pws):
        "Request weather data by Personal Weather Station code"
        self.requestURL = self.baseURL + 'q/pws:%s.json'%(pws)
        self.byURL(self.requestURL)

    def byAutoIP(self):
        "Request weather data by requestor IP address"
        self.requestURL = self.baseURL + 'q/%s.json'%('autoip')
        self.byURL(self.requestURL)

    def bySpecificIP(self,ip):
        "Request weather data by IP address"
        self.requestURL = self.baseURL + 'q/%s.json?geo_ip=%s'%('autoip',ip)
        self.byURL(self.requestURL)
        
    def byURL(self,urlstring):
        "Request weather data by URL"
        f = urllib2.urlopen(urlstring)
        jstr = f.read()
        self.response = json.loads(jstr)
        self.responseInfo = self.response['response']
        
        
    def getFeatureString(self):
        for feat in self.features:
            if feat in WunderFeatures:
                self.featureString += str(feat) + '/'
            else:
                print("***%s Not a valid Wunderground feature***"%feat)

class GeoLookup(WunderQuest):
    "Class for requesting GeoLookup feature data from the Weather API"
    def __init__(self,apikey):
        self.apikey = apikey
        self.features = 'geolookup'
        self.featureString = 'geolookup/'
        self.baseURL = 'http://api.wunderground.com/api/%s/%s'%(self.apikey,self.featureString)
        
class TravelPlanner(WunderQuest):
    "Class for requesting TravelPlanner data from the Weather API"
    def __init__(self,apikey,startmonth,startday,endmonth,endday):
        self.apikey = apikey
        self.features = ['planner']
        self.featureString = 'planner_%s%s%s%s'%(startmonth,startday,endmonth,endday)
        self.getFeatureString()
        self.baseURL = 'http://api.wunderground.com/api/%s/%s'%(self.apikey,self.featureString)
        
class Anvil(WunderQuest):
    "Class for requesting Anvil feature data from the Weather API"
    def __init__(self,apikey):
        self.apikey = apikey
        self.features = ['forecast10day','yesterday','webcams']
        self.featureString = ''
        self.getFeatureString()
        self.baseURL = 'http://api.wunderground.com/api/%s/%s'%(self.apikey,self.featureString)

    def byURL(self,urlstring):
        WunderQuest.byURL(self,urlstring)
        self.history = self.response['history']
        self.webcams = self.response['webcams']
        self.forecast = self.response['forecast']

class Stratus(WunderQuest):
    "Class for requesting Stratus feature data from the Weather API"
    def __init__(self,apikey):
        self.apikey = apikey
        self.features = ['conditions','forecast','astronomy','almanac']
        self.featureString = ''
        self.getFeatureString()
        self.baseURL = 'http://api.wunderground.com/api/%s/%s'%(self.apikey,self.featureString)

    def byURL(self,urlstring):
        WunderQuest.byURL(self,urlstring)
        self.conditions = self.response['current_observation']
        self.forecast = self.response['forecast']
        self.astronomy = self.response['moon_phase']
        self.almanac = self.response['almanac']
        
class Cumulus(WunderQuest):
    "Class for requesting Cumulus feature data from the Weather API"
    def __init__(self,apikey):
        self.apikey = apikey
        self.features = ['forecast10day','hourly','satellite','radar','alerts']
        self.featureString = ''
        self.getFeatureString()
        self.baseURL = 'http://api.wunderground.com/api/%s/%s'%(self.apikey,self.featureString)

    def byURL(self,urlstring):
        WunderQuest.byURL(self,urlstring)
        self.forecast = self.response['forecast']
        self.satellite = self.response['satellite']
        self.hourly = self.response['hourly_forecast']
        self.radar = self.response['radar']
        self.alerts = self.response['alerts']

    def getTravelPlan(self,startmonth,startday,endmonth,endday):
        self.travelplan = tpl.TravelPlanner(self.apikey,startmonth,startday,endmonth,endday)
        return self.travelplan
