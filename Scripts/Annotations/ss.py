import subprocess
from subprocess import Popen, PIPE
import glob
import time
import random

test_files = list(range(100))

#
def count_jobs():
    MyOut_bjobs = subprocess.Popen(['ls', '-l'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    stdout_bjobs, stderr_bjobs = MyOut_bjobs.communicate()

    job_count = len(str(stdout_bjobs).split('\\n'))

    return job_count
#

count = 0
total_count = len(test_files)
limit_jobs = 20
#

while(total_count):

    running_jobs = count_jobs()
    if running_jobs > limit_jobs-1:
        print('paused')
        time.sleep(2)
        MyOut = subprocess.Popen(['rm', 'gg-' + str(random.choice(list(range(0,count))))],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)

        print('continue..')

    else:
        free_jobs = 20 - running_jobs
        while(free_jobs):
            # print(free_jobs)
            MyOut = subprocess.Popen(['touch', 'gg-' + str(test_files[count])],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
            stdout, stderr = MyOut.communicate()
            print(str(list(range(0, 100))[count]), str(free_jobs))

            count = count + 1
            total_count = total_count - 1
            free_jobs = free_jobs-1