import sqlite3 as lite
import operator as op

def query(qstring, cur):
	# check if searching with blood group
	query_string = qstring.upper().replace('POSITIVE', '+').replace('NEGATIVE', '-')
	num_length = len(extract_num(query_string))
	
	if num_length<=2 and num_length>0:
		query_string = extract_num(query_string)
		# search by batch
		data = cur.execute(
			'''SELECT * FROM donor WHERE 
			batch=?
			ORDER BY name ASC
			''', 
			(query_string,)
			).fetchall() 
	else:
		if '+' in query_string or '-' in query_string:
			query_string = query_string.replace(' ', '').replace('(', '')
			query_string = query_string.replace(')', '').replace('VE', '')
			query_string = query_string.replace('+', '(+VE)')
			query_string = query_string.replace('-', '(-VE)')

			# search by blood group
			data = cur.execute(
				'''SELECT * FROM donor WHERE 
				blood_group=?
				ORDER BY name ASC
				''', 
				(query_string,)
			).fetchall() 
		else:
			query_string = '%' + query_string + '%'
			# search by name or contact no
			data = cur.execute(
				'''SELECT * FROM donor WHERE 
				name LIKE ? OR
				contact_no LIKE ?
				ORDER BY name ASC
				''', 
				(query_string, query_string)
			).fetchall()
	
	return data

def add_to_db(data, cur):
	name, contact_no, batch, blood_group = data
	name = name.upper()

	# formatting contact no
	contact_no = '0' + extract_num(contact_no)[-10:]

	# formatting blood group
	replacements = [
		(' ', ''),
		('(', ''),
		(')', ''),
		('POSITIVE', '+'),
		('NEGATIVE', '-'),
		('VE', ''),
		('+', '(+VE)'),
		('-', '(-VE)')
	]
	blood_group = blood_group.upper()

	# formatting batch 
	batch = int(extract_num(batch))

	for replacement in replacements:
		blood_group = blood_group.replace(replacement[0], replacement[1])

	#print(name, contact_no, batch, blood_group)

	if len(query(name, cur)) or len(query(contact_no, cur)):
		cur.execute(
			'''UPDATE donor
			SET name = ?, contact_no = ?, batch = ?, blood_group = ?
			WHERE name = ? OR contact_no = ?
			''',
			(name, contact_no, batch, blood_group, name, contact_no)
		)
	else:
		cur.execute(
			"INSERT INTO donor VALUES (?, ?, ?, ?)",
			(name, contact_no, batch, blood_group)
		)

def statistics(cur):
	stat = []
	categories = cur.execute("SELECT DISTINCT blood_group FROM donor").fetchall()
	categories = [category[0] for category in categories]
	total = len(cur.execute("SELECT * FROM donor").fetchall())
	stat.append(('Total', total))
	for category in categories:
		stat.append((category, len(query(category, cur))))

	stat = sorted(stat, key=op.itemgetter(1), reverse=True)
	return stat

def extract_num(value):
	return ''.join([c for c in value if c.isdigit()])

def main():
	conn = lite.connect('database.db')
	c = conn.cursor()
	stat = statistics(c)
	for row in stat:
		print(row)

if __name__=='__main__':
	main()