from dictionaryCommits import Commit


def read_user_input():
    """
    Reads and validates user's input

    None -> list/None
    """
    cve = input('Enter the tag of CVE, please: ')
    try:
        return Commit.cves[cve]
    except KeyError:
        return None


def result_printer():
    """
    Prints result for a chosen CVE id

    None -> None
    """
    commits_request = read_user_input()
    if commits_request:
        print(commits_request)
    else:
        print('Nothing found on this CVE')


if __name__ == '__main__':
    result_printer()
