import time

class Watch:
    def timer(self, sec):
        while sec:
            mins, secs = divmod(sec, 60)
            timer = f"{mins:02d}:{secs:02d}"
            print(f"Timer : {timer}", end="\r")
            time.sleep(1)
            sec -= 1

        for i in range(3):
            print("Time Up...!!!", end="\r")
            time.sleep(1)
            print(" " * 15, end="\r")
            time.sleep(1)
        
        print("Time Up...!!!")
        time.sleep(0.75)


    def time_convert(self, seconds):
        mins = seconds // 60
        seconds = seconds % 60
        hours = mins // 60
        mins = mins % 60
        print(f"Time Elapsed = {int(hours)}:{int(mins)}:{seconds:.2f}")

    def stopwatch(self):
        input("Press Enter to start the stopwatch...")
        start_time = time.time()

        input("Press Enter to stop the stopwatch...")
        end_time = time.time()

        elapsed_time = end_time - start_time
        self.time_convert(elapsed_time)

    def clock(self):
        try:
            while True:
                lt = time.localtime()
                current_time = time.strftime("%H:%M:%S", lt)
                print(f"Time: {current_time}", end="\r")
        except KeyboardInterrupt as e:
           print("user stopped the clock")


watch = Watch()
watch.clock()