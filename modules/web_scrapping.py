import wikipedia
import webbrowser
import requests
from bs4 import BeautifulSoup
import smtplib
import urllib.request
import os
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import ssl
from email.message import EmailMessage
import normal_chat
from youtubesearchpython import VideosSearch
class COVID:
	def __init__(self):
		self.total = 'Not Available'
		self.deaths = 'Not Available'
		self.recovered = 'Not Available'
		self.totalIndia = 'Not Available'
		self.deathsIndia = 'Not Available'
		self.recoveredIndia = 'Not Available'

	def covidUpdate(self):
		URL = 'https://www.worldometers.info/coronavirus/'
		result = requests.get(URL)
		src = result.content
		soup = BeautifulSoup(src, 'html.parser')

		temp = []
		divs = soup.find_all('div', class_='maincounter-number')
		for div in divs:
			temp.append(div.text.strip())
		self.total, self.deaths, self.recovered = temp[0], temp[1], temp[2]
		

	def covidUpdateVietnam(self):
		URL = 'https://www.worldometers.info/coronavirus/country/viet-nam/'
		result = requests.get(URL)
		src = result.content
		soup = BeautifulSoup(src, 'html.parser')

		temp = []
		divs = soup.find_all('div', class_='maincounter-number')
		for div in divs:
			temp.append(div.text.strip())
		self.totalIndia, self.deathsIndia, self.recoveredIndia = temp[0], temp[1], temp[2]

	def totalCases(self,india_bool):
		if india_bool: return self.totalIndia
		return self.total

	def totalDeaths(self,india_bool):
		if india_bool: return self.deathsIndia
		return self.deaths

	def totalRecovery(self,india_bool):
		if india_bool: return self.recoveredIndia
		return self.recovered

	def symptoms(self):
		symt = ['1. Sốt',
				'2. Ho',
				'3. Khó thở',
				'4. Mất vị giác hoặc mùi mới',
				'5. Đau họng',
				'6. Thở gấp hoặc khó thở',
				'7. Bệnh tiêu chảy',
				'8. Buồn nôn hoặc nôn mửa',
				'9. Đau bụng',
				'10. Mệt mỏi',
				'11. Đau đầu',
				'12. Đau nhức cơ thể']
		return symt

	def prevention(self):
		prevention = ['1. Làm sạch bàn tay của bạn thường xuyên. Sử dụng xà phòng và nước, hoặc một cái cọ rửa tay dựa trên cồn.',
						'2. Duy trì khoảng cách an toàn với bất kỳ ai đang ho hoặc hắt hơi.',
						'3. Đeo mặt nạ khi không thể tránh xa những người bị bệnh',
						'4. Không chạm tay vào mắt, mũi và miệng của bạn',
						'5. Dùng tay che mũi và miệng của bạn khi ho hoặc hắt hơi',
						'6. Ở nhà nếu bạn cảm thấy không khỏe',
						'7. Nếu bạn bị sốt, ho và khó thở, hãy tìm kiếm sự chăm sóc y tế']
		return prevention

def wikiResult(query):
	query = query.replace('wikipedia','')
	query = query.replace('tìm','')
	if len(query.split())==0: query = "wikipedia"
	try:
		wikipedia.set_lang('vi')
		return wikipedia.summary(query, sentences=2)
	except Exception as e:
		return "Kết quả mong muốn không tìm thấy!"

class WEATHER:
	def __init__(self):
		#Currently in Lucknow, its 26 with Haze
		self.tempValue = ''
		self.city = ''
		self.currCondition = ''
		self.speakResult = ''

	def updateWeather(self):
		#res = requests.get("https://ipinfo.io/")
		#data = res.json()
		data = getLocation()
		# URL = 'https://weather.com/en-IN/weather/today/l/'+data['loc']
		URL = 'https://weather.com/vi-VN/weather/today/l/'+data
		result = requests.get(URL)
		src = result.content

		soup = BeautifulSoup(src, 'html.parser')

		city = ""
		for h in soup.find_all('h1'):
			cty = h.text
			cty = cty.replace('thời tiết','')
			self.city = cty[:cty.find(',')]
			break

		spans = soup.find_all('span')
		for span in spans:
			try:
				if span['data-testid']=="TemperatureValue":
					self.tempValue = span.text[:-1]
					break
			except Exception as e:
				pass

		divs = soup.find_all('div', class_='CurrentConditions--phraseValue--2Z18W')
		for div in divs:
			self.currCondition = div.text
			break

	def weather(self):
		from datetime import datetime
		today = datetime.today().strftime('%A')
		self.speakResult = "Hiện đang ở: " + self.city + ", nhiệt độ là: " + self.tempValue + " độ, và chất lượng không khí: " + self.currCondition 
		return [self.tempValue, self.currCondition, today, self.city, self.speakResult]

c = COVID()
w = WEATHER()

def dataUpdate():
	c.covidUpdate()
	c.covidUpdateVietnam()
	w.updateWeather()

##### WEATHER #####
def weather():
	return w.weather()

### COVID ###
def covid(query):
	
	if "việt nam" in query: india_bool = True
	else: india_bool = False

	if "thống kê" in query or 'báo cáo' in query:
		return ["Đây là số liệu thống kê...", ["Tổng số trường hợp: " + c.totalCases(india_bool), "Tổng hồi phục: " + c.totalRecovery(india_bool), "Tổng số người chết: " + c.totalDeaths(india_bool)]]

	elif "triệu chứng" in query:
		return ["Đây là các triệu chứng...", c.symptoms()]

	elif "ngăn ngừa" in query or "phòng tránh" in query or "đề phòng" in query:
		return ["Dưới đây là một số phòng ngừa từ Covid-19:", c.prevention()]
	
	elif "số hồi phục" in query:
		return "Tổng hồi phục là: " + c.totalRecovery(india_bool)
	
	elif "số người chết" in query:
		return "Tổng số người chết là: " + c.totalDeaths(india_bool)
	
	else:
		return "Tổng số trường hợp là: " + c.totalCases(india_bool)

def latestNews(news=5):
	URL = 'https://vnexpress.net/tin-tuc-24h/'
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')

	headlineLinks = []
	headlines = []

	divs = soup.find_all('div', {'class':'title-news'})

	count=0
	for div in divs:
		count += 1
		if count>news:
			break
		a_tag = div.find('a')
		headlineLinks.append(a_tag.attrs['href'])
		headlines.append(a_tag.text)

	return headlines,headlineLinks

def maps(text):
	text = text.replace('maps', '')
	text = text.replace('map', '')
	text = text.replace('google', '')
	openWebsite('https://www.google.com/maps/place/'+text)

def getLocation():
	chrome_options = Options()
	chrome_options.add_argument("--use-fake-ui-for-media-stream")
	timeout = 20
	driver = webdriver.Chrome(executable_path="D:\\VKU\\Nam 4 - Ki 1\\Xử lý ngôn ngữ tự nhiên\\PersonalAssistantChatbot\\assets\\ggdrive\\chromedriver.exe",chrome_options=chrome_options)
	driver.get("https://mycurrentlocation.net/")
	
	wait = WebDriverWait(driver, timeout)
	longitude = driver.find_elements('xpath','//*[@id="longitude"]')
	longitude = [x.text for x in longitude]
	longitude = str(longitude[0])
	latitude = driver.find_elements('xpath','//*[@id="latitude"]')
	latitude = [x.text for x in latitude]
	latitude = str(latitude[0])
	driver.quit()
	return latitude+","+longitude

def giveDirections(startingPoint, destinationPoint):

	geolocator = Nominatim(user_agent='assistant')
	if 'vị trí hiện tại' in startingPoint or 'hiện tại' in startingPoint:
		
		startinglocation = getLocation()
		startingPoint = startinglocation
		startinglocationCoordinate = startinglocation
		
	else:
		startinglocation = geolocator.geocode(startingPoint)
		#startingPoint = startinglocation.address.replace(' ', '+')
		startinglocationCoordinate = (startinglocation.latitude, startinglocation.longitude)

	destinationlocation = geolocator.geocode(destinationPoint)
	#destinationPoint = destinationlocation.address.replace(' ', '+')
	openWebsite('https://www.google.co.in/maps/dir/'+startingPoint+'/'+destinationPoint+'/')
	destinationlocationCoordinate = (destinationlocation.latitude, destinationlocation.longitude)
	total_distance = great_circle(startinglocationCoordinate, destinationlocationCoordinate).km #.mile
	return str(round(total_distance, 2)) + 'KM'

def openWebsite(url='https://www.google.com/'):
	webbrowser.open(url)

def jokes():
	URL = 'https://icanhazdadjoke.com/'
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')
	from googletrans import Translator, constants
	translator = Translator()
	try:
		p = soup.find('p')
		translation = translator.translate(p.text,src='en',dest='vi')
		return translation.text
	except Exception as e:
		raise e


def youtube(query):
	query = query.replace('play',' ')
	query = query.replace('trên YouTube',' ')
	query = query.replace('YouTube',' ')
	query = query.replace('mở bằng YouTube',' ')

	print("Tìm kiếm video...")
	
	videosSearch = VideosSearch(query, limit = 1)
	results = videosSearch.result()['result']
	print(results) 
	print("Tìm kiếm hoàn tất!")

	webbrowser.open('https://www.youtube.com/watch?v=' + results[0]['id'])
	return "Mời bạn xem video..."


def googleSearch(query):
	if 'ảnh' in query:
		query += "&tbm=isch"
	query = query.replace('hình ảnh','')
	query = query.replace('ảnh','')
	query = query.replace('tìm kiếm ảnh','')
	query = query.replace('hiển thị ảnh','')
	webbrowser.open("https://www.google.com/search?q=" + query)
	return "Đây là kết quả..."

def sendWhatsapp(phone_no='',message=''):
	phone_no = '+84' + str(phone_no)
	webbrowser.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+message)
	import time
	from pynput.keyboard import Key, Controller
	time.sleep(10)
	k = Controller()
	k.press(Key.enter)

def email(rec_email=None, text="Hello, It's F.R.I.D.A.Y. here...", sub='F.R.I.D.A.Y.'):
	# from dotenv import load_dotenv
	# load_dotenv('config.env')
	# username = os.environ.get('MAIL_USERNAME') # email address
	# print(username)
	# password = os.environ.get('MAIL_PASSWORD')
	# print(password)
	# if not username or not password:
	# 	raise Exception("Mail_username hoặc mail_password không được tải trong môi trường, tạo tệp .env và thêm 2 giá trị này")
	
	# if '@gmail.com' not in rec_email: return
	# s = smtplib.SMTP('smtp.gmail.com', 587)
	# s.starttls()
	# s.login(USERNAME, PASSWORD)
	# message = 'Tiêu đề: {}\n\n{}'.format(sub, text)
	# s.sendmail(USERNAME, rec_email, message)
	# print("Gửi")
	# s.quit()
	username = 'vocaominh2k1@gmail.com'
	password = 'lazojrmgdvkxjwbd'
	em = EmailMessage()
	em['From'] = username
	em['To'] = rec_email
	em['subject'] = sub
	em.set_content(text)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com',465, context = context) as smtp:
    	 smtp.login(username,password)
    	 sendEmail=smtp.sendmail(username,rec_email,em.as_string())
	return "Đã gửi thư thành công!"
		 

def downloadImage(query, n=4):
	query = query.replace('images','')
	query = query.replace('image','')
	query = query.replace('search','')
	query = query.replace('show','')
	URL = "https://www.google.com/search?tbm=isch&q=" + query
	result = requests.get(URL)
	src = result.content

	soup = BeautifulSoup(src, 'html.parser')
	imgTags = soup.find_all('img', class_='yWs4tf') # old class name -> t0fcAb

	if os.path.exists('Downloads')==False:
		os.mkdir('Downloads')

	count=0
	for i in imgTags:
		if count==n: break
		try:
			urllib.request.urlretrieve(i['src'], 'Downloads/' + str(count) + '.jpg')
			count+=1
			print('Downloaded', count)
		except Exception as e:
			raise e

