#########################
# GLOBAL VARIABLES USED #
#########################
ai_name = 'F.R.I.D.Y.'.lower()
EXIT_COMMANDS = ['tạm biệt','thoát','hẹn gặp lại','dừng hệ thống', 'đóng ứng dụng']

rec_email, rec_phoneno = "", ""
WAEMEntry = None

avatarChoosen = 0
choosedAvtrImage = None

botChatTextBg = "#007cc7"
botChatText = "white"
userChatTextBg = "#4da8da"

chatBgColor = '#12232e'
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
KCS_IMG = 1 #0 for light, 1 for dark
voice_id = 0 #0 for female, 1 for male
ass_volume = 1 #max volume
ass_voiceRate = 200 #normal voice rate

####################################### IMPORTING MODULES ###########################################
""" User Created Modules """
try:
	import normal_chat
	import math_function
	import app_control
	import web_scrapping
	import game
	import app_timer
	import dictionary
	import todo_handler
	import file_handler
	from user_handler import UserData
	from face_unlocker import clickPhoto, viewPhoto
	from dotenv import load_dotenv

	load_dotenv()
except Exception as e:
	 print(e)

""" System Modules """
try:
	import os
	import speech_recognition as sr
	import pyttsx3
	from tkinter import *
	from tkinter import ttk
	from tkinter import messagebox
	from tkinter import colorchooser
	from PIL import Image, ImageTk
	from time import sleep
	from threading import Thread
except Exception as e:
	raise e

########################################## LOGIN CHECK ##############################################
try:
	user = UserData()
	user.extractData()
	ownerName = user.getName().split()[0]
	ownerDesignation = "Sếp"
	if user.getGender()=="Female": ownerDesignation = "Ma'am"
	ownerPhoto = user.getUserPhoto()
except Exception as e:
	print("Bạn chưa đăng ký !\nChạy SECURITY.py để đăng ký khuôn mặt của bạn.")
	raise SystemExit


########################################## BOOT UP WINDOW ###########################################
def ChangeSettings(write=False):
	import pickle
	global background, textColor, chatBgColor, voice_id, ass_volume, ass_voiceRate, AITaskStatusLblBG, KCS_IMG, botChatTextBg, botChatText, userChatTextBg
	setting = {'background': background,
				'textColor': textColor,
				'chatBgColor': chatBgColor,
				'AITaskStatusLblBG': AITaskStatusLblBG,
				'KCS_IMG': KCS_IMG,
				'botChatText': botChatText,
				'botChatTextBg': botChatTextBg,
				'userChatTextBg': userChatTextBg,
				'voice_id': voice_id,
				'ass_volume': ass_volume,
				'ass_voiceRate': ass_voiceRate
			}
	if write:
		with open('userData/settings.pck', 'wb') as file:
			pickle.dump(setting, file)
		return
	try:
		with open('userData/settings.pck', 'rb') as file:
			loadSettings = pickle.load(file)
			background = loadSettings['background']
			textColor = loadSettings['textColor']
			chatBgColor = loadSettings['chatBgColor']
			AITaskStatusLblBG = loadSettings['AITaskStatusLblBG']
			KCS_IMG = loadSettings['KCS_IMG']
			botChatText = loadSettings['botChatText']
			botChatTextBg = loadSettings['botChatTextBg']
			userChatTextBg = loadSettings['userChatTextBg']
			voice_id = loadSettings['voice_id']
			ass_volume = loadSettings['ass_volume']
			ass_voiceRate = loadSettings['ass_voiceRate']
	except Exception as e:
		pass

if os.path.exists('userData/settings.pck')==False:
	ChangeSettings(True)

def changeTheme():
	global background, textColor, AITaskStatusLblBG, KCS_IMG, botChatText, botChatTextBg, userChatTextBg, chatBgColor
	if themeValue.get()==1:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#203647", "white", "#203647",1
		cbl['image'] = cblDarkImg
		kbBtn['image'] = kbphDark
		settingBtn['image'] = sphDark
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "white", "#007cc7", "#4da8da"
		chatBgColor = "#12232e"
		colorbar['bg'] = chatBgColor
	else:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#F6FAFB", "#303E54", "#14A769", 0
		cbl['image'] = cblLightImg
		kbBtn['image'] = kbphLight
		settingBtn['image'] = sphLight
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
		botChatText, botChatTextBg, userChatTextBg = "#494949", "#EAEAEA", "#23AE79"
		chatBgColor = "#F6FAFB"
		colorbar['bg'] = '#E8EBEF'

	root['bg'], root2['bg'] = background, background
	settingsFrame['bg'] = background
	settingsLbl['fg'], userPhoto['fg'], userName['fg'], assLbl['fg'], voiceRateLbl['fg'], volumeLbl['fg'], themeLbl['fg'], chooseChatLbl['fg'] = textColor, textColor, textColor, textColor, textColor, textColor, textColor, textColor
	settingsLbl['bg'], userPhoto['bg'], userName['bg'], assLbl['bg'], voiceRateLbl['bg'], volumeLbl['bg'], themeLbl['bg'], chooseChatLbl['bg'] = background, background, background, background, background, background, background, background
	s.configure('Wild.TRadiobutton', background=background, foreground=textColor)
	volumeBar['bg'], volumeBar['fg'], volumeBar['highlightbackground'] = background, textColor, background
	chat_frame['bg'], root1['bg'] = chatBgColor, chatBgColor
	userPhoto['activebackground'] = background
	ChangeSettings(True)

def changeVoice(e):
	global voice_id
	voice_id=1
	if assVoiceOption.get()=='Male': voice_id=1
	engine.setProperty('voice', voices[voice_id].id)
	ChangeSettings(True)

def changeVolume(e):
	global ass_volume
	ass_volume = volumeBar.get() / 100
	engine.setProperty('volume', ass_volume)
	ChangeSettings(True)

def changeVoiceRate(e):
	global ass_voiceRate
	temp = voiceOption.get()
	if temp=='Very Low': ass_voiceRate = 100
	elif temp=='Low': ass_voiceRate = 150
	elif temp=='Fast': ass_voiceRate = 250
	elif temp=='Very Fast': ass_voiceRate = 300
	else: ass_voiceRate = 200
	print(ass_voiceRate)
	engine.setProperty('rate', ass_voiceRate)
	ChangeSettings(True)

ChangeSettings()

############################################ SET UP VOICE ###########################################
vi_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
try:
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', vi_voice_id) #AN-Vietnamese
	engine.setProperty('volume', ass_volume)
except Exception as e:
	print(e)


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
	AITaskStatusLbl['text'] = 'Nói...'
	if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)
	if display: attachTOframe(text, True)
	print('\n'+ai_name.upper()+': '+text)
	try:
		engine.say(text)
		engine.runAndWait()
	except:
		print("Cố gắng không gõ thêm...")

####################################### SET UP SPEECH TO TEXT #######################################

def record(clearChat=True, iconDisplay=True):
	print('\nĐang nghe...')
	AITaskStatusLbl['text'] = 'Đang nghe...'
	r = sr.Recognizer()
	r.dynamic_energy_threshold = False
	r.energy_threshold = 4000
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		said = ""
		try:
			AITaskStatusLbl['text'] = 'Xử lý...'
			said = r.recognize_google(audio,language="vi-VN")
			print(f"\nBạn nói: {said}")
			if clearChat:
				clearChatScreen()
			if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(said)
		except Exception as e:
			print(e)
			# speak("I didn't get it, Say that again please...")
			if "connection failed" in str(e):
				speak("Hệ thống của bạn là ngoại tuyến...", True, True)
			return 'None'
	return said.lower()

def voiceMedium():
	while True:
		query = record()
		if query == 'None': continue
		if isContain(query, EXIT_COMMANDS):
			speak("Dừng hệ thống, tạm biệt "+ownerDesignation+"!", True, True)
			break
		else: main(query.lower())
	app_control.Win_Opt('close')

def keyboardInput(e):
	user_input = UserField.get().lower()
	if user_input!="":
		clearChatScreen()
		if isContain(user_input, EXIT_COMMANDS):
			speak("Dừng hệ thống, tạm biệt "+ownerDesignation+"!", True, True)
		else:
			Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(user_input.capitalize())
			Thread(target=main, args=(user_input,)).start()
		UserField.delete(0, END)

###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):
	for word in lst:
		if word in txt:
			return True
	return False

def main(text):	
		if "dự án" in text:
			if isContain(text, ['làm', 'tạo']):				
				speak("Bạn muốn đặt tên dự án là gì ?",)
				projectName = record(False, False)
				speak(file_handler.CreateHTMLProject(projectName.capitalize()), True)
				return

		if "tạo" in text and "tập tin" in text:
			speak(file_handler.createFile(text), True, True)
			return

		if "phiên dịch" in text:
			speak("Bạn muốn dịch gì?", True, True)
			sentence = record(False, False)
			speak("Ngôn ngữ nào để dịch?", True)
			langauage = record(False, False)
			result = normal_chat.lang_translate(sentence, langauage)
			if result=="None": speak("Ngôn ngữ này không tồn tại !")
			else:
				speak(f"Trong {langauage.capitalize()} bạn sẽ nói:", True)
				if langauage=="english":
					attachTOframe(result.text, True)
					speak(result.pronunciation)
				
				else: speak(result.text, True)
			return

		if 'ghi chú' in text:
			if isContain(text, ['thêm', 'tạo', 'làm']):
				speak("Bạn muốn thêm gì?", True, True)
				item = record(False, False)
				todo_handler.toDoList(item)
				speak("Được rồi, tôi đã thêm vào danh sách của bạn!", True)
				return
			if isContain(text, ['hiển thị', 'ghi chú của tôi']):
				items = todo_handler.showtoDoList()
				if len(items)==1:
					speak(items[0], True, True)
					return
				attachTOframe('\n'.join(items), True)
				speak(items[0])
				return

		if isContain(text, ['năng lượng', 'thông tin hệ thống']):
			result = app_control.OSHandler(text)
			if len(result)==2:
				speak(result[0], True, True)
				attachTOframe(result[1], True)
			else:
				speak(result, True, True)
			return
			
		if isContain(text, ['meaning', 'từ điển', 'definition', 'define']):
			result = dictionary.translate(text)
			speak(result[0], True, True)
			if result[1]=='': return
			speak(result[1], True)
			return

		if 'chụp ảnh' in text or ('tự' in text and 'sướng' in text):
			speak("Ok, ảnh của "+ownerDesignation+"đã được lưu lại", True, True)
			clickPhoto()
			speak('Bạn có muốn xem ảnh đã chụp của mình không?', True)
			query = record(False)
			if isContain(query, ['ok', 'đồng ý', 'có', 'hiển thị']):
				Thread(target=viewPhoto).start()
				speak("Ok...", True, True)
			else:
				speak("Không vấn đề gì "+ownerDesignation, True, True)
			return

		if 'âm lượng' in text:
			app_control.volumeControl(text)
			Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)		
			attachTOframe('Cài đặt âm lượng đã thay đổi', True)
			return
			
		if isContain(text, ['hẹn giờ', 'đếm ngược']):
			Thread(target=app_timer.startTimer, args=(text,)).start()
			speak('Ok,hẹn giờ bắt đầu!', True, True)
			return
	
		if 'whatsapp' in text:
			speak("Oke "+ownerDesignation+"...", True, True)
			speak('Bạn muốn gửi tin nhắn cho ai?', True)
			WAEMPOPUP("WhatsApp", "Số điện thoại")
			attachTOframe(rec_phoneno)
			speak('Tin nhắn là gì?', True)
			message = record(False, False)
			Thread(target=web_scrapping.sendWhatsapp, args=(rec_phoneno, message,)).start()
			speak("Tin nhắn đang được gửi, không chuyển màn hình!")
			attachTOframe("Tin nhắn đã gửi", True)
			return

		if 'thư điện tử' in text or 'email' in text:
			speak('Bạn muốn gửi email cho ai?', True, True)
			WAEMPOPUP("Email", "E-mail Address")
			attachTOframe(rec_email)
			speak('Tiêu đề là gì?', True)
			subject = record(False, False)
			speak('Hãy đọc tin nhắn bạn cần gửi?', True)
			message = record(False, False)
			Thread(target=web_scrapping.email,args=(rec_email,message,subject)).start()
			speak("Đã gửi thư thành công!",True)
			return

		if isContain(text, ['covid','dịch bệnh']):
			result = web_scrapping.covid(text)
			if 'str' in str(type(result)):
				speak(result, True, True)
				return
			speak(result[0], True, True)
			result = '\n'.join(result[1])
			attachTOframe(result, True)
			return

		if isContain(text, ['youtube','video']):
			speak("Ok "+ownerDesignation+", đây là video danh cho bạn...", True, True)
			try:
				speak(web_scrapping.youtube(text), True)
			except Exception as e:
				print(e)
				speak("Kết quả mong muốn không tìm thấy!", True)
			return

		if isContain(text, ['tìm kiếm ảnh', 'hình ảnh','ảnh']):
			if 'hiển thị' in text and 'hình ảnh' in text:
				Thread(target=showImages, args=(text,)).start()
				speak('Đây là những hình ảnh...', True, True)
				return
			speak(web_scrapping.googleSearch(text), True, True)
			return
			
		if isContain(text, ['bản đồ', 'chỉ đường','tìm đường','hướng dẫn đường đi']):
			if "chỉ đường" in text or "tìm đường" in text or "hướng dẫn đường đi" in text:
				speak('Vị trí bắt đầu của bạn là gì?', True,True)
				startingPoint = record(False, False)
				speak("Ok "+ownerDesignation+", Bạn muốn đến địa điểm nào?", True)
				destinationPoint = record(False, False)
				speak("Ok "+ownerDesignation+", Xác nhận đoạn đường cần di chuyển...", True)
				try:
					distance = web_scrapping.giveDirections(startingPoint, destinationPoint)
					speak('Khoảng cách của 2 địa điểm trên là:'+ distance, True)
				except:
					speak("Tôi nghĩ rằng vị trí không đúng, hãy thử lại!")
			else:
				web_scrapping.maps(text)
				speak('Bản đồ đang được hiển thị...', True, True)
			return

		if isContain(text, ['giai thừa','logarit','value of','tính','cộng','trừ','nhân','chia','+','x','-','*','/','^','mũ','nhân với','lũy thừa','chia cho','nhị phân','thập lục phân','bát phân','shift','sin ','cos ','tan ']):
			try:
				speak(('Kết quả là: ' + math_function.perform(text)), True, True)
			except Exception as e:
				return
			return

		if "kể chuyện cười" in text or "chuyện cười" in text or "truyện cười" in text:
			speak('Đây là chuyện cười dành cho bạn...', True, True)
			speak(web_scrapping.jokes(), True)
			return

		if isContain(text, ['tin tức']):
			speak('Tin tức mới nhất..', True, True)
			headlines,headlineLinks = web_scrapping.latestNews(2)
			for head in headlines: speak(head, True)
			speak('Bạn có muốn đọc toàn bộ tin tức không?', True)
			text = record(False, False)
			if isContain(text, ["không","không, cảm ơn"]):
				speak("OK"+ownerDesignation, True)
			else:
				speak("Ok "+ownerDesignation+", Mở trình duyệt...", True)
				web_scrapping.openWebsite('https://vnexpress.net/tin-tuc-24h/')
				speak("Bạn có thể đọc toàn bộ tin tức từ trang web này!")
			return

		if isContain(text, ['thời tiết']):
			data = web_scrapping.weather()
			speak('', False, True)
			showSingleImage("weather", data[:-1])
			speak(data[-1])
			return

		if isContain(text, ['lưu màn hình']):
			Thread(target=app_control.Win_Opt, args=('screenshot',)).start()
			speak("Ảnh màn hình đã được chụp lại!", True, True)
			return

		if isContain(text, ['cửa sổ','close that']):
			app_control.Win_Opt(text)
			return

		if isContain(text, ['thẻ']):
			app_control.Tab_Opt(text)
			return

		if isContain(text, ['cài đặt']):
			raise_frame(root2)
			clearChatScreen()
			return

		if isContain(text, ['open','type','save','delete','select','press enter']):
			app_control.System_Opt(text)
			return

		if isContain(text, ['wiki', 'là ai','là gì']):
			Thread(target=web_scrapping.downloadImage, args=(text, 1,)).start()
			speak('Tìm kiếm...', True, True)
			result = web_scrapping.wikiResult(text)
			showSingleImage('wiki')
			speak(result, True)
			return
		
		if isContain(text, ['trò chơi','game']):
			speak("Bạn muốn chơi trò chơi nào?", True, True)
			attachTOframe(game.showGames(), True)
			text = record(False)
			if text=="None":
				speak("Tôi không hiểu bạn nói gì?", True, True)
				return
			if 'trực tuyến' in text:
				speak("Ok "+ownerDesignation+", Hãy chơi một số trò chơi trực tuyến!", True, True)
				web_scrapping.openWebsite('https://www.agame.com/games/mini-games/')
				return
			if isContain(text, ["đừng", "không", "thoát", "trở lại", "không bao giờ"]):
				speak("Không vấn đề "+ownerDesignation+", Chúng ta sẽ chơi vào lần sau", True, True)
			else:
				speak("Ok "+ownerDesignation+", bắt đầu trò chơi " + text, True, True)
				os.system(f"python -c \"from modules import game; game.play('{text}')\"")
			return

		if isContain(text, ['đồng tiền','xúc xắc','die']):
			if "quăng" in text or "lăn" in text or "đổ" in text or 'lật' in text or 'chơi' in text or 'trò chơi' in text: 
				speak("Ok "+ownerDesignation, True, True)
				result = game.play(text)
				if "mặt trước" in result: showSingleImage('mặt trước')
				elif "mặt sau" in result: showSingleImage('mặt sau')
				else: showSingleImage(result[-1])
				speak(result)
				return
		
		if isContain(text, ['giờ','ngày']):
			speak(normal_chat.chat(text), True, True)
			return

		if 'tên của tôi' in text:
			speak('Tên của bạn là: , ' + ownerName, True, True)
			return

		if isContain(text, ['giọng nói']):
			global voice_id
			try:
				if 'nữ' in text: voice_id = 0
				elif 'nam' in text: voice_id = 1
				else:
					if voice_id==0: voice_id=1
					else: voice_id=0
				engine.setProperty('voice', voices[voice_id].id)
				ChangeSettings(True)
				speak("Chào "+ownerDesignation+", Tôi đã thay đổi giọng nói của mình. Tôi có thể giúp gì cho bạn?", True, True)
				assVoiceOption.current(voice_id)
			except Exception as e:
				print(e)
			return

		if isContain(text, ['buổi sáng','buổi tối','buổi chiều']) and 'chào' in text:
			speak(normal_chat.chat("chào"), True, True)
			return
		
		result = normal_chat.reply(text)
		if result != "None": speak(result, True, True)
		else:
			speak("Tôi không biết gì về điều này. Đây là những gì tôi tìm thấy trên web...?", True, True)
			#response = record(False, True)
			#if isContain(response, ["không","không cần thiết"]):
				#speak("Ok "+ownerDesignation, True)
			#else:
				#speak("Đây là những gì tôi tìm thấy trên web...", True, True)
			web_scrapping.googleSearch(text)
		

##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():
	result = messagebox.askquestion('Báo động', 'Bạn có chắc là bạn muốn xóa dữ liệu khuôn mặt của mình không?')
	if result=='no': return
	messagebox.showinfo('Xóa dữ liệu khuôn mặt', 'Khuôn mặt của bạn đã bị xóa\nĐăng ký khuôn mặt bạn một lần nữa để sử dụng!')
	import shutil
	shutil.rmtree('userData')
	root.destroy()

						#####################
						####### GUI #########
						#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text,bot=False):
	if bot:
		botchat = Label(chat_frame,text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=250, font=('Montserrat',12, 'bold'))
		botchat.pack(anchor='w',ipadx=5,ipady=5,pady=5)
	else:
		userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250, font=('Montserrat',12, 'bold'))
		userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)

def clearChatScreen():
	for wid in chat_frame.winfo_children():
		wid.destroy()

### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
	frame.tkraise()
	clearChatScreen()

################# SHOWING DOWNLOADED IMAGES ###############
img0, img1, img2, img3, img4 = None, None, None, None, None
def showSingleImage(type, data=None):
	global img0, img1, img2, img3, img4
	try:
		img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((90,110), Image.Resampling.LANCZOS))
	except:
		pass
	img1 = ImageTk.PhotoImage(Image.open('assets/images/heads.jpg').resize((220,200), Image.Resampling.LANCZOS))
	img2 = ImageTk.PhotoImage(Image.open('assets/images/tails.jpg').resize((220,200), Image.Resampling.LANCZOS))
	img4 = ImageTk.PhotoImage(Image.open('assets/images/WeatherImage.png'))

	if type=="weather":
		weather = Frame(chat_frame)
		weather.pack(anchor='w')
		Label(weather, image=img4, bg=chatBgColor).pack()
		Label(weather, text=data[0], font=('Arial Bold', 45), fg='white', bg='#3F48CC').place(x=65,y=45)
		Label(weather, text=data[1], font=('Montserrat', 15), fg='white', bg='#3F48CC').place(x=78,y=110)
		Label(weather, text=data[2], font=('Montserrat', 10), fg='white', bg='#3F48CC').place(x=78,y=140)
		Label(weather, text=data[3], font=('Arial Bold', 12), fg='white', bg='#3F48CC').place(x=60,y=160)

	elif type=="wiki":
		Label(chat_frame, image=img0, bg='#EAEAEA').pack(anchor='w')
	elif type=="mặt trước":
		Label(chat_frame, image=img1, bg='#EAEAEA').pack(anchor='w')
	elif type=="mặt sau":
		Label(chat_frame, image=img2, bg='#EAEAEA').pack(anchor='w')
	else:
		img3 = ImageTk.PhotoImage(Image.open('assets/images/dice/'+type+'.jpg').resize((200,200), Image.Resampling.LANCZOS))
		Label(chat_frame, image=img3, bg='#EAEAEA').pack(anchor='w')
	
def showImages(query):
	global img0, img1, img2, img3
	web_scrapping.downloadImage(query)
	w, h = 150, 110
	#Showing Images
	imageContainer = Frame(chat_frame, bg='#EAEAEA')
	imageContainer.pack(anchor='w')
	#loading images
	img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((w,h), Image.Resampling.LANCZOS))
	img1 = ImageTk.PhotoImage(Image.open('Downloads/1.jpg').resize((w,h), Image.Resampling.LANCZOS))
	img2 = ImageTk.PhotoImage(Image.open('Downloads/2.jpg').resize((w,h), Image.Resampling.LANCZOS))
	img3 = ImageTk.PhotoImage(Image.open('Downloads/3.jpg').resize((w,h), Image.Resampling.LANCZOS))
	#Displaying
	Label(imageContainer, image=img0, bg='#EAEAEA').grid(row=0, column=0)
	Label(imageContainer, image=img1, bg='#EAEAEA').grid(row=0, column=1)
	Label(imageContainer, image=img2, bg='#EAEAEA').grid(row=1, column=0)
	Label(imageContainer, image=img3, bg='#EAEAEA').grid(row=1, column=1)


############################# WAEM - WhatsApp Email ##################################
def sendWAEM():
	global rec_phoneno, rec_email
	data = WAEMEntry.get()
	rec_email, rec_phoneno = data, data
	WAEMEntry.delete(0, END)
	app_control.Win_Opt('close')
def send(e):
	sendWAEM()

def WAEMPOPUP(Service='None', rec='Reciever'):
	global WAEMEntry
	PopUProot = Tk()
	PopUProot.title(f'{Service} Service')
	PopUProot.configure(bg='white')

	if Service=="WhatsApp": PopUProot.iconbitmap("assets/images/whatsapp.ico")
	else: PopUProot.iconbitmap("assets/images/email.ico")
	w_width, w_height = 410, 200
	s_width, s_height = PopUProot.winfo_screenwidth(), PopUProot.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	PopUProot.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	Label(PopUProot, text=f'Reciever {rec}', font=('Arial', 16), bg='white').pack(pady=(20, 10))
	WAEMEntry = Entry(PopUProot, bd=10, relief=FLAT, font=('Arial', 12), justify='center', bg='#DCDCDC', width=30)
	WAEMEntry.pack()
	WAEMEntry.focus()

	SendBtn = Button(PopUProot, text='Send', font=('Arial', 12), relief=FLAT, bg='#14A769', fg='white', command=sendWAEM)
	SendBtn.pack(pady=20, ipadx=10)
	PopUProot.bind('<Return>', send)
	PopUProot.mainloop()

######################## CHANGING CHAT BACKGROUND COLOR #########################
def getChatColor():
	global chatBgColor
	myColor = colorchooser.askcolor()
	if myColor[1] is None: return
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor
	ChangeSettings(True)

chatMode = 1
def changeChatMode():
	global chatMode
	if chatMode==1:
		# appControl.volumeControl('mute')
		VoiceModeFrame.pack_forget()
		TextModeFrame.pack(fill=BOTH)
		UserField.focus()
		chatMode=0
	else:
		# appControl.volumeControl('full')
		TextModeFrame.pack_forget()
		VoiceModeFrame.pack(fill=BOTH)
		root.focus()
		chatMode=1

############################################## GUI #############################################

def onhover(e):
	userPhoto['image'] = chngPh
def onleave(e):
	userPhoto['image'] = userProfileImg

def UpdateIMAGE():
	global ownerPhoto, userProfileImg, userIcon

	os.system('python modules/avatar_selection.py')
	u = UserData()
	u.extractData()
	ownerPhoto = u.getUserPhoto()
	userProfileImg = ImageTk.PhotoImage(Image.open("assets/images/avatars/a"+str(ownerPhoto)+".png").resize((120, 120)))

	userPhoto['image'] = userProfileImg
	userIcon = PhotoImage(file="assets/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")

def SelectAvatar():	
	Thread(target=UpdateIMAGE).start()


#####################################  MAIN GUI ####################################################

#### SPLASH/LOADING SCREEN ####
def progressbar():
	s = ttk.Style()
	s.theme_use('clam')
	s.configure("white.Horizontal.TProgressbar", foreground='white', background='white')
	progress_bar = ttk.Progressbar(splash_root,style="white.Horizontal.TProgressbar", orient="horizontal",mode="determinate", length=303)
	progress_bar.pack()
	splash_root.update()
	progress_bar['value'] = 0
	splash_root.update()
 
	while progress_bar['value'] < 100:
		progress_bar['value'] += 5
		# splash_percentage_label['text'] = str(progress_bar['value']) + ' %'
		splash_root.update()
		sleep(0.1)

def destroySplash():
	splash_root.destroy()

if __name__ == '__main__':
	splash_root = Tk()
	splash_root.configure(bg='#3895d3')
	splash_root.overrideredirect(True)
	splash_label = Label(splash_root, text="Xử lý...", font=('montserrat',15),bg='#3895d3',fg='white')
	splash_label.pack(pady=40)
	# splash_percentage_label = Label(splash_root, text="0 %", font=('montserrat',15),bg='#3895d3',fg='white')
	# splash_percentage_label.pack(pady=(0,10))

	w_width, w_height = 400, 200
	s_width, s_height = splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	splash_root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30))

	progressbar()
	splash_root.after(10, destroySplash)
	splash_root.mainloop()	

	root = Tk()
	root.title('Trợ Lý VKU')
	w_width, w_height = 400, 650
	s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	root.configure(bg=background)
	# root.resizable(width=False, height=False)
	root.pack_propagate(0)

	root1 = Frame(root, bg=chatBgColor)
	root2 = Frame(root, bg=background)
	root3 = Frame(root, bg=background)

	for f in (root1, root2, root3):
		f.grid(row=0, column=0, sticky='news')	
	
	################################
	########  CHAT SCREEN  #########
	################################

	#Chat Frame
	chat_frame = Frame(root1, width=380,height=551,bg=chatBgColor)
	chat_frame.pack(padx=10)
	chat_frame.pack_propagate(0)

	bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
	bottomFrame1.pack(fill=X, side=BOTTOM)
	VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	VoiceModeFrame.pack(fill=BOTH)
	TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	TextModeFrame.pack(fill=BOTH)

	# VoiceModeFrame.pack_forget()
	TextModeFrame.pack_forget()

	cblLightImg = PhotoImage(file='assets/images/centralButton.png')
	cblDarkImg = PhotoImage(file='assets/images/centralButton1.png')
	if KCS_IMG==1: cblimage=cblDarkImg
	else: cblimage=cblLightImg
	cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
	cbl.pack(pady=17)
	AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG, font=('montserrat', 16))
	AITaskStatusLbl.place(x=140,y=32)
	
	#Settings Button
	sphLight = PhotoImage(file = "assets/images/setting.png")
	sphLight = sphLight.subsample(2,2)
	sphDark = PhotoImage(file = "assets/images/setting1.png")
	sphDark = sphDark.subsample(2,2)
	if KCS_IMG==1: sphimage=sphDark
	else: sphimage=sphLight
	settingBtn = Button(VoiceModeFrame,image=sphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf",command=lambda: raise_frame(root2))
	settingBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Keyboard Button
	kbphLight = PhotoImage(file = "assets/images/keyboard.png")
	kbphLight = kbphLight.subsample(2,2)
	kbphDark = PhotoImage(file = "assets/images/keyboard1.png")
	kbphDark = kbphDark.subsample(2,2)
	if KCS_IMG==1: kbphimage=kbphDark
	else: kbphimage=kbphLight
	kbBtn = Button(VoiceModeFrame,image=kbphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	kbBtn.place(x=25, y=30)

	#Mic
	micImg = PhotoImage(file = "assets/images/mic.png")
	micImg = micImg.subsample(2,2)
	micBtn = Button(TextModeFrame,image=micImg,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	micBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Text Field
	TextFieldImg = PhotoImage(file='assets/images/textField.png')
	UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
	UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
	UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
	UserField.place(x=20, y=30)
	UserField.insert(0, "Hỏi tôi bất cứ điều gì...")
	UserField.bind('<Return>', keyboardInput)
	
	#User and Bot Icon
	userIcon = PhotoImage(file="assets/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")
	botIcon = PhotoImage(file="assets/images/assistant2.png")
	botIcon = botIcon.subsample(2,2)
	

	###########################
	########  SETTINGS  #######
	###########################

	settingsLbl = Label(root2, text='Cài đặt', font=('Arial Bold', 15), bg=background, fg=textColor)
	settingsLbl.pack(pady=10)
	separator = ttk.Separator(root2, orient='horizontal')
	separator.pack(fill=X)
	#User Photo
	userProfileImg = Image.open("assets/images/avatars/a"+str(ownerPhoto)+".png")
	userProfileImg = ImageTk.PhotoImage(userProfileImg.resize((120, 120)))
	userPhoto = Button(root2, image=userProfileImg, bg=background, bd=0, relief=FLAT, activebackground=background, command=SelectAvatar)
	userPhoto.pack(pady=(20, 5))

	#Change Photo
	chngPh = ImageTk.PhotoImage(Image.open("assets/images/avatars/changephoto2.png").resize((120, 120)))
	
	userPhoto.bind('<Enter>', onhover)
	userPhoto.bind('<Leave>', onleave)

	#Username
	userName = Label(root2, text=ownerName, font=('Arial Bold', 15), fg=textColor, bg=background)
	userName.pack()

	#Settings Frame
	settingsFrame = Frame(root2, width=300, height=300, bg=background)
	settingsFrame.pack(pady=20)

	assLbl = Label(settingsFrame, text='Giọng trợ lý', font=('Arial', 13), fg=textColor, bg=background)
	assLbl.place(x=0, y=20)
	n = StringVar()
	assVoiceOption = ttk.Combobox(settingsFrame, values=('Female', 'Male'), font=('Arial', 13), width=13, textvariable=n)
	assVoiceOption.current(voice_id)
	assVoiceOption.place(x=150, y=20)
	assVoiceOption.bind('<<ComboboxSelected>>', changeVoice)

	voiceRateLbl = Label(settingsFrame, text='Tốc độ âm lượng', font=('Arial', 13), fg=textColor, bg=background)
	voiceRateLbl.place(x=0, y=60)
	n2 = StringVar()
	voiceOption = ttk.Combobox(settingsFrame, font=('Arial', 13), width=13, textvariable=n2)
	voiceOption['values'] = ('Very Low', 'Low', 'Normal', 'Fast', 'Very Fast')
	voiceOption.current(ass_voiceRate//50-2) #100 150 200 250 300
	voiceOption.place(x=150, y=60)
	voiceOption.bind('<<ComboboxSelected>>', changeVoiceRate)
	
	volumeLbl = Label(settingsFrame, text='Âm lượng', font=('Arial', 13), fg=textColor, bg=background)
	volumeLbl.place(x=0, y=105)
	volumeBar = Scale(settingsFrame, bg=background, fg=textColor, sliderlength=30, length=135, width=16, highlightbackground=background, orient='horizontal', from_=0, to=100, command=changeVolume)
	volumeBar.set(int(ass_volume*100))
	volumeBar.place(x=150, y=85)



	themeLbl = Label(settingsFrame, text='Nền', font=('Arial', 13), fg=textColor, bg=background)
	themeLbl.place(x=0,y=143)
	themeValue = IntVar()
	s = ttk.Style()
	s.configure('Wild.TRadiobutton', font=('Arial Bold', 10), background=background, foreground=textColor, focuscolor=s.configure(".")["background"])
	darkBtn = ttk.Radiobutton(settingsFrame, text='Tối', value=1, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	darkBtn.place(x=150,y=145)
	lightBtn = ttk.Radiobutton(settingsFrame, text='Sáng', value=2, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
	lightBtn.place(x=230,y=145)
	themeValue.set(1)
	if KCS_IMG==0: themeValue.set(2)


	chooseChatLbl = Label(settingsFrame, text='Nền Chat', font=('Arial', 13), fg=textColor, bg=background)
	chooseChatLbl.place(x=0,y=180)
	cimg = PhotoImage(file = "assets/images/colorchooser.png")
	cimg = cimg.subsample(3,3)
	colorbar = Label(settingsFrame, bd=3, width=18, height=1, bg=chatBgColor)
	colorbar.place(x=150, y=180)
	if KCS_IMG==0: colorbar['bg'] = '#E8EBEF'
	Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)

	backBtn = Button(settingsFrame, text='   Trở lại   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=lambda:raise_frame(root1))
	clearFaceBtn = Button(settingsFrame, text='   Xóa dữ liệu   ', bd=0, font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=deleteUserData)
	backBtn.place(x=5, y=250)
	clearFaceBtn.place(x=120, y=250)

	try:
		# pass
		Thread(target=voiceMedium).start()
	except:
		pass
	try:
		# pass
		Thread(target=web_scrapping.dataUpdate).start()
	except Exception as e:
		print('Hệ thống ngoại tuyến...')
	
	root.iconbitmap('assets/images/assistant2.ico')
	raise_frame(root1)
	root.mainloop()