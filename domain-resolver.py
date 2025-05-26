import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from socket import gethostbyname, gaierror
from datetime import datetime
import pandas as pd
from os.path import exists
import os, platform, datetime, time, warnings, sys


if len(sys.argv) < 2:
    print("Error: No input file provided.")
    print("Usage: domain-resolver all-domains.txt")
    sys.exit(1)


input_file = sys.argv[1]
root_domain_path = sys.argv[2]
scan_type = sys.argv[3]

# Banner
def banner():
    print("""
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|D|O|M|A|I|N|-|R|E|S|O|L|V|E|R| by srlsec
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
""")
    

def domain_resolver_single(domain):
    resolved_domain_file = f"resolved-domains.txt"
    unresolved_domain_file = f"unresolved-domains.txt"
    
    try:
        ip = gethostbyname(domain)
        print({"domain": domain, "ip": ip})

        # Append result to output file (thread-safe)
        with open(resolved_domain_file, "a") as f:
            f.write(f"{domain}\n")

    except gaierror:
        pass

# Resolve domain to IP
def domain_resolver(domain, root_domain):
    resolved_domain_file = f"{root_domain_path}/{root_domain}/resolved-domains.txt"
    unresolved_domain_file = f"{root_domain_path}/{root_domain}/unresolved-domains.txt"
    
    # Ensure the directory exists
    os.makedirs(f"{root_domain_path}/{root_domain}", exist_ok=True)

    try:
        ip = gethostbyname(domain)
        print({"domain": domain, "ip": ip})

        # Append result to output file (thread-safe)
        with open(resolved_domain_file, "a") as f:
            f.write(f"{domain}\n")

    except gaierror:
        pass
        #  # Append result to output file (thread-safe)
        # with open(unresolved_domain_file, "a") as f:
        #     f.write(f"{domain}\n")
        # # print({"domain": domain, "ip": ""})

def main():
    max_threads=50
    if scan_type == 'p':
        try:
            with open(input_file, 'r') as f:
                root_domains = f.read().splitlines()
            
            for root_domain in root_domains:
                print(f"Processing: {root_domain}")

                root_domain_file = f"{root_domain_path}/{root_domain}/1-valid-subds.txt"
                if not os.path.exists(root_domain_file):
                    print(f"Error: {root_domain_file} not found.")
                    continue

                with open(root_domain_file, 'r') as f:
                    domains = f.read().splitlines()

                with ThreadPoolExecutor(max_workers=max_threads) as executor:
                    executor.map(lambda domain: domain_resolver(domain, root_domain), domains)

        except FileNotFoundError:
            print("Error: Input file not found.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    elif scan_type == 's':
        root_domain_file = input_file

        with open(root_domain_file, 'r') as f:
            domains = f.read().splitlines()


        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(lambda domain: domain_resolver_single(domain), domains)


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