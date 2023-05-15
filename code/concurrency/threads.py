import threading
import time

def worker(id:int , delay: float):
    print(f"----------- worker#{id} is started...")
    for i in range(10):
        time.sleep(delay)
        print(f"worker{id} is running: {time.time()}")
    print(f"----------- worker#{id} is finished...")


class Worker(threading.Thread):
    def __init__(self, name: str, delay: float, *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)
        self.delay = delay
        print(self.name)

    def run(self):
        print(f"+++++++++++ Worker#{self.name} is started...")
        for i in range(10):
            time.sleep(self.delay)
            print(f"Worker{self.name} is running: {time.time()}")
        print(f"+++++++++++ Worker#{self.name} is finished...")

if __name__ == "__main__":
    w1 = threading.Thread(target=worker, args=(1, 0.5,))
    w2 = threading.Thread(target=worker, args=(2, 0.1,))
    w3 = Worker("3", 1.5, daemon=True)

    w1.start()
    w2.start()
    w3.start()

    w1.join()
    w2.join()
    #w3.join()

    print("End of __main__")
