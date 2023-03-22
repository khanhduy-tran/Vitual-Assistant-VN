from datetime import datetime
import os
file = "userData/toDoList.txt"

def createList():
	f = open(file,"w",encoding='utf-8')
	present = datetime.now()
	dt_format = present.strftime("Date: " + "%d/%m/%Y"+ " Time: " + "%H:%M:%S" + "\n")
	f.write(dt_format)
	f.close()

def toDoList(text):
	if os.path.isfile(file) == False:
		createList()

	f = open(file,"r",encoding='utf-8')
	x = f.read(8)
	f.close()
	y = x[6:]
	yesterday = int(y)
	present = datetime.now()
	today = int(present.strftime("%d"))
	if (today-yesterday) >= 1:
		createList()
	f = open(file,"a",encoding='utf-8')
	dt_format = present.strftime("%H:%M")
	print(dt_format)
	f.write(f"[{dt_format}] : {text}\n")
	f.close()

def showtoDoList():
	if os.path.isfile(file)==False:
		return ["Danh sách ghi chú trống!"]
	
	f = open(file, 'r',encoding='utf-8')
	
	items = []
	for line in f.readlines():
		items.append(line.strip())

	speakList = [f"Bạn có {len(items)-1} ghi chú trong danh sách:\n"]
	for i in items[1:]:
		speakList.append(i.capitalize())
	return speakList
