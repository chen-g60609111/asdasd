import email, getpass
from email.header import decode_header, make_header
from email.message import EmailMessage
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
ntu_id = input('NTU Student ID: ')
#ntu_id = "b08202022"   #寄件者學號
ntu_id = ntu_id.rstrip('@ntu.edu.tw')
to_send = input('to_send: ')
#to_send = "b08202022@ntu.edu.tw"   #收件者信箱
NTU_SMTP = 'smtps.ntu.edu.tw'
mime = MIMEMultipart()  # 建立MIMEMultipart物件

#C:\\Users\\user1\\Downloads\\1.png
    
with SMTP(NTU_SMTP) as smtp:
    # a connection is required before login and sendemail.
    # https://stackoverflow.com/questions/37224073/smtp-auth-extension-not-supported-by-server
    smtp.connect(NTU_SMTP, 587)
    smtp.ehlo()
    resp = smtp.starttls()
    #print(resp)
    if resp[0] == 220:
        smtp.login(ntu_id, getpass.getpass('Password: '))
        
        subject = input('Subject: ')
        content = input('Content: ')
        #subject = "注意!"
        #content = "注意!\n妳的帳號已被妳自己盜用，且被幸運大鵝造訪\n若要了解更多，請打開messenger確認訊息。"
        
        #若要輸入圖檔
        #image_path = "email_image.png"   #圖檔位置
        print("attach an image?")
        a = input("y or n:")
        
        
        
        if a == "y":
            image_path = input("圖片位置:")  #例image_path = "email_image.png"   #注意絕對路徑或相對路徑
            with open(image_path, "rb") as file:   #在第一個參數輸入圖片位置及檔名
                filecontent=file.read()
                mime.attach(MIMEImage(filecontent))   #增加圖檔
                mime["Content-Disposition"]='attachment; filename=%s' %image_path   #寫你的檔案名讓他可以找到，例:email_image.png
        else:
            print("do not attach any image")
        a = 123354686
        
        mime.attach(MIMEText(content))  # 郵件純文字內容
        mime["Content-Type"]="application/octet-stream"         
        mime["Subject"]=subject #撰寫郵件標題
        all_id = ntu_id+"@ntu.edu.tw"                
        #mime["Cc"]="@gmail.com, @gmail.com" #副本收件人       
           
        custom_from = input('自訂寄信者名稱? (y/\"enter\") ')[:1].lower() == 'y'
        if custom_from:
            all_id = input('Name <user@mail>\n')
            mime["From"]=all_id #撰寫你的暱稱或是信箱
        else:
            mime['From'] = ntu_id + '@ntu.edu.tw'
        mime["To"]=to_send #
        
        msg=mime.as_string() #將msg將text轉成str
        status=smtp.sendmail(mime['From'], [mime["To"]], msg)
        if status=={}:
            print("郵件傳送成功!")
        else:
            print("郵件傳送失敗!")
        smtp.quit()
