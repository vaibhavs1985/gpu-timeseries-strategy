

from utility import *
import multiprocessing


util_array = [[] for i in range(8)]
forecast = []

# Read the current performance events value from the file
prev_len = -1
current_len = 0
counter = 0
n = len(gpu_freq)
def switch_gpu_frequency(forecast,budget):

    index = 0
    if budget==1200:
        index = 3
    elif budget ==1000:
        index = 2
    elif budget == 800:
        index = 1

    gpu_freq_arr = []
    for i in range(8):
        gpu_freq_raw = ((forecast[i] * 1530 - 140)/100) + 140
        if gpu_freq_raw < 135:
            gpu_freq_raw = 135
        if gpu_freq_raw > 1530:
            gpu_freq_raw = 1530
        
        gpu_freq_index = int((1530-gpu_freq_raw)/8)

        gpu_freq_arr.append(gpu_freq[n-1-gpu_freq_index])
        cmd = f'sudo nvidia-smi -i {i} -ac 877,{gpu_freq[n-1-gpu_freq_index+index]}'
        #cmd = f'~/./highestfrequency.sh {core_freq[a]} {uncore_to_code[uncore_freq[b]]}'
        os.system(cmd)

    print(gpu_freq_arr)


while True:
   
    for i in range(8):
        util_array[i].append(get_gpu_util()[i])
    
    if counter>=10:
        
       forecast = modeling(util_array)
       switch_gpu_frequency(forecast,800)
        

        

    #a, b = optimal_core_uncore(line_array)
    #print(a,b)
    #cmd = f'~/./highestfrequency.sh {core_freq[a]} {uncore_to_code[uncore_freq[b]]}'
    #os.system(cmd)
    sleep(1)
    counter+=1

