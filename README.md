# Book Reservation Platform

## Requirements 

前端使用 vue 框架以及 `vite` 脚手架。

后端使用 python+flask 框架，数据库使用 sqlite。整体依赖库如下

```txt
blinker==1.8.2
certifi==2024.6.2
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
contourpy==1.1.1
cycler==0.12.1
Flask==3.0.3
Flask-Cors==4.0.1
Flask-JWT-Extended==4.6.0
Flask-SQLAlchemy==3.1.1
fonttools==4.53.0
greenlet==3.0.3
idna==3.7
importlib_metadata==7.1.0
importlib_resources==6.4.0
itsdangerous==2.2.0
Jinja2==3.1.4
kiwisolver==1.4.5
MarkupSafe==2.1.5
matplotlib==3.7.5
numpy==1.24.4
packaging==24.1
pillow==10.3.0
PyJWT==2.8.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
pytz==2024.1
requests==2.32.3
six==1.16.0
SQLAlchemy==2.0.30
typing_extensions==4.12.2
urllib3==2.2.2
Werkzeug==3.0.3
zipp==3.19.2
```

可以通过如下指令安装。

```shell
pip install -r server/requirements.txt
```

## Runing

本项目为前后端分离项目，因此二者都需要启动

前端可在`client`目录下运行`npm run dev`，通过`localhost:5173`访问

后端需要先初始化数据库，可以运行通过`init_db.py`完成

```shell
python server/init_db.py
```

然后启动flask服务器即可

```python
python server/run.py
```
