import urllib.request
import re


class Data:
    """Class for storing CVE id and links of commits"""
    def __init__(self, name, links):
        """
        Constructor for class Data

        :param name: str
        :param links: list
        """
        self.name = name
        self.links = links

    def __str__(self):
        return self.name + '\n' + '\n'.join(self.links) + '\n---------------\n'


def pull_list():
    """
    Pulls data from CVE tracking list

    None -> list
    """
    URL = 'https://salsa.debian.org/security-tracker-team/security-tracker/raw/master/data/CVE/list'
    file = urllib.request.urlopen(URL).readlines()
    generic = [line.strip().decode() for line in file]
    return generic


def save_file():
    """
    Pulls CVE names and commit links from tracking list

    None -> list
    """
    # TODO: move to separate function
    generic = pull_list()
    result = list()
    i = 0
    while True:
        try:
            if generic[i].startswith('CVE'):
                cve_pattern = "^CVE-\d+-\d+|^CVE-\d+-[X]+"
                header = re.findall(cve_pattern, generic[i])[0]
                i += 1
                notes = list()
                while not generic[i].startswith('CVE'):
                    commit_pattern = "http[s]?:\/\/.+commit\/.+$"
                    if re.search(commit_pattern, generic[i]):
                        link = re.findall(commit_pattern, generic[i])
                        notes.append(link[0])
                    i += 1
                if notes != list():
                    result.append(Data(header, notes))
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
    for item in data:
        f.write(item.__str__())
    f.close()


if __name__ == '__main__':
    data = save_file()
    write_to_txt(data, 'data_commits.txt')
