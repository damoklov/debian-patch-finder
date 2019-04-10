import urllib.request
import wget
from dictionaryCommits import Commit
from chooseCVE import read_user_input


github = {'github'}
git_like = {'git', 'gnunet', 'source', 'anongit', 'cgit', 'w1.fi', 'roy',
            'gitweb', 'repos', 'bacula', 'pkgs', 'kernel'}
lab_like = {'gitlab', 'dulwich', 'dev', '0xacab', 'lab', 'salsa'}
source_like = {'perl5', 'source', 'repo'}


def git_parser(link):
    """
    Checked on: github, salsa, gitlab
    """
    URL = link + '.patch'
    site = [line.strip().decode() for line in urllib.request.urlopen(URL).readlines()]
    down_border = None
    upper_border = None
    for line in site:
        if 'diff --git' in line:
            down_border = site.index(line)
            upper_border = site.index('---')
            break

    working_piece = site[upper_border+1:down_border-2]
    files = [line.split('|')[0].strip() for line in working_piece]
    return files


def other_parser(link):
    """
    Checked on: git, w1.f1, cgit, kernel
    """
    URL = link.replace('commit', 'patch')
    site = [line.strip().decode() for line in
            urllib.request.urlopen(URL).readlines()]
    down_border = None
    upper_border = None
    for line in site:
        if 'diff --git' in line:
            down_border = site.index(line)
            upper_border = site.index('---')
            break

    working_piece = site[upper_border + 1:down_border - 2]
    files = [line.split('|')[0].strip() for line in working_piece]
    return files


def get_lab_filepage(files, link):
    """
    Checked on: gitlab, dulwich, dev, 0xacab, lab, salsa
    """
    for file in files:
        URL = link.replace('commit/', 'raw/') + '/' + file
        wget.download(URL)


def get_source_filepage(files, link):
    """
    Checked on: perl5, source, repo
    """
    for file in files:
        URL = link.replace('commit/', 'blob_plain/') + ':' + file
        wget.download(URL)


def get_git_filepage(files, link):
    """
    Checked on: git, gnunet, source, anongit, cgit, w1.fi, roy, gitweb,
                repos, bacula, pkgs, kernel
    """
    for file in files:
        URL = link.replace('commit', 'plain/' + file)
        wget.download(URL)


def get_github_filepage(files, link):
    """
    Checked on: github
    """
    for file in files:
        URL = link.replace('commit/', '').replace('github', 'raw.github') + '/' + file
        wget.download(URL)


def main():
    """
    Launches patch-searching process

    None -> None
    """
    links = read_user_input()

    if not links:
        print('Wrong input!')
        quit(0)

    for link in links:

        try:
            files = git_parser(link)
        except Exception:
            files = other_parser(link)

        try:
            if any(x in link for x in github):
                get_github_filepage(files, link)
            elif any(x in link for x in git_like):
                get_git_filepage(files, link)
            elif any(x in link for x in lab_like):
                get_lab_filepage(files, link)
            elif any(x in link for x in source_like):
                get_source_filepage(files, link)
            else:
                print('Probably an invalid link')
                quit(0)
        except Exception:
            print('An exception occurred!')
            quit(0)


if __name__ == '__main__':
    main()
