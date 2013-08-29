<<<<<<< HEAD
=======
#!/home/openleg/.envs/kallos/bin/python

>>>>>>> 15c8675dc1f428ee1a0ca1c4ab9c452466fd40e6
import datetime
from subprocess import check_call
import scrape


def main():
<<<<<<< HEAD
    scrape.main()

    cmd = 'git add .'
    check_call(cmd, shell=True)

=======

    # Update.
    scrape.main()

    # Add any new files.
    cmd = 'git add .'
    check_call(cmd, shell=True)

    # Commit changes.
>>>>>>> 15c8675dc1f428ee1a0ca1c4ab9c452466fd40e6
    cmd = 'git commit -am"changes as of %s"'
    cmd = cmd % datetime.datetime.now().isoformat()
    check_call(cmd, shell=True)

<<<<<<< HEAD
=======
    # Pull changes.
    cmd = 'git pull origin master'
    check_call(cmd, shell=True) 

    # Push changes.   
>>>>>>> 15c8675dc1f428ee1a0ca1c4ab9c452466fd40e6
    cmd = 'git push origin master'
    check_call(cmd, shell=True)


if __name__ == '__main__':
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 15c8675dc1f428ee1a0ca1c4ab9c452466fd40e6
