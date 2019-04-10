import urllib.request
import csv


def save_file():
    """
    Pulls all information from CVE tracking list

    None -> list
    """
    URL = 'https://salsa.debian.org/security-tracker-team/security-tracker/raw/master/data/CVE/list'
    file = urllib.request.urlopen(URL).readlines()
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
                    if 'NOT-FOR-US' in generic[i] or 'RESERVED' in generic[i] \
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
            print('Finished')
            break
    return result


def write_to_txt(data, filename, attr='w'):
    """
    Writes data from tracking list to txt file

    (list, str, str) -> None
    """
    f = open(filename, attr, encoding='utf-8', errors='ignore')
    for collection in data:
        for item in collection:
            f.write(item)
            f.write('\n')
        f.write('----------------------------\n')
    f.close()


def write_to_csv(data, filename, attr='w'):
    """
    Writes data from tracking list to csv file

    (list, str, str) -> None
    """
    writer = csv.writer(open(filename, attr))
    for collection in data:
        writer.writerow([item for item in collection])


if __name__ == '__main__':
    data = save_file()
    write_to_txt(data, 'data_main.txt')
    write_to_csv(data, 'data_main.csv')
