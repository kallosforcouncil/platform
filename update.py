from subprocess import check_call
import scrape

scrape.main()
cmd = 'git add .'
check_call(cmd, shell=True)
cmd = 'git commit -am"changes as of 2012-12-13T19:21:41.723576"'
check_call(cmd, shell=True)