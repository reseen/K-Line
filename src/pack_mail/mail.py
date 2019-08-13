import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
 
# 第三方 SMTP 服务
mail_host = "smtp.exmail.qq.com"              # 设置服务器
mail_user = "trendalarm@mallocx.com"          # 用户名
mail_pass = "123123"                          # 口令 
 
receivenm = 'reseen'                           # 接收邮件名称
receivers = 'yanyang@mallocx.com'              # 接收邮件地址

mail_subject = 'Python SMTP 邮件测试'           # 邮件标题
mail_message = 'Python 邮件发送测试...'          # 邮件正文

# 邮件打包
message = MIMEText(mail_message, 'plain', 'utf-8')
message['Subject'] = mail_subject
message['From'] = formataddr(['TrendAlarm', mail_user])
message['To'] = formataddr([receivenm, receivers])
 
try:
    smtpObj = smtplib.SMTP_SSL() 
    smtpObj.connect(mail_host, 465)         # 465 为 SMTP 端口号
    smtpObj.login(mail_user,mail_pass)  
    smtpObj.sendmail(mail_user, receivers, message.as_string())
    print("邮件发送成功")

except smtplib.SMTPException:
    print("Error: 无法发送邮件")