#!/home/openleg/.envs/kallos/bin/python

import datetime
from subprocess import check_call
import scrape


def main():
    scrape.main()
    cmd = 'git add .'
    check_call(cmd, shell=True)
    cmd = 'git commit -am"changes as of %s"'
    cmd = cmd % datetime.datetime.now().isoformat()
    check_call(cmd, shell=True)
    cmd = 'git push origin master'
    check_call(cmd, shell=True)


if __name__ == '__main__':
    main()
