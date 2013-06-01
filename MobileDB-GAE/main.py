import webapp2
import json
import urllib
import re
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import ndb


class Mobile(ndb.Model):
    os = ndb.StringProperty()
    camera = ndb.FloatProperty()
    GPS = ndb.BooleanProperty()
    Bluetooth = ndb.BooleanProperty()
    Price = ndb.IntegerProperty()
    company = ndb.StringProperty() #present
    brand = ndb.StringProperty() #present
    image = ndb.StringProperty() #present
    talktime = ndb.IntegerProperty()

class Crawler(webapp2.RequestHandler):
    """crawls the web page"""
    def get(self):
        try:
            self.brand_urls = {}
            html_read = urllib.urlopen("http://www.gsmarena.com").read()
            # html_read = urlfetch.fetch("http://www.gsmarena.com").content
            menu_list_pattern = r'<div id="brandmenu">(.*)</ul>'
            # self.response.out.write(html_read)
            matched = re.search(menu_list_pattern,html_read,re.DOTALL)
            brand_list = None
            if matched:
                brand_list = matched.group(1)
                anchor_pattern = r'<a href="(.*?)">(.*?)</a>'
                
                #has list of tuples url,company
                temp = re.findall(anchor_pattern,brand_list,re.DOTALL)
                
                #modify so it becomes company,url suitable for dict ctr
                modified = []
                for tup in temp:
                    modified.append((tup[1],tup[0]))
                #dictionary key:value pair  =>  company:url
                self.brand_urls = dict(modified)
                #print brand_urls
                #req_companies = ['Apple','Nokia','Motorola','Samsung','HTC']
                req_companies = ['Samsung']
                for key in self.brand_urls.keys():
                    if key not in req_companies:
                        self.brand_urls.pop(key)
                self.update_database()
                # self.response.out.write("Scrapping aaythu")
            else:
                print "some error"
        except Exception, e:
            print e.message
    def update_database(self):
        camera_regex = r"(.*) MP*"
        os_regex = r"*(ios|android|windows|bada|symbian).*"
        
        try:
            for comp_name, url in self.brand_urls.items():
                instance = Company("http://www.gsmarena.com",comp_name,url)
                # print len(device)
                for device in instance.devices:
                    
                    m = re.match(camera_regex,device['Primary'],re.DOTALL)
                    if m:
                        device['Primary'] = float(m.group(1))
                    else:
                        device['Primary'] = 0.0
                    if device['GPS'].find('Yes') >= 0:
                        device['GPS'] = True
                    else:
                        device['GPS'] = False
                    if device['Bluetooth'].find('Yes') >= 0:
                        device['Bluetooth'] = True
                    else:
                        device['Bluetooth'] = False
                    # print "<h1>" + device['OS'] + "</h1>"
                    mobile = Mobile(company=device['Company'],image=device['Image'],os=device['OS'],GPS=device['GPS'],Price=device['Price group'],brand=device['Brand'],camera=device['Primary'],Bluetooth=device['Bluetooth'],talktime=device['Talk time'])
                    mobile.put()    
                    
        
        except Exception, e:
            print e.message


class Company:
    """ this class has fields that contains complete information about all the 
        mobiles of a particular company.
    """
    def __init__(self,website,name,start_page):
        self.website = website
        self.name = name 
        self.spanning_pages = self.fill_spanning_pages(start_page)
        self.device_urls = self.fill_device_urls()
        self.devices = self.fill_devices()
        
    def fill_spanning_pages(self,start_page):
        try:
            urls_pages = list()
            urls_pages.append(start_page)
            file_obj = urllib.urlopen(self.website + '/' + start_page)
            html_file = file_obj.read()
            nav_list_pattern = r'<div class="nav-pages">(.*?)</div>'
            re_obj = re.search(nav_list_pattern,html_file,re.DOTALL)
            if re_obj:
                matched = re_obj.group()
                anchor_pattern = r'<a href="(.*?)">(.*?)</a>'
                temp = re.findall(anchor_pattern,matched,re.DOTALL)
                temp = temp[:len(temp) - 1]
                #now add all urls to the spanning list
                for tup in temp:
                    if tup[0] not in urls_pages:
                        urls_pages.append(tup[0])
           
            return urls_pages
        except Exception, e:
            print "in fill_spanning_pages"
            print e.message

    def fill_device_urls(self):
        try:
            final_list = []
            for page in self.spanning_pages:
                html_obj = urllib.urlopen(self.website + '/' + page)
                html_file = html_obj.read()
                list_pattern = r'<div class="makers">(.*?)</div>'
                dev_list = []
                temp = re.findall(list_pattern,html_file,re.DOTALL)
                anchor_pattern = r'<a href="(.*?)"><img src=(.*?)(?=(.jpg|.gif|.png)).*?<strong>(.*?)</strong></a>'
                for blocks in temp:
                    modified = []
                    li = re.findall(anchor_pattern,blocks,re.DOTALL)
                    for tup in li:
                        modified.append((tup[3],tup[1] + tup[2],tup[0]))
                    dev_list.extend(modified)
                final_list.extend(dev_list)
            return final_list

        except Exception, e:
            print "in fill_device_urls"
            print e.message

    def fill_devices(self):
        all_devices = []
        try:
            for device in self.device_urls:
                url = self.website + '/' + device[2]
                html_obj = urllib.urlopen(url)
                html_file = html_obj.read()
                data_dict = {}
                div_pattern = r'<div id="specs-list">(.*?)</div>'
                re_obj = re.search(div_pattern,html_file,re.DOTALL)
                if re_obj:
                    matched = re_obj.group()
                    title_pattern = r'<td class="ttl">.*?<a href=.*?>(.*?)</a>.*?</td>.*?<td class="nfo">(.*?)</td>'
                    match = re.findall(title_pattern,matched,re.DOTALL)
                    match.append(('Brand',device[0]))
                    match.append(('Image',device[1]))
                    match.append(('Company',self.name))
                    err = ['Video','Loudspeaker','Audio quality','Display','Camera','Primary','Battery life','Secondary']
                    data_dict = dict(match)
                    for qual in err:
                        if data_dict.has_key(qual):
                            re1 = r'.*?<a class="noUnd" href=.*?>(.*?)</a>'
                            re2 = r'(.*?)<a href=.*?</a>'
                            robj1 = re.match(re1,data_dict[qual],re.DOTALL)
                            robj2 = re.match(re2,data_dict[qual],re.DOTALL)
                            if robj1:
                                data_dict[qual] = robj1.group(1).split(',')[0]
                            elif robj2:
                                data_dict[qual] = robj2.group(1).split(',')[0]
                    if data_dict.has_key("Price group"):
                        price_url = data_dict.pop("Price group")
                        price = re.findall(r'<img src=.*? title="About (.*?) EUR">',price_url,re.DOTALL)
                        data_dict['Price group'] = int(price[0].strip().split(',')[0])  
                    talk_time_pattern = r'(?i)up to (.*?)h.*?'
                    if data_dict.has_key('Talk time'):
                        talktime = data_dict.pop('Talk time')
                        tt = re.match(talk_time_pattern,talktime,re.DOTALL)
                        if tt:
                            data_dict['Talk time'] = int(tt.group(1).strip().split(' ')[0])
                            
                        else:
                            data_dict['Talk time'] =  5
                    
                    available_features = data_dict.keys() 
                    if 'Primary' not in available_features:
                        data_dict['Primary'] = "0 MP"
                    if 'GPS' not in available_features:
                        data_dict['GPS'] = "no"
                    if 'OS' not in available_features:
                        data_dict['OS'] = "unknown"
                    if 'Bluetooth' not in available_features:
                        data_dict['Bluetooth'] = "no"
                    if 'Price group' not in available_features:
                        data_dict['Price group'] = 100
                    if 'Talk time' not in available_features:
                        data_dict['Talk time'] =  5
                    all_devices.append(data_dict)
                else:
                    print "some error in fill_devices()"
            return all_devices
        except Exception, e:
            print "in fill_devices"
            print e.message

class QueryHandler(webapp2.RequestHandler):
    def post(self):
        request_json = json.loads(self.request.body)
        response_json = {'result':[]}
        # mobiles = ndb.gql("SELECT image,brand FROM Mobile WHERE Price>400 AND Bluetooth=True")
        gql_query = self.getGql(request_json)
        # self.response.out.write(gql_query)
        mobiles = ndb.gql(gql_query)
        for mobile in mobiles:
            response_json['result'].append(json.dumps(mobile.to_dict()))
        self.response.out.write(json.dumps(response_json))

    def getGql(self,request_json):
        requested_features = ['image','brand'] + request_json['requested_features']
        conditional_features = request_json['conditional_features']
        if "company=all" not in conditional_features:
            gql_query = "SELECT DISTINCT "
            for eachFeature in requested_features:
                gql_query = gql_query + eachFeature + ","

            gql_query = gql_query[:-1] + " FROM Mobile "
            gql_query = gql_query + "WHERE "
            for eachFeature in conditional_features:
                temp = eachFeature.split("=")
                if (temp[0] == "company") or (temp[0] == "os"):
                    eachFeature = temp[0] + "=" + "'" + temp[1] +"'"
                gql_query = gql_query + eachFeature + " AND "
            gql_query = gql_query[:-4]
            # self.response.out.write(gql_query)
            return gql_query
        else:
            conditional_features.remove("company=all")
            if len(conditional_features) == 0:
                gql_query = "SELECT DISTINCT "
                for eachFeature in requested_features:
                    gql_query = gql_query + eachFeature + ","
                gql_query = gql_query[:-1] + ' FROM Mobile'
                return gql_query
            else:
                gql_query = "SELECT DISTINCT "
                for eachFeature in requested_features:
                    gql_query = gql_query + eachFeature + ","

                gql_query = gql_query[:-1] + " FROM Mobile "
                gql_query = gql_query + "WHERE "
                for eachFeature in conditional_features:
                    temp = eachFeature.split("=")
                    if temp[0] == "os":
                        eachFeature = temp[0] + "=" + "'" + temp[1] +"'"
                    gql_query = gql_query + eachFeature + " AND "
                gql_query = gql_query[:-4]
                # self.response.out.write(gql_query)
                return gql_query

        
class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        self.response.out.write(template.render("index.html",{}))


app = webapp2.WSGIApplication([
        ('/scrap',Crawler),
        ('/query',QueryHandler),
        ('/*', MainHandler),
        ],debug=True)
