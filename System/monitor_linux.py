import os
import time
# -*- coding:utf-8 -*- 

#Cpu
###############################################################
# Cpu use
last_worktime=0
last_idletime=0
def get_cpu_use():
    global last_worktime, last_idletime
    f=open("/proc/stat","r")
    line=""
    while not "cpu " in line:
        line=f.readline()
    f.close()
    spl=line.split(" ")
    worktime=int(spl[2])+int(spl[3])+int(spl[4])
    idletime=int(spl[5])
    dworktime=(worktime-last_worktime)
    didletime=(idletime-last_idletime)
    rate=float(dworktime)/(didletime+dworktime)
    cpu_t = rate*100
    last_worktime=worktime
    last_idletime=idletime
    if(last_worktime==0): 
        return 0
    return round(cpu_t,2)

# Cpu freq
def get_cpu_freq():
    freq_str = os.popen('cat /proc/cpuinfo | grep MHz | uniq').read()
    freqs =[]
    while freq_str.find('\n') != -1:
        freqs.append(float(freq_str[freq_str.find(':')+2:freq_str.find('\n')]))
        freq_str=freq_str[freq_str.find('\n')+1:]
    return max(freqs)

# Cpu freq
def get_cpu_temp():
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        temp_str = os.popen('cat /sys/class/thermal/thermal_zone0/temp').read()
    elif os.path.isfile('/sys/class/hwmon/hwmon0/device/hwmon/hwmon0/temp1_input'):
        temp_str = os.popen('cat /sys/class/hwmon/hwmon0/device/hwmon/hwmon0/temp1_input').read()
    elif os.path.isfile('/sys/class/hwmon/hwmon0/device/hwmon0/temp1_input'):
        temp_str = os.popen('cat /sys/class/hwmon/hwmon0/device/hwmon0/temp1_input').read()
    else:
        return -1
    return (float(temp_str)/1000)

# Mem
###############################################################
def get_mem_use():
    mem_str = os.popen('free').read()
    if '内存'in mem_str :
        mem_str = mem_str[mem_str.find('内存：')+3:mem_str.find('交换')]
    else:
        mem_str = mem_str[mem_str.find('Mem:')+4:mem_str.find('Swap')]
    mem_str = mem_str.split()
    total = int(float(mem_str[0])/1024)
    used = int(float(mem_str[1])/1024)
    percent = int(used/total*100)
    return total,used,percent

def get_swap_use():
    mem_str = os.popen('free').read()
    if '内存'in mem_str :
        mem_str = mem_str[mem_str.find('交换：')+3:]
    else:
        mem_str = mem_str[mem_str.find('Swap:')+5:]
    mem_str = mem_str.split()
    total = int(float(mem_str[0])/1024)
    used = int(float(mem_str[1])/1024)
    percent = int(used/total*100)
    return total,used,percent

#gpu 
###############################################################
gpus_str = os.popen('nvidia-smi -L').read()
gpus =[]
if 'communicate with the NVIDIA driver' not in gpus_str:
    while gpus_str.find('\n') != -1:
        gpus.append(gpus_str[gpus_str.find(':')+2:gpus_str.find('(')-1])
        gpus_str=gpus_str[gpus_str.find('\n')+1:]

def get_gpu_use():
    
    gpu_infos = []
    for i in range(len(gpus)):
        infos_str = os.popen('nvidia-smi').read()
        infos_str = infos_str[infos_str.find(str(i)+'  '+gpus[i]):]
        infos_str = infos_str[infos_str.find('\n')+1:]
        infos_str = infos_str[:infos_str.find('\n')+1]
        infos_str = infos_str.split()
        #['|', '50%', '42C', 'P0', '19W', '/', '75W', '|', '929MiB', '/', '5050MiB', '|', '14%', 'Default', '|']
        if infos_str[1].replace('%','') == 'N/A':
            fan = -1
        else:
            fan = int(infos_str[1].replace('%',''))        # %
        temp = int(infos_str[2].replace('C',''))       # C
        if infos_str[4] == 'N/A':
            power_used = -1
            power_max = -1
        else:
            power_used = int(infos_str[4].replace('W','')) # W
            power_max = int(infos_str[6].replace('W',''))  # W
        mem_used = int(infos_str[8].replace('MiB','')) # MB
        mem_max = int(infos_str[10].replace('MiB',''))  # MB
        util_used = int(infos_str[12].replace('%',''))  # %
        gpu_infos.append([fan,temp,power_used,power_max,mem_used,mem_max,util_used])
    return gpu_infos


#Net
###############################################################
net_infos_history = [0,0]
def get_net_use(network_adapter = 'all'):
    net_str = os.popen('cat /proc/net/dev').read()
    infos = []
    net_infos = [0,0,0,0]
    while net_str.find('\n') != -1:
        if net_str[:50].find(':') != -1:
            infos.append((net_str[net_str.find(':')+2:net_str.find('\n')-1]).split())
        net_str=net_str[net_str.find('\n')+1:]
    net_rxs=[];net_txs=[]
    for info in infos:
        net_rxs.append(int(info[0]))
        net_txs.append(int(info[8]))
    if network_adapter == 'all':
        net_infos[0] = (sum(net_rxs)/1024)
        net_infos[1] = (sum(net_txs)/1024)
    elif network_adapter == 'auto':
        net_infos[0] = (max(net_rxs)/1024)
        net_infos[1] = (max(net_txs)/1024)
    if net_infos_history[0] == 0:
        net_infos[2] = 0
        net_infos[3] = 0
    else:
        net_infos[2] = net_infos[0]-net_infos_history[0]
        net_infos[3] = net_infos[1]-net_infos_history[1]
    net_infos_history[0] = net_infos[0]
    net_infos_history[1] = net_infos[1]
    return net_infos

#Disk
###############################################################
def get_disk_use():
    disk_str = os.popen('df -h').read()
    disk_str = disk_str.split('\n')
    disk_infos = []
    for line in disk_str:
        if 'G' in line[:24] and 'tmpfs' not in line:
            line = line.split()
            if float(line[1].replace('G',''))>20:
                disk_infos.append(line)
        elif 'T' in line and 'tmpfs' not in line:
            line = line.split()
            disk_infos.append(line)
    return disk_infos

def get_bar(percent,num = 25):
    # graphs = ' ▏▎▍▋▊▉'
    percent = round(percent)
    bar = '['
    for i in range(num):
        if i < round(percent/int((100/num))):
            bar += '#'
        else:
            bar += '-'
    bar += ']'
    return bar

def fill_str(string,num):
    if len(string)>num:
        return string[:num-3]+'...'
    for i in range(num-len(string)):
        string +=' '
    return string

def main():
    while(1):
        #cpu
        cpu_used = get_cpu_use()
        cpu_freq = get_cpu_freq()
        cpu_temp = get_cpu_temp()
        cpu_used_bar = get_bar(cpu_used,num=50)

        #memory
        mem_total,mem_used,mem_percent = get_mem_use()
        mem_used_bar = get_bar(mem_percent)
        swap_total,swap_used,swap_percent = get_swap_use()
        swap_used_bar = get_bar(swap_percent)

        #gpu
        util_used_bars=[];gpu_mem_bars=[]
        gpu_infoss = get_gpu_use()
        print(gpu_infoss)
        for i in range(len(gpus)):
            gpu_infos = gpu_infoss[i]
            util_used_bars.append(get_bar(gpu_infoss[i][6]))
            gpu_mem_bars.append(get_bar(100*gpu_infoss[i][4]/gpu_infoss[i][5]))

        #net
        net_infos = get_net_use()

        #disk
        disk_infos = get_disk_use()

        ####################################print#################################
        os.system('clear')
        #cpu
        print(('Cpu   Temp: {0:.1f}C | Freq: {1:.1f}MHz').format(cpu_temp,cpu_freq))
        print(('Util: {0:.1f}%  '+cpu_used_bar).format(cpu_used))

        #memory
        print(('\nMemory   Mem: {0:d}MB/{1:d}MB | Swap: {2:d}MB/{3:d}MB').format(
            mem_used,mem_total,swap_used,swap_total))
        print(('Mem: {0:.1f}% '+mem_used_bar+' Swap: {1:.1f}% '+swap_used_bar).format(mem_percent,swap_percent))

        #gpu
        for i in range(len(gpus)):
            print(('\n'+'Gpu'+'{0:d}'+': '+gpus[i].replace('GeForce','')+'   Temp: {1:.1f}C | Power: {2:d}w/{3:d}w | Mem: {4:d}MB/{5:d}MB | Fan: {6:d}%').format(
                i,gpu_infoss[i][1],gpu_infoss[i][2],gpu_infoss[i][3],
                gpu_infoss[i][4],gpu_infoss[i][5],gpu_infoss[i][0]))
            print(('Util:{0:.1f}% '+util_used_bars[i]+'   Mem:{1:.1f}% '+gpu_mem_bars[i]).format(
                gpu_infoss[i][6],100*gpu_infoss[i][4]/gpu_infoss[i][5]))

        #net
        print(('\nNetwork    ↑ all:{0:.1f}GB ↓ all:{1:.1f}GB     ↑ :{2:.1f}Kb/s ↓ :{3:.1f}Kb/s').format(
            net_infos[1]/1024/1024,net_infos[0]/1024/1024,net_infos[3],net_infos[2]))

        #disk
        print('\nFilesystem           Mounted on           Used/Total           Used%')
        for disk_info in disk_infos:
            print(fill_str(disk_info[0], 20),fill_str(disk_info[5], 20),
                fill_str(disk_info[2]+'/'+disk_info[1], 20),fill_str(disk_info[4], 15))

        time.sleep(1)

if __name__ == '__main__':
    main()
