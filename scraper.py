import urllib.request
import csv


def save_file():
	file = urllib.request.urlopen('https://salsa.debian.org/security-tracker-team/security-tracker/raw/master/data/CVE/list').readlines()
	generic = [line.strip().decode() for line in file]
	result = list()
	i = 0
	while True:
		try:
			if generic[i].startswith('CVE'):
				if ')' in generic[i]:
					flag = False
				else:
					flag = True
				header = [generic[i]]
				i += 1
				notes = list()
				while not generic[i].startswith('CVE'):
					if 'NOT-FOR-US' in generic[i] or 'RESERVED' in generic[i]\
							or 'NOTE' in generic[i] or 'TODO' in generic[i]:
						notes.append(generic[i])
						i += 1
					elif generic[i].startswith('-'):
						notes.append(generic[i])
						i += 1
					else:
						if flag:
							header[0] += generic[i]
							i += 1
						else:
							notes.append(generic[i])
							i += 1
				result.append(header + notes)
			else:
				i += 1
		except IndexError:
			print('exception')
			break
	return result


def write_to_txt(data, attr='w'):
	f = open('data.txt', attr, encoding='utf-8', errors='ignore')
	for collection in data:
		for item in collection:
			f.write(item)
			f.write('\n')
		f.write('----------------------------\n')
	f.close()


def write_to_csv(data, attr='w'):
	writer = csv.writer(open('data.csv', attr))
	for collection in data:
		writer.writerow([item for item in collection])


if __name__ == '__main__':
	data = save_file()
	#write_to_txt(data)
	#write_to_csv(data)
