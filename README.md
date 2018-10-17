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

### 发送email例子
```
{
  "content": "这是一封测试邮件",
  "fromEmail": "noreply@cyber-life.cn",
  "subject": "发送测试邮件",
  "toEmail": "thomas@cyber-life.cn",
  "fromName": "cyber-life.cn"
}
```
### 发送sms例子
```
{
  "content": "{'ekey':'123456'}",
  "smsUser": "Test",
  "fromName": "cyber-life.cn",
  "phone": "13910586316",
  "templateId": "151"
}
```

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

### 安装后修改配置参数
```
vi /etc/cyberlife/mailroom.conf

EMAIL_API_USER = ***
EMAIL_API_KEY = ***
SMS_API_USER = ***
SMS_API_KEY = ***
```
将***修改为正确的值
