# """
# 需要 chmod +x get_rasp_info.py
# 增加权限，否则无法读取CPU的使用效率
#
# """
# import os
#
# def getCPUtemperature():
#     res = os.popen('vcgencmd measure_temp').readline()
#     return (res.replace("temp=", "").replace("'C\n", ""))
#
#
# # Return RAM information (unit=kb) in a list
# # Index 0: total RAM
# # Index 1: used RAM
# # Index 2: free RAM
# def getRAMinfo():
#     p = os.popen('free')
#     i = 0
#     while 1:
#         i = i + 1
#         line = p.readline()
#         if i == 2:
#             return (line.split()[1:4])
#
# def getCPUuse():
#     return (str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
#
# def getDiskSpace():
#     p = os.popen("df -h /")
#     i = 0
#     while 1:
#         i = i + 1
#         line = p.readline()
#         if i == 2:
#             return (line.split()[1:5])
#
# CPU_temp = getCPUtemperature() # CPU 温度
# CPU_usage = getCPUuse() # CPU使用信息
#
#
# # RAM information
# RAM_stats = getRAMinfo()
# RAM_total = round(int(RAM_stats[0]) / 1000, 1)
# RAM_used = round(int(RAM_stats[1]) / 1000, 1)
# RAM_free = round(int(RAM_stats[2]) / 1000, 1)
#
# # Disk information
# DISK_stats = getDiskSpace()
# DISK_total = DISK_stats[0]
# DISK_used = DISK_stats[1]
# DISK_perc = DISK_stats[3]
#
#
def get_rasp_infos():
    #return (CPU_temp, CPU_usage, str((RAM_used / RAM_total) * 100)[0:4])
    return (32,45,39)
#
#
#
# if __name__ == '__main__':
#     print('')
#     print('CPU Temperature = ' + CPU_temp)
#     print('CPU Use = ' + CPU_usage)
#     print('')
#     print('RAM Total = ' + str(RAM_total) + ' MB')
#     print('RAM Used = ' + str(RAM_used) + ' MB')
#     print('RAM Free = ' + str(RAM_free) + ' MB')
#     print('')
#     print('DISK Total Space = ' + str(DISK_total) + 'B')
#     print('DISK Used Space = ' + str(DISK_used) + 'B')
#     print('DISK Used Percentage = ' + str(DISK_perc))