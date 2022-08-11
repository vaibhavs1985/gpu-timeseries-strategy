import nvidia_smi

nvidia_smi.nvmlInit()

gpu_util_avg = 0.0
for i in range(0,8):
    handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
# card id 0 hardcoded here, there is also a call to get all available card ids, so we could iterate

    res = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
    gpu_util_avg+=(res.gpu/8)

print(gpu_util_avg)
#print(f'gpu: {res.gpu}%, gpu-mem: {res.memory}%')
