# Python3-reptile
Python3 爬虫
以功能项目为中心，展开学习


# 登录模块
###  文件列表：
####     account.txt            账号列表(网站名，网站登录url，登录名，登录密码，验证码url)
####     cookie.txt             cookie列表(网站名，网站登录url，登录名，浏览器已登录cookie，cookie文件名)
####     cookie_网站名_登录名.txt    cookie文件(cookie字段)
###  功能概述：
####    第一路径：从《账号列表》读取账户信息，获取【验证码】，保存验证码到本地，人工验证，交互输入，登录，保存cookie文件
####                                     ，账户密码配置，登录，保存cookie文件
####    第二路径：                        ，读取路径下cookie_网站名_登录名.txt，用已有cookie文件，登录，刷新cookie文件
####    第三路径，                        ，匹配account.txt的cookie字段，利用cookie配置request，登录，保存cookie文件





# 其他模块
