from random import *
import playsound
from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
import speech_recognition as sr
import pyttsx3
import time
from pynput.keyboard import Key, Controller
vi_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
def closeWindow():
	keyboard = Controller()
	keyboard.press(Key.alt_l)
	keyboard.press(Key.f4)
	keyboard.release(Key.f4)
	keyboard.release(Key.alt_l)

try:
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', vi_voice_id) #male
	engine.setProperty('volume', 1)
except Exception as e:
	print(e)

def speak(text):
	print(text)
	engine.say(text)
	engine.runAndWait()

def record():
	global userchat
	userchat['text'] = "Đang nghe..."
	r = sr.Recognizer()
	r.dynamic_energy_threshold = False
	r.energy_threshold = 4000
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		said = ""
		try:
			said = r.recognize_google(audio,language="vi-VN")
			print(f"\nBạn nói: {said}")
		except Exception as e:
			print(e)
			speak("Tôi nghĩ đó là di chuyển không hợp lệ...")
			return "None"	
	return said.lower()

moves = ['búa', 'bao', 'kéo']
class RockPaperScissor:
	def __init__(self):
		self.playerScore = 0
		self.botScore = 0
		self.total_moves = 0
		self.intro()

	def intro(self):
		speak("Chào mừng bạn đến với trò chơi Kéo Búa Bao. Để dừng trận đấu, nói dừng lại hoặc hủy bỏ. Hãy bắt đầu!")

	def nextMove(self, move):
		global userchat, botchat, totalLabel, botMoveLBL
		userchat['text'] = move.upper()
		botMove = randint(0,2)
		playerMove = moves.index(move)
		botchat['text'] = moves[botMove].upper()
		self.total_moves += 1

		if botMove==playerMove:
			self.botScore += 1
			self.playerScore += 1
		elif botMove==0:
			if playerMove==1:
				self.playerScore += 1
			else:
				self.botScore += 1
		elif botMove==1:
			if playerMove==2:
				self.playerScore += 1
			else:
				self.botScore += 1
		else:
			if playerMove==0:
				self.playerScore += 1
			else:
				self.botScore += 1
		totalLabel['text'] = str(self.botScore)+'   |   '+str(self.playerScore)
		if botMove==0: botMoveLBL['image'] = rockImg
		if botMove==1: botMoveLBL['image'] = paperImg
		if botMove==2: botMoveLBL['image'] = scissorImg
		speak('Tôi chọn: ' + str(moves[botMove]))
		return botMove+1

	def whoWon(self):
		result = ""
		if self.playerScore == self.botScore:
			result = "Trận đầu hòa !\n"
		elif self.playerScore > self.botScore:
			result = "Bạn đã thắng, rất tốt !\n"
		else:
			result = "Bạn đã thua, hãy bắt đầu lại !\n"
		for el in root.winfo_children():
			el.destroy()
		if 'thắng' in result:
			Label(root, image=winImg).pack(pady=30)
		elif 'thua' in result:
			Label(root, image=loseImg).pack(pady=30)
		else:
			Label(root, image=drawImg).pack(pady=30)
		result += "Bạn đã thắng " +str(self.playerScore)+"/"+str(self.total_moves)+" điểm."
		Label(root, text='Điểm', font=('Arial Bold', 50), fg='#FE8A28', bg='white').pack()
		Label(root, text=str(self.playerScore)+' / '+str(self.total_moves), font=('Arial Bold', 40), fg='#292D3E', bg='white').pack()
		speak(result)
		time.sleep(1)
		closeWindow()
		return

rockImg, paperImg, scissorImg, userchat, botchat, totalLabel, botMoveLBL, userMoveLBL, winImg, loseImg, drawImg = None, None, None, None, None, None, None, None, None, None, None
def playRock():
	rp = RockPaperScissor()
	while True:
		global botMoveLBL, userMoveLBL
		move = record()
		if isContain(move, ["không", "quay lại", "dừng lại","hủy bỏ"]):
			rp.whoWon()
			break
		else:
			img = None
			if 'búa' in move:
				userMoveLBL['image'] = rockImg
				img = rp.nextMove('búa')
			elif 'bao' in move:
				userMoveLBL['image'] = paperImg
				img = rp.nextMove('bao')
			elif 'kéo' in move or 'caesar' in move:
				userMoveLBL['image'] = scissorImg
				img = rp.nextMove('kéo')


def rockPaperScissorWindow():
	global root, rockImg, paperImg, scissorImg, userchat, botchat, totalLabel, botMoveLBL, userMoveLBL, winImg, loseImg, drawImg
	root = Tk()
	root.title('Kéo Búa Bao')
	# root.resizable(0,0)
	# root.attributes('-toolwindow', True)
	w_width, w_height = 400, 650
	s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	root.configure(bg='white')

	rockImg = ImageTk.PhotoImage(Image.open('assets/images/rps/1.jpg'))
	paperImg = ImageTk.PhotoImage(Image.open('assets/images/rps/2.jpg'))
	scissorImg = ImageTk.PhotoImage(Image.open('assets/images/rps/3.jpg'))
	grayImg = ImageTk.PhotoImage(Image.open('assets/images/rps/grayQuestion.png'))
	orangeImg = ImageTk.PhotoImage(Image.open('assets/images/rps/orangeQuestion.jpg'))
	winImg = ImageTk.PhotoImage(Image.open('assets/images/rps/win.jpg'))
	loseImg = ImageTk.PhotoImage(Image.open('assets/images/rps/lose.jpg'))
	drawImg = ImageTk.PhotoImage(Image.open('assets/images/rps/draw.jpg'))

	toplbl = Label(root, text='Tổng điểm', font=('Arial Bold', 20), fg='#FE8A28', bg='white').pack()
	totalLabel = Label(root, text='0   |   0', font=('Arial Bold', 15), fg='#1F1F1F', bg='white')
	totalLabel.pack()
	#bottom image
	img = ImageTk.PhotoImage(Image.open('assets/images/rps/rockPaperScissor.jpg'))
	downLbl = Label(root, image=img)
	downLbl.pack(side=BOTTOM)
	
	#user response
	userchat = Label(root, text='Đang nghe...', bg='#FE8A28', fg='white', font=('Arial Bold',13))
	userchat.place(x=300, y=120)
	userMoveLBL = Label(root, image=orangeImg)
	userMoveLBL.place(x=260, y=150)

	#bot response
	botchat = Label(root, text='Hãy đợi...', bg='#EAEAEA', fg='#494949', font=('Arial Bold',13))
	botchat.place(x=12, y=120)
	botMoveLBL = Label(root, image=grayImg)
	botMoveLBL.place(x=12, y=150)

	Thread(target=playRock).start()
	root.iconbitmap("assets/images/game.ico")
	root.mainloop()

def isContain(text, lst):
	for word in lst:
		if word in text:
			return True
	return False


def play(gameName):
	speak('')
	if isContain(gameName, ['xúc xắc','die']):
		playsound.playsound('assets/audios/dice.mp3')
		result = "Bạn có " + str(randint(1,6))
		return result

	elif isContain(gameName, ['đồng tiền']):
		playsound.playsound('assets/audios/coin.mp3')
		p = randint(-10,10)
		if p>0: return "Bạn vừa lật được mặt trước"
		else: return "Bạn vừa lật được mặt sau"

	elif isContain(gameName, ['đá','giấy','kéo','first']):
		rockPaperScissorWindow()
		return
	
	else:
		print("Trò chơi không có sẵn!")


def showGames():
	return "1. Kéo Búa Bao\n2. Trò chơi trực tuyến"
	