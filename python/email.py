import os
import re
import shutil
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os
import time
timestamp = time.strftime('%Y-%m-%d', time.gmtime(time.time() - 24 * 60 * 60))
#smtp configure
smtpserver = 'smtp.live.com'
port = 587
smtpuser = 'wanggenguo@outlook.com'
smtppass = 'yourpass'
sendto = "wanggenguo@sina.com"

srcPath = "E:/Projects/imleagues/"
targetPathG = "E:/Projects/imleaguse other/reviewgenerator/"
dirfile = "dirs.dat"

# send email
def sendMail(to, subject, text, files=[]):
    assert type(to) == list
    assert type(files) == list
    fro = smtpuser	
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text,'html'))
    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
        % os.path.basename(file))
        msg.attach(part)
	#print msg.as_string()
    try:
        smtp = smtplib.SMTP()
	#smtp.set_debuglevel(1)
        smtp.connect(smtpserver,port)
	smtp.starttls()
        smtp.login(smtpuser, smtppass)
        smtp.sendmail(smtpuser, to, msg.as_string())
        smtp.quit()
	print "the email is sent~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    except Exception, e:
        print e, "the email send failure!!"

def main():
	file = open(dirfile)
	a = file.readline()
	flag = ""
	settings = {"bugid":"noid","sendemail":"false","address":sendto}
	messages=""
	while a:
		if len(a) > 2 and a[0:2] == "##":
			flag = a.strip()
			print a
		else:
			if flag == "##setting":
				a = a.strip()
				vals = a.split("=")
				if len(vals)<2:
					continue
				if vals[0] in settings:
					settings[vals[0]] = vals[1]
			elif  flag == "##files":
				b = settings["bugid"]
				bugname = "[IM_CRR]_("+b+")"
				rarFile = targetPathG+"[IM_CRR]_("+b+").rar"
				targetPath = targetPathG+"[IM_CRR]_("+b+")/imleagues/"
				if os.path.exists(targetPath):
				  shutil.rmtree(targetPath)
				  print "remove old files"
				if os.path.isfile(rarFile):
				  os.remove(rarFile)
				  print "remove old rar files"
				while a and a[0:2] != "$$":
				  m = re.match(r"\s*(.*/)(.*)",a)
				  if m:
					dirstr = m.group(1)
					filename = m.group(2)
					if not os.path.exists(targetPath+dirstr):  
					   os.makedirs(targetPath+dirstr)
					open(targetPath+dirstr+filename, "wb").write(open(srcPath+dirstr+filename, "rb").read())
					print "copy %s"%(dirstr+filename)
				  a = file.readline()
				os.system("\"C:\\Program Files (x86)\\WinRAR\\Rar.exe\" a -r "+bugname+" "+bugname)
			elif  flag == "##messages":
				messages = messages + a
		a = file.readline()
	if settings["sendemail"] == "true" or settings["sendemail"] == "yes" :
		sendMail(settings["address"].split(","),bugname,messages,[bugname+".rar",])
	os.system("pause")
main()
