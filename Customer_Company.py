import random
import re
import datetime
# -*- coding: utf-8 -*-
bdate = datetime.date(2011, 4,5)
customer_id = 0
person_id = 0
person_file = open('Person.sql', 'w+')
customer_file = open('Customer.sql', 'w+')
def prepare_script():
	t = ['Person','Customer']
	identity = 'set identity_insert [dbo].['
	identity2 = '] on;'
	print('set nocount on;', file = person_file)
	print('set nocount on;', file = customer_file)
	print(identity + t[0] +identity2, file = person_file)
	print(identity + t[1] +identity2, file = customer_file)
def create_names(names, surnames, n):
	result = []
	for name in names:
		for sname in surnames:
			result.append((name, sname))
	return result

def cin_list(n):
	lista = []
	for i in range(0,n):
		myString = ' '
		input(myString)
		lista.append(myString)
	return cin_list

def create_mails(fullnames, hosts):
	s = set()
	l = list()
	for n in fullnames:
		name = ogonki(n[0])[0:5] + '.' + ogonki(n[1])[0:8]
		name2 = name[0:12]
		mail2 = None
		for h in hosts:
			mail = name2.lower() + h
			if mail not in s:
				mail2 = mail
				break
		if mail2 != None:
			l.append((n[0], n[1], mail2))
			s.add(mail2)

	return (l, s)

def create_corp_mails(companies, hosts, s):
	l = list()
	for c in companies:
		name = ogonki(c)[0:10]
		mail2 = None
		for h in hosts:
			mail = name + h
			if mail not in s:
				mail2 = mail
				break
		if mail2 != None:
			l.append((c, mail2))
			s.add(mail2)
	return l

def read_make_names():
	male_firstnames = open("faceci_imiona.csv").read().splitlines()
	male_surnames = open("faceci_nazwiska.csv").read().splitlines()
	famale_firstnames = open("kobiety_imiona.csv").read().splitlines()
	famale_surnames = open("kobiety_nazwiska.csv").read().splitlines()
	male_data1 = create_names(male_firstnames, male_surnames, 10000)
	famale_data1 = create_names(famale_firstnames, famale_surnames, 2000)
	names = random.sample(male_data1, 5000) + random.sample(famale_data1, 1000)
	names += random.sample(names, 5000)
	names += random.sample(names, 1000)
	names += random.sample(names, 1000)
	return names

def create_phones(data, nr):
	res = []
	for d in data:
		nr += 1
		number = str(nr)
		first = number[0:3]
		second = number[3:6]
		third = number[6:9]
		phone = '+48-' + first + '-' + second + '-' + third
		tup = d + (phone,)
		res.append(tup)
	return res


def insert_name(data):
	# Name Tuple: (FirstName, LastName, Email, Phone)
	global customer_id
	customer_id = 0
	query1 = 'INSERT INTO Customer (CustomerID, Phone, Email) VALUES ('
	query2 = 'INSERT INTO Individual (FirstName, LastName, CustomerID) VALUES ('
	for tup in data:
		customer_id += 1
		c_id = customer_id
		str1 = str(c_id) + ' ,\'' + tup[3] + '\' , \'' + tup[2] + '\''
		str2 = '\'' + tup[0] + '\' , \'' + tup[1] + '\' , ' + str(c_id)
		print (query1 + str1 + ')', file = customer_file)
		print (query2 + str2 + ')', file = customer_file)

def insert_company(data):
	# Name Tuple: (FirstName, LastName, Email, Phone)
	global customer_id
	query1 = 'INSERT INTO [dbo].[Customer] (CustomerID, Phone, Email) VALUES ('
	query2 = 'INSERT INTO [dbo].[Company] (CompanyName, CustomerID) VALUES ('
	for tup in data:
		customer_id += 1
		c_id = customer_id
		str1 = str(c_id) + ' ,\'' + tup[2] + '\' , \'' + tup[1] + '\')'
		str2 = '\'' + tup[0] + '\' , ' + str(c_id) + ' )'
		print (query1 + str1, file = customer_file)
		print (query2 + str2, file = customer_file)

def ogonki(word):
	word = word.lower()
	exp = [(r'ą','a'), (r'ę','a'), (r'ć','c'),(r'ł','l'),(r'ń','n'), (r'ó','o'), (r'ś','s'), (r'ż','z'), (r'ź','z')]
	for e in exp:
		word = re.sub(e[0], e[1], word)
	word = re.sub('\W', '', word)
	return word

def get_student(_id, doc_id, s_id):
	student = 'INSERT INTO [dbo].[Student] (IDCard, PersonID, ValidFrom, ValidUntil) VALUES ('
	doc_id = doc_id[s_id]
	from_date = bdate + datetime.timedelta(days = random.randint(1, 400))
	until_date = from_date + datetime.timedelta(days = random.randint(400, 800))
	print (student + str(doc_id) + ',' + str(_id) + ',\'' + from_date.isoformat() +'\',\'' + until_date.isoformat() + '\')', file = person_file)


def insert_person(data):
	_id = 0
	details = ['Computer Scientist', 'Intern', 'Graphics Designer', 'Software Developer', 'Geek', 'Software Engeneer', 'Manager', 'CEO', 'CTO']
	for i in range(len(details)):
		details += details[0:len(details)-i]
	query1 = 'INSERT INTO [dbo].[Person] (PersonID, FirstName, LastName, PersonalDetails, Phone, Mail) VALUES ('
	doc_id = random.sample(range(11111,88888), 150)
	s_id = 0
	for tup in data:
		_id += 1
		str1 = str(_id) + ' ,\'' + tup[0] + '\' , \'' + tup[1] + '\',\'' +  random.choice(details) + '\'' 
		str2 = ',\'' + tup[3] + '\' , \'' + tup[2] + '\'' + ')'
		print (query1 + str1 + str2, file = person_file)
		if _id % 100 == 0:
			get_student(_id, doc_id, s_id)
			s_id += 1

def __main__():
	prepare_script()
	hosts = ['@gmail.com', '@outlook.com', '@live.com', '@yahoo.com', '@mail.com', '@inbox.com']
	names = read_make_names()
	companies = open('firmy.csv').read().splitlines()
	names = random.sample(names + names + names, 16000)
	creator1 = create_mails(names, hosts)
	creator2 = create_corp_mails(companies, hosts, creator1[1])
	Person = create_phones(creator1[0], 123456789)
	Company = create_phones(creator2, 456132798)
	Individual = random.sample(Person, 150)
	Person = random.sample(Person, 15000)
	random.shuffle(Company)
	random.shuffle(Individual)
	random.shuffle(Person)
	insert_name(Individual)
	insert_company(Company)
	insert_person(Person)
	print ('--Person ' + str(len(Person)))
	print ('--Customer' + str(len(Company) + len(Individual)))

__main__()