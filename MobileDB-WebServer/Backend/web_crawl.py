import urllib
import re
import time
import pymongo

class Crawler:
	"""crawls the web page"""
	def __init__(self, website):
		self.website = website
		self.file_obj = urllib.urlopen(self.website)
		self.brand_urls = self.get_urls()
	def get_urls(self):
		try:
			html_read = self.file_obj.read()
			menu_list_pattern = r'<div id="brandmenu">(.*)</ul>'
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
				brand_urls = dict(modified)
				#print brand_urls
				#req_companies = ['Apple','Nokia','Motorola','Samsung','HTC']
				req_companies = ['Sony']
				for key in brand_urls.keys():
					if key not in req_companies:
						brand_urls.pop(key)
				#print "popped"
				#print brand_urls
				return	brand_urls
			else:
				print "some error"
		except Exception, e:
			print e.message
	def update_database(self):
		client = pymongo.MongoClient('localhost',27017)
		database = client['device_database']
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
			else:
				print "in fill_spanning_pages() some error : no navigation entries"
			#print urls_pages
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
				else:
					print "some error in fill_devices()"
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
