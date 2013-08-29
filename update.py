#!/home/openleg/.envs/kallos/bin/python

import datetime
from subprocess import check_call
import scrape


def main():

    # Update.
    scrape.main()

    # Add any new files.
    cmd = 'git add .'
    check_call(cmd, shell=True)

    # Commit changes.
    cmd = 'git commit -am"changes as of %s"'
    cmd = cmd % datetime.datetime.now().isoformat()
    check_call(cmd, shell=True)

    # Pull changes.
    cmd = 'git pull origin master'
    check_call(cmd, shell=True) 

    # Push changes.   
    cmd = 'git push origin master'
    check_call(cmd, shell=True)


if __name__ == '__main__':
    main()
