# cyber-mailroom
send mail by http://sendcloud.sohu.com api
make rpm package on centos7, but I think this project can run on anything linux.

## 功能
* 使用sendcloud发送email
* 使用sendcloud发送短信


## REST API文档
http://mailroom.cyber-life.cn/swagger/spec.html


## Demo
* http://mailroom.cyber-life.cn/mailroom/web/index
* http://mailroom.cyber-life.cn/smsbox/web/index


## 安装软件包
### 安装 nginx
```
yum -y install nginx
systemctl start nginx
systemctl enable nginx
```
### 安装 pip
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```
### 安装 tornado
```
pip install --upgrade pip
pip install tornado==4.3
```
### 安装python依赖包
```
yum install git
git clone https://github.com/SerenaFeng/tornado-swagger.git
cd tornado-swagger
python setup.py install
pip install requests
```

## 安装 cyber-mailroom
```
rpm -Uvh cyber-mailroom-1.0.0-3_git_ed98137.x86_64.rpm --force
```
