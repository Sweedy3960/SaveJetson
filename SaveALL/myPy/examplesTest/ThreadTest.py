import threading
lck = threading.Lock()
def p1():
    with lck:
        
        for i in range(3):
            print("ZZz")
    for i in range(10):
            print("p1")
def p2():
    for i in range(10):
        print("p2")

t1=threading.Thread(target=p1)
t2=threading.Thread(target=p1)

t1.start()
t2.start()

t2.join()
t1.join()