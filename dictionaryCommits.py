"""
There are two possibilities:
1. Create a dictoinary of commits
2. Use class variable as the storage of commits
"""

class Commit:
    """Class for representing commits as ID<->links"""
    cves = dict()

    def __init__(self, id, links):
        """
        Constructor for class Commit

        :param id: str
        :param links: list
        """
        self.id = id
        self.links = links

    def add_to_dictionary(self):
        """
        Add commit-associated data into class' variable

        :return: None
        """
        Commit.cves[self.id] = self.links


def read_file(filename):
    """
    Reads chosen file (data_commits.txt in this case)

    str -> <class 'generator'>
    """
    f = open(filename, 'r', encoding='utf-8', errors='ignore')
    generator = (line.strip() for line in f if line != '---------------\n')
    return generator


def create_dictionary(generator):
    """
    Creates dictionary
    (key=CVE id, value=list of links)

    <class 'generator'> -> dict
    """
    cves = dict()
    for item in generator:
        if item.startswith('CVE'):
            header = item
            links = list()
        else:
            links.append(item)
        cves[header] = links

    return cves


def create_class_dictionary(generator):
    """
    Creates dictionary as an class' variable
    (key=CVE id, value=list of links)

    <class 'enerator'> -> None
    """
    for item in generator:
        if item.startswith('CVE'):
            header = item
            links = list()
        else:
            links.append(item)
        commit = Commit(header, links)
        commit.add_to_dictionary()


filelines = read_file('data_commits.txt')
create_class_dictionary(filelines)
