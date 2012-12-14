import datetime
from subprocess import check_call
import scrape

scrape.main()
cmd = 'git add .'
check_call(cmd, shell=True)
cmd = 'git commit -am"changes as of %s"' % datetime.datetime.now().isoformat()
check_call(cmd, shell=True)