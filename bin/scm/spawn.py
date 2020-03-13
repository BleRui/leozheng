import sys
sys.path.append(sys.path[0]+"/../tools_dep/")
import pexpect

def spawn(command, password):
    output_info = ''
    try:
        child = pexpect.spawn(command, timeout=6000)
        child.expect('Password*')
        child.sendline(password)
        output_info = child.read()
    except Exception as e:
        pass
    
    if output_info == '':
        try:
            child = pexpect.spawn(command, timeout=6000)
            output_info = child.read()
        except Exception as e:
            pass
        
    return str(output_info)

def ssh_spawn(private_key, password):
    output_info = ''
    try:
        child = pexpect.spawn('ssh-add '+private_key, timeout=6000)
        child.expect('Enter passphrase for '+private_key+':')
        child.sendline(password)
        index = child.expect (['Bad passphrase, try again for '+private_key+':', 'Identity added: '+private_key+' ('+private_key+')'])
        if index == 0:
            child.sendline('\x03')
            
        output_info = child.read()
    except Exception as e:
        pass
    return str(output_info)
    
if __name__ == "__main__" :
    if len(sys.argv) == 4:
        type = sys.argv[1]
        command = sys.argv[2]
        password = sys.argv[3]
        if type == 'http':
            output_info = spawn(command, password)
        elif type == 'ssh':
            output_info = ssh_spawn(command, password)
        print(output_info)