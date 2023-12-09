import time
import DB.dbFuncs as db

def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            pass
        next_time += (time.time() - next_time) // delay * delay + delay

def check():
    pass

every(60, check)