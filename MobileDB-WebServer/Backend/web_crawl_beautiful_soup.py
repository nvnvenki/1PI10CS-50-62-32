import urllib
import re
import time
import pymongo
import bs4

class Crawler:
	"""crawls the web page"""
	def __init__(self, website):
		self.website = website
		self.file_obj = urllib.urlopen(self.website)
		self.brand_urls = self.get_urls()
	def get_urls(self):
		try:
			html_read = self.file_obj.read()
			soup = bs4.BeautifulSoup(html_read,"html.parser")
			# print "Type of html_read " + str(type(html_read))
			# print html_read
			# brand_list = None
			# print soup.prettify()
			brandmenu_div = soup.find("div",id="brandmenu")
			# print "Brand menu :" + str(brandmenu_div)
			if brandmenu_div:
				ul = brandmenu_div.find("ul")
				li_list = [li for li in ul.contents[1:] if li.name.encode("ascii","ignore") == 'li']
				a_list = [li.find("a") for li in li_list]
				brand_urls = dict([(a.string.encode("ascii","ignore"),a["href"].encode("ascii","ignore")) for a in a_list])
				req_companies = ["Nokia"]
				for key in brand_urls.keys():
					if key not in req_companies:
						brand_urls.pop(key)
				print "Got the brand urls: " + str(brand_urls)
				return brand_urls
			else:
				print "no mobile urls found"
		except Exception, e:
			print e.message
	def update_database(self):
		instance = Company(self.website,"Nokia",self.brand_urls["Nokia"])
		for i in instance.devices:
			for k, v in i.items():
				print k + ":" + v
		
		client = pymongo.MongoClient('localhost',27017)
		database = client['device_database_bs4']
		collection = database['devices']
		try:
			print "in update database"
			for comp_name, url in self.brand_urls.items():
				instance = Company(self.website,comp_name,url)
				print len(instance.devices)
				for dev in instance.devices:
					dev = eval((str(dev).decode("ascii","ignore")).encode("ascii"))
					collection.insert(dev)
			client.close()
		except Exception, e:
			print e.message
		
class Company:
	""" this class has fields that contains complete information about all the 
		mobiles of a particular company.
	"""
	def __init__(self,website,name,start_page):
		self.website = website
		self.name = name 
		self.spanning_pages = self.fill_spanning_pages(start_page)[0]
		self.device_urls = self.fill_device_urls()[0]
		self.devices = self.fill_devices()
	def fill_spanning_pages(self,start_page):
		try:
			# print "here1"
			urls_pages = list()
			urls_pages.append(start_page)
			# print "here2"
			html = urllib.urlopen(self.website + '/' + start_page).read()
			soup = bs4.BeautifulSoup(html,"html.parser")
			nav_pages_div = soup.find("div","nav-pages")
			# print nav_pages_div
			# print "here3"
			if nav_pages_div:
				# print "here"
				a_list = nav_pages_div.find_all("a")
				# print a_list
				for a in a_list:
					url = a["href"].encode("ascii","ignore")
					if url not in urls_pages:
						urls_pages.append(url)
			print "Spannig pages: " + str(urls_pages)
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
				soup = bs4.BeautifulSoup(html_file,"html.parser")
				makers_div_list = soup.find_all("div","makers")
				for div in makers_div_list:
					li_list = div.find_all("li")
					for li in li_list:
						a = li.find("a")
						final_list.append((a.find("strong").string.encode("ascii","ignore"),a.find("img")["src"].encode("ascii","ignore"),a["href"].encode("ascii","ignore")))
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
				data_dict = dict()

				soup = bs4.BeautifulSoup(html_file,"html.parser")
				specs_div = soup.find("div",id="specs-list")
				rows_list = specs_div.find_all("tr")
				for row in rows_list:
					if row.find("td","ttl").find("a"):
						data_dict[row.find("td","ttl").find("a").string.encode("ascii","ignore")] = row.find("td","nfo").string.encode("ascii","ignore")
				data_dict["Company"] = self.name
				data_dict["Brand"] = device[0]
				data_dict["Image"] = device[1]
				err = ['Video','Loudspeaker','Audio quality','Display','Camera','Primary','Battery life','Secondary']
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
					if data_dict.has_key('Stand-by'):
						talktime = data_dict.pop('Stand-by')
						tt = re.match(talk_time_pattern,talktime,re.DOTALL)
						if tt:	
							data_dict['Stand-by'] = int(tt.group(1).strip().split(' ')[0])
					if data_dict.has_key('3.5mm jack'):
						jack = data_dict.pop('3.5mm jack')
						data_dict['jack'] = jack
					if data_dict.has_key('SAR EU'):
						data_dict.pop('SAR EU')
					if data_dict.has_key('SAR US'):
						data_dict.pop('SAR US')
					if data_dict.has_key('Features'):
						data_dict.pop('Features')
				all_devices.append(data_dict)
			return all_devices
		except Exception, e:
			print "in fill_devices"
			print e.message
	def formatter(self):
		try:
			fobj = open("devices.txt","w")
			for tup in self.devices:
				fobj.write('*' * 100 + '\n')
				fobj.write('Name : ' + tup[0] + '\n')
				fobj.write('Image Url : ' + tup[1] + '\n')
				fobj.write('Specs : \n')
				for key, val in tup[2].items():
					fobj.write(key + " : " + val + '\n')
				fobj.write('*' * 100 + '\n')
			fobj.close()
		except Exception, e:
			print e.message
def main():
	try:
		site = 'http://www.gsmarena.com'
		# html = urllib.urlopen(site)
		one = time.time()
		crawl = Crawler(site)
		crawl.update_database()
		two = time.time()
		print "elapsed : " + str(two - one) + "seconds..."
	except Exception, e:
		print "connection error"
		print e.message
if __name__ == '__main__':
	main()
