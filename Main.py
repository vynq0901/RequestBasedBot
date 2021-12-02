from Task import Task
from CoppingThread import CoppingThread

threads = []

task1 = Task("ngqvy0901@gmail.com", "fireblood1", "tien anh", "0331212252", "xã bình lợi", 45, 724, 25234, "chocolate", "pant2", "l", 1)
task2 = Task("nqvy0901@gmail.com", "fireblood1", "Văn Lợi", "0931444444", "thon 8", 41, 443, 23956, "chocolate", "pa2nt", "l", 2)
task3 = Task("cmtry0901@gmail.com", "fireblood1", "Văn Lợi", "0931444444", "thon 8", 41, 443, 23956, "chocolate", "pan2t", "l", 2)
task4 = Task("ktran2246@gmail.com", "fireblood1", "Văn Lợi", "0931444444", "thon 8", 41, 443, 23956, "chocolate", "pan2t", "l", 2)

thread1 = CoppingThread(task1)
thread1.start()
threads.append(thread1)

thread2 = CoppingThread(task2)
thread2.start()
threads.append(thread2)

thread3 = CoppingThread(task3)
thread3.start()
threads.append(thread3)

thread4 = CoppingThread(task4)
thread4.start()
threads.append(thread4)
for t in threads:
    t.join()
