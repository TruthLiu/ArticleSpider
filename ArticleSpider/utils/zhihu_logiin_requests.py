
import requests
#cookielib是python2版本的 cookiejar是python3的
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

#设置session实例化
session=requests.session()
#设置cookies的存放位置，如果不存在文件名，会自动创建一个
session.cookies=cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未能加载")






#设置代理
agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36"
header={
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com/",
    "User-Agent":agent
}

def is_login():
    #通过个人中心页面返回状态码来判断是否为登录状态
    inbox_url="https://www.zhihu.com/inbox"
    response=session.get(inbox_url,headers=header,allow_redirects=False)
    if response.status_code !=200:
        return False
    else:
        return True

#获取_xsrf的值
def get_xsrf():
    response=session.get("https://www.zhihu.com",headers=header)
    # match_re=re.match('.*name="_xsrf" value="(.*)"',response.text)
    #text='<input type="hidden" name="_xsrf" value="36666331356536392d323963392d343836642d383163342d386666653139633563333436">'
    match_re=re.search(r'.*name="_xsrf" value="(.*?)"',response.text)
    if match_re:
        print(match_re.group(1))
        return match_re.group(1)
    else:
        print("xsrf值不存在。。。。")
        return ""

def get_index():
    response=session.get("https://www.zhihu.com",headers=header)
    with open("index_page.html","wb") as f:
        f.write(response.text.encode('utf8'))
    print("OK")



def zhihu_login(account,password):
    #知乎登录
    if re.match("^1[3,5,8]\d{9}",account):
        print("手机号码登录")
        post_url="https://www.zhihu.com/login/phone_num"
        post_data={
            "_xsrf":get_xsrf(),
            "phone_num":account,
            "password":password
        }
    else:
        if "@" in account:
            #判断用户名是否为邮箱
            print("邮箱方式登录")
            post_url="https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": password
            }

    response_text = session.post(post_url, data=post_data, headers=header)
    session.cookies.save()

# zhihu_login("15137337097","9638527410.")
# get_index()
#get_xsrf()
is_login()































