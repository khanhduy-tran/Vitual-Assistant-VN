from difflib import get_close_matches
import json
from random import choice

data = json.load(open('assets/dict_vi.json', encoding='utf-8'))

def getMeaning(word):
	if word in data:
		return word, data[word], 1
	elif len(get_close_matches(word, data.keys())) > 0:
		word = get_close_matches(word, data.keys())[0]
		return word, data[word], 0
	else:
		return word, ["Từ này không tồn tại trong từ điển"], -1

def translate(query):
	query = query.replace('từ điển', '')
	if 'nghĩa' in query:
		ind = query.index('nghĩa là')
		word = query[ind+10:].strip().lower()
	elif 'xác định' in query:
		try:
			ind = query.index('định nghĩa')
			word = query[ind+13:].strip().lower()
		except:
			ind = query.index('xác định')
			word = query[ind+10:].strip().lower()
	else: word = query

	word, result, check = getMeaning(word)
	result = choice(result)

	if check==1:
		return ["Đây là định nghĩa của \"" +word.capitalize()+ '"', result]
	elif check==0:
		return ["Tôi nghĩ bạn đang tìm kiếm \"" +word.capitalize()+ '"', "Định nghĩa của nó là,\n" + result]
	else:
		return [result, '']
