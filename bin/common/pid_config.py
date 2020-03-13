import sys
sys.path.append("../tools_dep/")
import portalocker
import os,signal

def add_pid(pid, pid_file):
    if not os.path.isfile(pid_file): 
         file = open(pid_file, "w", encoding = 'utf-8')
         file.close()

    with open(pid_file, "r+", encoding = 'utf-8') as file:
        lines = file.readlines()
        portalocker.lock(file, portalocker.LOCK_EX)
        if len(lines) > 0:
            file.writelines("\n"+pid)
        else:
            file.writelines(pid)

def clean_pid(pid_file):
    if os.path.isfile(pid_file):
        with open(pid_file, "r+", encoding = 'utf-8') as file:
            lines = file.readlines()
            portalocker.lock(file, portalocker.LOCK_EX)
            for line in lines:
                try:
                    os.killpg(int(line.strip()), signal.SIGTERM)
                except Exception as e:
                    pass
                    #print(e)
                    #print("kill pid "+line.strip()+" but no such process")     
        os.remove(pid_file) 
            
if __name__ == "__main__" :
    clean_pid(sys.argv[1])