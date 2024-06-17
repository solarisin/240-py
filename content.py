
# import subprocess
# def stats_get_line(line_num, data):
#     if line_num == 0:
#         cmd = "hostname -I | cut -d' ' -f1"
#         text = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
#         color = "#FFFFFF"
#     elif line_num == 1:
#         # note: this can take ~150ms to execute
#         cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
#         text = subprocess.check_output(cmd, shell=True).decode("utf-8")
#         color = "#FFFF00"
#     elif line_num == 2:
#         cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
#         text = subprocess.check_output(cmd, shell=True).decode("utf-8")
#         color = "#00FF00"
#     elif line_num == 3:
#         cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
#         text = subprocess.check_output(cmd, shell=True).decode("utf-8")
#         color = "#0000FF"
#     elif line_num == 4:
#         cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"
#         text = subprocess.check_output(cmd, shell=True).decode("utf-8")
#         color = "#FF00FF"
#     elif line_num == 5:
#         text, color = get_fps_text(data)
#     else:
#         text = "Line " + str(line_num)
#         color = "#{:06x}".format(randrange(0x1000000))
#     return text, color
