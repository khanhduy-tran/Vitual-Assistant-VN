import math

def basicOperations(text):
	if 'root' in text:
		temp = text.rfind(' ')
		num = int(text[temp+1:])
		return round(math.sqrt(num),2)

	text = text.replace('cộng', '+')
	text = text.replace('trừ', '-')
	text = text.replace('nhân', '*')
	text = text.replace('x', '*')
	text = text.replace('nhân với', '*')
	text = text.replace('bội', '*')
	text = text.replace('chia', '/')
	text = text.replace('bình phương', '**')
	text = text.replace('lũythừa', '**')
	text = text.replace('^', '**')
	text = text.replace('mũ', '**')
	text = text.replace(' ', '')
	result = eval(text)
	return round(result,2)

def bitwiseOperations(text):
	if 'sang phải' in text or 'dịch phải' in text or 'right' in text:
		temp = text.rfind(' ')
		num = int(text[temp+1:])
		return num>>1
	elif 'sang trái' in text or 'dịch trái' in text or 'left' in text:
		temp = text.rfind(' ')
		num = int(text[temp+1:])
		return num<<1
	text = text.replace('and', '&')
	text = text.replace('or', '|')
	text = text.replace('not of', '~')
	text = text.replace('not', '~')
	text = text.replace('xor', '^')
	result = eval(text)
	return result

def conversions(text):
	temp = text.rfind(' ')
	num = int(text[temp+1:])
	if 'nhị phân' in text or 'bin' in text:
		return eval('bin(num)')[2:]
	elif 'thập lục phân' in text or 'hex' in text:
		return eval('hex(num)')[2:]
	elif 'bát phân' in text or 'oct' in text:
		return eval('oct(num)')[2:]

def trigonometry(text):
	temp = text.replace('độ','')
	temp = text.rfind(' ')
	deg = int(text[temp+1:])
	rad = (deg * math.pi) / 180
	if 'sin' in text:
		return round(math.sin(rad),2)
	elif 'cos' in text:
		return round(math.cos(rad),2)
	elif 'tan' in text:
		return round(math.tan(rad),2)

def factorial(n):
	if n==1 or n==0: return 1
	else: return n*factorial(n-1)

def logFind(text):
	temp = text.rfind(' ')
	num = int(text[temp+1:])
	return round(math.log(num,10),2)

def isHaving(text, lst):
	for word in lst:
		if word in text:
			return True
	return False

def perform(text):
	text = text.replace('tính','')
	text = text.replace('Tính','')
	text = text.replace(' ','')
	if "giai thừa" in text or '!' in text: return str(factorial(int(text[text.rfind(' ')+1:])))
	elif isHaving(text, ['sin','cos','tan']): return str(trigonometry(text))
	elif isHaving(text, ['nhị phân','thập lục phân','bát phân','bin','hex','oct']): return str(conversions(text))
	elif isHaving(text, ['shift','and','or','not']): return str(bitwiseOperations(text))
	elif 'lôgarit' in text or 'log' in text or 'logarit' in text: return str(logFind(text))
	else: return str(basicOperations(text))

# print(round(math.log(1,10),2))