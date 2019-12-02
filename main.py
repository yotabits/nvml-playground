from pynvml import *

nvmlInit()

def get_gpu_handle_list():
    device_handle_list = []
    nb_devices = nvmlDeviceGetCount()
    for device_number in range(0, nb_devices):
        device_handle_list.append(nvmlDeviceGetHandleByIndex(device_number))
    return device_handle_list

def configure_gpu(device_handle):
    nvmlDeviceSetAccountingMode(device_handle, NVML_FEATURE_ENABLED)

device_list = get_gpu_handle_list()


for device_handle in device_list:
    #configure_gpu(device_handle)
    gpu_info_dict = {}
    gpu_info_dict["power_usage_mw"] = nvmlDeviceGetPowerUsage(device_handle)
    gpu_info_dict["gpu_percent"] = nvmlDeviceGetUtilizationRates(device_handle).gpu
    gpu_info_dict["gpu_memory"] = nvmlDeviceGetUtilizationRates(device_handle).memory
    gpu_info_dict["clock_sm"] = nvmlDeviceGetClockInfo(device_handle, NVML_CLOCK_SM)
    gpu_info_dict["clock_mem"] = nvmlDeviceGetClockInfo(device_handle, NVML_CLOCK_MEM)
    gpu_info_dict["clock_video"] = nvmlDeviceGetClockInfo(device_handle, NVML_CLOCK_GRAPHICS)
    gpu_info_dict["accounting_mode"] = nvmlDeviceGetAccountingMode(device_handle)
    pcie_counter = nvmlDeviceGetPcieReplayCounter(device_handle)
    gpu_info_dict["PCIe_usage"] = nvmlDeviceGetPcieThroughput(device_handle, pcie_counter)
    gpu_info_dict["pid_map"] = nvmlDeviceGetAccountingPids(device_handle)

    pid_map = gpu_info_dict.get("pid_map")
    pid_dict = {}
    process_list = []

    for pid in pid_map:
        single_pid_dict = {}
        process_info = nvmlDeviceGetAccountingStats(device_handle, pid)
        try:
            name = nvmlSystemGetProcessName(pid)
            print(str(name) + " " + str(pid))
        except nvml.NVMLError_NotFound:
            print("Process name not found for: " + str(pid))
            name = "Unknown"

        single_pid_dict["name"] = name
        single_pid_dict["pid"] = pid
        single_pid_dict["ram_percent"] = process_info.memoryUtilization
        single_pid_dict["gpu_percent"] = process_info.gpuUtilization
        process_list.append(single_pid_dict)



    print(gpu_info_dict)
    print(process_list)
    #nvmlDeviceSetAccountingMode(device_handle, NVML_FEATURE_DISABLED)







