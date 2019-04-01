import urllib.request
import re
from scraper import write_to_txt


def save_file():
    """
    Pulls CVE names and commit links from tracking list

    None - list
    """
    URL = 'https://salsa.debian.org/security-tracker-team/security-tracker/raw/master/data/CVE/list'
    file = urllib.request.urlopen(URL).readlines()
    generic = [line.strip().decode() for line in file]
    result = list()
    i = 0
    while True:
        try:
            if generic[i].startswith('CVE'):
                header = [
                    re.findall("^CVE-\d+-\d+|^CVE-\d+-[X]+", generic[i])[0]]
                i += 1
                notes = list()
                while not generic[i].startswith('CVE'):
                    if re.search("http[s]?:\/\/.+commit\/.+$", generic[i]):
                        link = re.findall("http[s]?:\/\/.+commit\/.+$",
                                          generic[i])
                        notes.append(link[0])
                    i += 1
                if notes != list():
                    result.append(header + notes)
        except IndexError:
            print('Finished')
            break
    return result


if __name__ == '__main__':
    data = save_file()
    write_to_txt(data, 'data_commits.txt')
