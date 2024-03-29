from multiprocessing import Process
from main import main

pv = "20"
for decision in ["H", "S", "D"]:
    for count in range(-5,6):
        process_list = []
        for dv in ["A", "T", "9", "8", "7", "6", "5", "4", "3", "2"]:
            process_list.append(Process(target=main, args=(pv, dv, count, decision)))

        for process in process_list:
            process.start()
        
        for process in process_list:
            process.join()