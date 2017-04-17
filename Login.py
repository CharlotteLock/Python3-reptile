import urllib.request
import urllib.parse
import http.cookiejar
import time
import re


class Email(object):
    def __init__(self):
        self.path_email = "account.txt"
        self.path_cookie = "cookie.txt"
        self.path = ''
        self.matcher_email = re.compile(r'(\s*)(?P<url_name>\S*)(\s*)(?P<url_login>\S*)(\s*)(?P<email>\S*)(\s*)(?P<passwd>\S*)')
        self.matcher_cookie = re.compile(r'(\s*)(?P<url_name>\S*)(\s*)(?P<url_login>\S*)(\s*)(?P<email>\S*)(\s*)(?P<cookie>.*)')
        self.url_name = ''
        self.url_login = ''
        self.email = ''
        self.passwd = ''
        self.cookie = {}

    def loadFile(self):
        self.path = self.path_cookie
        self.loadFileInfo()
        self.path = self.path_email
        self.loadFileInfo()

    def loadFileInfo(self):
        with open(self.path) as file:
            self.readFileInfo(file)
            time.sleep(0.1)

    def readFileInfo(self, file):
        for line in file:
            try:
                self.extractFileInfo(line)
            except:
                pass

    def extractFileInfo(self, line):
        if self.path == self.path_email:
            m = self.matcher_email.match(line)
            ret = m.groupdict()
            self.url_name = ret.get('url_name', 'None')
            self.url_login = ret.get('url_login', 'None')
            self.email = ret.get('email', 'None')
            self.passwd = ret.get('passwd', 'None')
            self.loginEmail()
        elif self.path == self.path_cookie:
            m = self.matcher_cookie.match(line)
            ret = m.groupdict()
            self.url_name = ret.get('url_name', 'None')
            self.url_login = ret.get('url_login', 'None')
            self.email = ret.get('email', 'None')
            self.cookie[self.url_name] = {self.email : ret.get('cookie', 'None')}

    def loginEmail(self):
        login = Login()
        if self.url_name not in self.cookie.keys() or self.email not in self.cookie[self.url_name]:
            login.setLoginInfo(url_name=self.url_name, url_login=self.url_login, email=self.email, passwd=self.passwd)
        else:
            login.setLoginInfo(url_name=self.url_name, url_login=self.url_login, email=self.email, cookie=self.cookie[self.url_name][self.email])
        login.login()


class Login(object):
    def __init__(self):
        self.url_name = ''
        self.url_login = ''
        self.email = ''
        self.passwd = ''
        self.cookie = ''


    def setLoginInfo(self, *args, **kwargs):
        self.url_name = kwargs.get('url_name', 'None')
        self.url_login = kwargs.get('url_login', 'None')
        self.email = kwargs.get('email', 'None')
        self.passwd = kwargs.get('passwd', 'None')
        self.cookie = kwargs.get('cookie', 'None')
        self.CodeUrl = 'http://icode.renren.com/getcode.do?t=web_login&rnd=Math.random()'

    def login(self):
        if self.cookie == 'None':
            self.path_cookies = "cookie_{}_{}.txt".format(self.url_name, self.email)
            self.cj = http.cookiejar.LWPCookieJar(self.path_cookies)
            self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
            urllib.request.install_opener(self.opener)
            if 0: # no code
                Form_Data = {'email': self.email, 'password': self.passwd}
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
            else:
                picture = self.opener.open(self.CodeUrl).read()
                local = open('./image.jpg', 'wb')
                local.write(picture)
                local.close()
                SecretCode = input('输入验证码: ')
                Form_Data = {'email': self.email,
                             'icode': SecretCode,
                             'origURL': 'http://www.renren.com/home',
                             'captcha_type': 'web_login',
                             'password': self.passwd}
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
            req = urllib.request.Request(self.url_login,  urllib.parse.urlencode(Form_Data).encode(),headers=headers)
            self.operate = self.opener.open(req)
            thePage = self.operate.read()
            self.cj.save(ignore_discard=True, ignore_expires=True)
        else:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
                'cookie': self.cookie
            }
            req = urllib.request.Request(self.url_login, headers=headers)
            response = urllib.request.urlopen(req)
            thePage = response.read()
        html = open('./Page.html', 'wb')
        html.write(thePage)
        html.close()
        print('....ok')


if __name__ == '__main__':
    email_check = Email()
    email_check.loadFile()
