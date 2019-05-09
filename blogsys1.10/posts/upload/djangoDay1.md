---
title: "Django基础（一）- 搭建基本的网站"
categories:
- Django
tags:
- 网站搭建
photo:
- http://pk0mla8df.bkt.clouddn.com/dj4.png
top: true
---



#### 虚拟环境：
- 安装：pip install virtualenv
   使用： virtualenv --no-site-packages -p 环境位置  项目名
       --no-site-packages:表示创建的环境为纯净环境，不安装其他的

- pip使用：
       pip list : 查看安装的库
       pip install xxx: 安装
   激活虚拟环境： winows: activate 
             mac/linux : 直接执行scurce activat
   **注意：要到环境文件中激活虚拟环境**
   ![](/img/dj1.png) 

退出虚拟环境  deactivate


#### Django项目创建：
django-admin startproject 项目名称
**注意切换到你的代码文件目录下创建**

启动命令： python manage.py runserver 默认ip为127.0.0.1 默认端口为8000

修改启动端口： python manage.py runserver 端口
修改ip和端口： python manage.py runserver ip:端口
                  ip参数：0.0.0.0 表示任何人都可以通过公网ip访问Django项目
                  端口prot参数：如果端口设置为80，表示改端口可以不用写
**在pycharm中切换为上面创建的虚拟环境，执行启动命令，结果如下：**
![](/img/dj2.png) 
打开上图网址，最基本的Django框架就OK了
![](/img/dj3.png)

#### settings.py配置文件设置
- 语言设置
  LANGUAGE_CODE = 'zh-hans' 表示中文 LANGUAGE_CODE = 'en-us' 表示英文
  设置时区：TIME_ZONE = 'Asia/Shanghai'
  时区默认是UTC：世界标准时间，也就是平常说的零时区。 北京时间表示东八区时间，即UTC+8
  再打开网页刷新一下
  ![](/img/dj4.png)
- 连接数据库
  修改配置文件
```python
# 原配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 修改后的
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名', # 要是存在的数据库
        'PORT': '端口（MySQL默认的为3306）',
        'USER': '用户名', # MySQL的用户名和密码
        'PASSWORD' : '密码',
        'HOST' : 'MySQL服务器的ip地址'
    }
}
```
**需要安装MySQL客户端
在创建Terminal中输入 pip install pymysql 即可**
```python
# 安装pymysql：使用pymysql连接数据库：因为python3没有MySQLdb驱动，无法直接连接MySQL
# 在工程目录的__init__.py文件中加入
import pymysql

pymysql.install_as_MySQLdb()
```
在上面的网址后面加上admin，(http://127.0.0.1:8000/admin)再访问
![](/img/dj5.png)
#### 添加账号
- 迁移：
  迁移默认文件：python manage.py migrate
  ![](/img/dj6.png)
  ![](/img/dj7.png)
  添加管理员账号：python manage.py createsuperuser
  ![](/img/dj8.png)
  现在在运行服务器就可以用刚才创建的账号登陆了
  ![](/img/dj9.png)

**以上就是django基础框架搭建
自定义模板待续...**
#### 补充：
MVC（model,view,controller）模式是所有框架遵循的模式

    M: 模型（M）是数据的表述。它不是真正的数据，而是数据的接口。使用模型从数据库中获取数据时，无需知道底层数据库错综复杂的知识。模型通常还会为数据库提供一层抽象，这样同一个模型就能使用不同的数据库
    V: 视图（V）是你看到的界面。它是模型的表现层。在电脑中，视图是你在浏览器中看到的 Web 应用的页面，或者是桌面应用的 UI。视图还提供了收集用户输入的接口
    C: controller，控制器 控制模型和视图之间的信息流动。它通过程序逻辑判断通过模型从数据库中获取什么信息，以及把什么信息传给视图。它还通过视图从用户那里收集信息，并且实现业务逻辑：变更视图，或者通过模型修改数据，或者二者兼具
严格来说，Django的模式应该是MVT模式，本质上和MVC没什么区别，也是各组件之间为了保持松耦合关系，只是定义上有些许不同  
MVT (model,view,template )：
	M： models.py 模型层：定义模型和数据库中表
	V:  views.py  视图层：定义业务逻辑
	T:  templates  模板，定义HTML的地方

MVT模式是由MVT模式演变出来的