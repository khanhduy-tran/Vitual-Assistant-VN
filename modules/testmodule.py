# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# import chromedriver_binary
# import requests
# import json
# from geopy.geocoders import Nominatim
# from geopy.distance import great_circle
# def getLocation():
#     chrome_options = Options()
#     chrome_options.add_argument("--use-fake-ui-for-media-stream")
#     timeout = 20
#     driver = webdriver.Chrome(executable_path="D:\\VKU\\Nam 4 - Ki 1\\Xử lý ngôn ngữ tự nhiên\\PersonalAssistantChatbot\\assets\\ggdrive\\chromedriver.exe",chrome_options=chrome_options)
#     driver.get("https://mycurrentlocation.net/")
#     wait = WebDriverWait(driver, timeout)
#     longitude = driver.find_elements('xpath','//*[@id="longitude"]')
#     longitude = [x.text for x in longitude]
#     longitude = str(longitude[0])
#     latitude = driver.find_elements('xpath','//*[@id="latitude"]')
#     latitude = [x.text for x in latitude]
#     latitude = str(latitude[0])
#     driver.quit()
#     return latitude+","+longitude
# geolocator = Nominatim(user_agent='assistant')
# data = getLocation()
# print(data)
# data1 = (data.latitude,data.longitude)
# print(data1)
import os
from dotenv import load_dotenv
import smtplib
import ssl

# Import the email modules we'll need
from email.message import EmailMessage
load_dotenv('config.env')

email = os.environ.get('MAIL_USERNAME')
print(email)
password = os.environ.get('MAIL_PASSWORD')
print(password)
email_receiver = 'famab41750@sunetoa.com'
subject = 'test emaill'
body = 'hell friend'

 
if not email or not password:
		raise Exception("Mail_username hoặc mail_password không được tải trong môi trường, tạo tệp .env và thêm 2 giá trị này")
	#if '@gmail.com' not in rec_email: return
em = EmailMessage()
em['From'] = email
em['To'] = email_receiver
em['subject'] = subject
em.set_content(body)
context = ssl.create_default_context()
with smtplib.SMTP_SSL('smtp.gmail.com',465, context = context) as smtp:
     smtp.login(email,password)
     smtp.sendmail(email,email_receiver,em.as_string())	

