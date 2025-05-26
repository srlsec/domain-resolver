import sys, os
from colorama import Fore
import subprocess
import time
from datetime import datetime
import os, platform, datetime, time, warnings, sys
import os, warnings
from os.path import exists
from concurrent.futures import ThreadPoolExecutor


home_dir = os.path.expanduser("~")
resolver_path = f"{home_dir}/sec-tools/wordlists/domain-resolver/resolvers.txt"


if len(sys.argv) < 3:
    print("Error: No input file provided.")
    print("Usage  : domain-checker <input_file> <output_path> <output_file>")
    print("Example: domain-checker root-domains.txt ../domains no")
    print("Example: domain-checker 1-list-subds.txt . 1-all-subds.txt")
    sys.exit(1)

input_file = sys.argv[1]
output_path = sys.argv[2]
output_file = sys.argv[3]


dnsx = 'dnsx'
PUREDNS = 'puredns'
SUFFLEDNS = 'shuffledns'

target_path = output_path

file_exists = exists(target_path)
if file_exists is False:
    os.mkdir(target_path) 


def banner():
    # https://patorjk.com/software/taag/#p=testall&f=Graffiti&t=cobratoxin
    dec = "\n| Subdomain bruteforce using subdomains list |"
    banner="""
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |D|O|M|A|I|N|-|C|H|E|C|K|E|R|  by srlsec
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""
    print(dec + banner)

def time_now():
    a = datetime.datetime.now().strftime("%H:%M:%S")
    return a

def send_notification(message, provider_id=None):
    command = ["notify", "-silent"]
    
    if provider_id:
        command.extend(["-id", provider_id])
    
    with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True) as process:
        process.communicate(message)

def domaintoip(input_subd_list, output_file_name):

    file_exists = exists(output_file_name)
    if file_exists is False:
        # cmd = f'{dnsx} -d {input_domain} -w {wordlist} -t 400 -silent > {output_file}'
        cmd = f"{PUREDNS} resolve {input_subd_list} --resolvers {resolver_path} --skip-validation  -l 2000 -w {output_file_name}"
        # cmd = f"{SUFFLEDNS} -l {input_subd_list} -r {resolver_path} -silent -mode resolve -t 1000 -o {output_file_name}"
        print(cmd)
        subprocess.check_output((f"{cmd}"), shell=True, text=True)

    if os.path.exists(f"{output_file_name}"):
        with open(output_file_name, 'r') as fp:
            lines = len(fp.readlines())
    
    if lines == 0: 
        print(Fore.WHITE + f"+ [{time_now()}] [active-scan] []" " [" + Fore.RED + f"{lines}" + Fore.WHITE + "]")
        # send_notification(f"{input_domain} bruteforce-subdomains : {lines} ")
    else:
        print(Fore.WHITE + f"+ [{time_now()}] [active-scan] []" " [" + Fore.GREEN + f"{lines}" + Fore.WHITE + "]")
        #end_notification(f"{input_domain} bruteforce-subdomains : {lines} ")


    
def main():
    if input_file == "root-domains.txt":
        pass
    if input_file != "root-domains.txt" and input_file[-4:] == ".txt":
        input_subd_list = input_file
        output_file_name = output_file
        domaintoip(input_subd_list, output_file_name)
    else:
        root_domain = input_file
        domaintoip(root_domain)


if __name__ == "__main__":
    try :
        start = time.time()
        banner()

        print(datetime.datetime.now().strftime( "================ STARTED - %d/%m/%Y %H:%M:%S 00:00:00:00 ================") + '\n')

        main()
        
        now = datetime.datetime.now()
        end = time.time()
        hours, rem = divmod(end-start, 3600)
        minutes, seconds = divmod(rem, 60)

        print(now.strftime('\n' + "=============== COMPLETED - %d/%m/%Y %H:%M:%S")+  " {:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)  + ' ===============' + '\n')

    except KeyboardInterrupt:
        print(f'\nKeyboard Interrupt.\n')
        sys.exit(130)