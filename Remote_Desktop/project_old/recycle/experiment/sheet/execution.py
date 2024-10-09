import subprocess

cmd = "net session"

test = subprocess.run(cmd, shell=True)

if test.returncode == 0:
    print('command : success')
else:
    print('command: failed')

