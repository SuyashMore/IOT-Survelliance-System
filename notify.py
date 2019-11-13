from notify_run import Notify
notify = Notify()



def alert():
    notify.send('Somebody is there')


if __name__=="__main__":
    alert()