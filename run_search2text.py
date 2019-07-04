import subprocess

for i in range(0,10000):
    cmd = "python3 search2text.py " 
    print("开始处理: "+cmd)
    print(subprocess.call(cmd, shell=True))