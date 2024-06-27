import schedule
import time


jobs = ["web server", "load balancer", "app server"]
count = 0


def job(message='none', count=0):
    if len(message):
        print("I'm working on:", message[count])
        message.pop(0)
    else:
        return
    schedule.every(5).seconds.do(job, message)


job(jobs)
while True:
    schedule.run_pending()
    time.sleep(1)
