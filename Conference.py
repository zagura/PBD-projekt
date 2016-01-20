import datetime
import random
import decimal
# -*- coding: utf-8 -*-

'''
	Additional data
	CustomersID's range(1,473)
	Person's range(1,15001)
'''

conference_day_id = 0
conference_day_reservation_id = 0
workshop_enrollment_id = 0
participant_id = 0
workshop_id = 0
conference_file = open('Conference.sql', 'w+')
ConferenceDay_file = open('ConferenceDay.sql', 'w+')
Workshop_file = open('Workshop.sql', 'w+')
ConfernceDayReservation_file = open('ConfernceDayReservation.sql', 'w+')
WorkshopEnrollment_file = open('WorkshopEnrollment.sql', 'w+')
Participants_file = open('Participants.sql', 'w+')
Price_file = open('Price.sql', 'w+')
Payment_file = open('Payment.sql', 'w+')
ConferenceDayReservation_file = open('ConferenceDayReservation.sql', 'w+')
WorkshopParticipants_file = open('WorkshopParticipants.sql', 'w+')


def read_file():
	return open("konferencje.csv").read().splitlines()

def get_decimals():
	dis = []
	for i in range(10):
		dec = decimal.Decimal(i)
		dis.append(dec/20)
	return dis

def preapre_script():
	t = ['Conference', 'ConfernceDay', 'Workshop', 'ConfernceDayReservation']
	t += ['WorkshopEnrollment', 'Participants']
	id1 = 'set identity_insert [dbo].['
	id2 = '] on;'
	print(id1 + t[0] + id2, file = conference_file)
	print(id1 + t[1] + id2, file = ConferenceDay_file)
	print(id1 + t[2] + id2, file = Workshop_file)
	print(id1 + t[3] + id2, file = ConfernceDayReservation_file)
	print(id1 + t[4] + id2, file = WorkshopEnrollment_file)
	print(id1 + t[5] + id2, file = Participants_file)

def __main__():
	preapre_script()
	global conference_day_id
	global conference_day_reservation_id
	global workshop_enrollment_id
	global participant_id
	global workshop_id
	bdate = datetime.date(2013,1,1)
	conf_names = read_file()
	confs = []
	confs_days = []
	index = 0
	m_query = 'INSERT INTO [dbo].[Conference] (ConferenceID, BeginDate, EndDate, ConferenceName) \n\tVALUES ('
	days = 0
	for m in range(1,76):
		index += 1
		months = m / 2
		months *= 30
		base_date = bdate + datetime.timedelta(days = months)
		begin_date = base_date +  datetime.timedelta(random.randint(1,24))
		duration = random.randint(1,4)
		end_date = begin_date + datetime.timedelta(days = duration - 1)
		name = conf_names[m]
		c_val = str(m) +  ' , '
		c_val += '\'' + str(begin_date) + '\' , '
		c_val += '\'' + str(end_date) + '\' , '
		c_val += '\'' + name + '\' )'
		print (m_query + c_val, file = conference_file)
		conf_id = index
		create_days(conf_id, begin_date, duration, days, name)
		days += duration

def make_decimals(lista):
	res = []
	for d in lista:
		res += [decimal.Decimal(d)]
	return res

def create_days(conf_id, begin_date, duration, days, conf_name):
	global conference_day_id
	query = 'INSERT INTO [dbo].[ConferenceDay] (DayID, ParticipantsLimit, StudentDiscount, ConferenceID, Date) \n\tVALUES ('
	student_dicounts = get_decimals()
	limits = [120,150,200,250]
	day = days
	for i in range(duration):
		conference_day_id += 1
		__id = conference_day_id
		day += 1
		date = begin_date + datetime.timedelta(i)
		limit = random.choice(limits)
		discount = random.choice(student_dicounts)
		val = str(__id) + ' , '
		val += str(limit) + ' , ' + str(discount) + ' , '
		val += str(conf_id) + ' , \'' + str(date) + '\')'
		print (query + val, file = ConferenceDay_file)
		prices = create_prices(day, date)
		enroll = get_workshops(day, date, conf_name)
		create_reservations(prices, enroll, limit, discount, date)

def get_workshops(day_id, date, conf_name):
	# Return value is a list of tuples (workshop_id, limit, day_id, price) for every workshop
	w_limits = [30,50,60,120]
	w_prices = [50, 70, 125, 45]	
	hours = [10,12,15,17]
	duration = [1,2,3]
	_id = (day_id - 1)*4
	query = 'INSERT INTO [dbo].[Workshop] (WorkshopID, BeginTime, EndTime, ParticipantsLimit, Price, ConferenceDayID, WorkshopName) \n\tVALUES ('
	enroll = []
	global workshop_id
	for i in range(4):
		workshop_id += 1
		w__id = workshop_id
		begintime = datetime.datetime.combine(date, datetime.time(hour = random.choice(hours)))
		endtime = begintime + datetime.timedelta(hours = random.choice(duration))
		price = random.choice(w_prices)
		limit = random.choice(w_limits)
		val = str(w__id) + ' , '
		val += '\'' + str(begintime) + '\' , '   #BeginTime
		val += '\'' + str(endtime) + '\' , '	#EndTime
		val += str(limit) + ' , '				#ParticipantsLimit
		val += str(price) + ' , '				#Price
		val += str(day_id) + ' , '
		val += '\'' + conf_name + '  (' + str(w__id) + ')\''
		val += ')'
		print (query + val, file = Workshop_file)
		enroll += [(w__id, limit, day_id, price)]
	return enroll

def create_prices(day_id, date):
	deltas = [7,14,21,25]
	prices = [50, 70, 100 , 200, 300, 400, 600, 800]
	prices = make_decimals(prices)
	delta = random.choice(deltas)
	d1 = datetime.timedelta(days = delta*(-4))
	d2 = datetime.timedelta(days = delta)
	delta = delta / 2
	d3 = datetime.timedelta(days = delta)
	date1 = date + d1
	date2 = date1 + d2
	date3 = date2 + d3
	date4 = date3 + d3
	dates = [date1, date2, date3, date4, date]
	index = random.randint(0, 4)
	result = []
	query = 'INSERT INTO [dbo].[Price] (BeginDate, EndDate, PriceValue, ConferenceDayID) \n\tVALUES ('
	for i in range(4):
		val = '\'' +  str(dates[i]) + '\' , '
		val += '\'' + str(dates[i+1]) + '\' , '
		val += str(prices[i+index]) + ' , '
		val += str(day_id) + ' )'
		print (query + val, file = Price_file)
		result += [(dates[i], dates[i+1], prices[i+index])]
	return result

#def workshop_enroll(_id, limit):


def create_payments(price, res_id, date):
	p = int(price*100)
	d = date
	query = 'INSERT INTO [dbo].[Payment] (PaymentValue, PaymentDay, ReservationID) \n\tVALUES ('
	while (p > 0):
		delta = datetime.timedelta(random.randint(1, 10))
		value = random.randint(1,p)
		p = p - value
		p_val = decimal.Decimal(p)/100
		val = str(p_val) + ' , '
		val += '\'' + str(d + delta) + '\', '
		val += str(res_id) + ' )'
		print (query + val, file = Payment_file)


#	need to be corrected - no concept
def create_reservations(prices, enroll, limit, discount, day_date):
	'''
		pirces = list of (begin_date, end_date, price)
		enroll = list of (workshop_id, limit, day_id, w_price)
		target:
			create reservations that fulfill min 80% of limit
			create participantsList for every reservation
			create workshop participants max 1 for 2 workshops 
			create workshop_list based on participantsList
			reverse the list :)
	'''
	day_id = enroll[0][2]
	global conference_day_reservation_id
	people = 0
	low_limit = limit / 13
	participants = []
	l = limit
	reservations = []
	reservations_detailed = []
	enrollment_args = []
	users =[]
	# Divide ConferenceDay for reservations
	while l > low_limit:
		r = random.randint(1,limit)
		l -= r
		people += r
		date = random.randint(3, 35)
		date = day_date + datetime.timedelta((-1)*date)
		reservations.append((r, date))
	participants = random.sample(range(1,15001), people)
	index = 0
	for r in reservations:
		_date = r[1]
		res = []
		for i in range(r[0]):
			res += [participants[index]]
			index += 1
		conference_day_reservation_id += 1
		reservation_id = conference_day_reservation_id
		day_price = 0
		for i in prices:
			if(not(_date  < i[0]) and _date < i[1]):
				day_price = i[2]
				break
		students_count = 0
		for s in res:
			if s % 100 == 0:
				students_count += 1
		customer_id = random.randint(1, 473)
		users += create_participants(res, reservation_id)
		enrollment_args += [(reservation_id, r[0], users[1])]
		price = students_count*(day_price*(1-discount))
		price += day_price*(r[0]-students_count)
		reservations_detailed += [(reservation_id, students_count, customer_id, day_id, r[0], r[1], price)]
	result = make_enrollment(enrollment_args, enroll, discount)
	# result - {
	#	workshop_enrollment list of workshopenrollment records (reservation_id, workshop_enrollment_id, WorkshopID, ParticipantCount, StudentsCount)
	#	list of tuples where tuple : enrollment_id, (list of users)
	# 	total_price of all enrollments
	#}
	make_reservation(reservations_detailed, result[2])
	make_participants(users[0])
	create_workshop_enrollment(result[0])
	for t in result[1]:
		create_workshop_participants(t[0], t[1])


def create_participants(person, conference_day_reservation_id):
	res = []
	res2 = []
	global participant_id
	for r in person:
		participant_id += 1
		res.append((participant_id, r, conference_day_reservation_id))
		res2.append(participant_id)
	return (res, res2)

def make_participants(users):
	query = 'INSERT INTO [dbo].[Participants] (ParticipantID, PersonID, ConferenceReservationID) \n\t VALUES ('
	for u in users:
		val = str(u[0]) + ' , ' + str(u[1]) + ' , ' + str(u[2]) + ' )'
		print (query + val, file = Participants_file)


def make_enrollment(reservation, enroll, discount):
	# reservation = [(ReservationID, overall_count, list of paricipants)]
	# enroll = list : (workshop_id, limit, day_id, w_price) -> day_id is redundant
	# discount = students-discount for workshop
	# result - {
	#	workshop_enrollment list of workshopenrollment records (reservation_id, workshop_enrollment_id, WorkshopID, ParticipantCount, StudentsCount)
	#	list of tuples where tuple : enrollment_id, (list of users)
	# 	total_price of all enrollments
	#}
	global workshop_enrollment_id
	result_0 = []
	result_1 = []
	res2 = []
	w_ids = []
	limits = []
	prices = []
	for e in enroll:
		limits += [e[1]]
		prices += [e[3]]
		w_ids +=[e[0]]

	for res in reservation:
		res_count = res[1]
		_id = res[0]
		participants = []
		result_2 = 0
		for i in range(4):
			workshop_enrollment_id += 1
			we__id = workshop_enrollment_id
			if(limits[i] > 0):
				fulfillment = random.randint(1,limits[i])
				limits[i] = limits[i] - fulfillment
				sample = min(len(res[2]), fulfillment)
				participants += random.sample(res[2], sample)
				students_count = 0
				for p in participants:
					if p % 100 == 0:
						students_count += 1
				curr_price = students_count*(1 - discount)*prices[i]
				curr_price += (len(participants) - students_count)*prices[i]
				result_2 += curr_price
				result_1.append((we__id, participants))
				result_0.append((_id, we__id, w_ids[i], fulfillment, students_count))
		res2.append((_id, result_2))
	return (result_0, result_1, res2)



# enroll = list of (workshop_id, limit, day_id, w_price)


def make_reservation(reservations, prices):
	# reservations_detailed [(ConferenceDayReservationID, students_count, customer_id, day_id, ParticipantsCount, reservation_date, price)]
	# prices = [_id, price]
	query = 'INSERT INTO [dbo].[ConferenceDayReservation] (ReservationID, ParticipantsCount, ConferenceDayID, CustomerID, RegistrationDate, StudentsCount)'
	query += '\n\t VALUES ('
	result = []
	for r in reservations:
		for p in prices:
			if(p[0] == r[0]):
				result.append((p[1] + r[6], p[0], r[5]))
		val = str(r[0]) + ' , ' + str(r[4]) + ' , ' + str(r[3]) + ' , ' + str(r[2]) + ' , \'' + str(r[5]) + '\' , ' +  str(r[1]) + ' )'
		print (query + val, file = ConferenceDayReservation_file)
	for reservation in result:
		create_payments(reservation[0], reservation[1], reservation[2])



def create_workshop_enrollment(enrollments):
	#list of workshopenrollment records (reservation_id, workshop_enrollment_id, WorkshopID, ParticipantCount, StudentsCount)
	query = 'INSERT INTO [dbo].[WorkshopEnrollment] (ReservationID, WorkshopEnrollmentID, WorkshopID, ParticipantsCount, StudentsCount)'
	query += '\n\t VALUES ('
	end_signs = [' , ', ' , ', ' , ', ' , ', ' )']
	for e in enrollments:
		val = ""
		for i in range(5):
			val += str(e[i]) + end_signs[i]
		print(query + val, file = WorkshopEnrollment_file)

def create_workshop_participants(enrollment_id, users):
	# user = participantID
	query = 'INSERT INTO [dbo].[WorkshopParticipants] (WorkshopEnrollmentID, ParticipantID) \n\t VALUES ('
	query += ' ' + str(enrollment_id) + ' , '
	for u in users:
		print (query + str(u) + ' )', file = WorkshopParticipants_file)




__main__()