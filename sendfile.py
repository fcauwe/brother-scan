#!/usr/bin/python
import sys,os
from email.Utils import COMMASPACE, formatdate
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEImage import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders
import smtplib
import XmlDict

function=sys.argv[1]
user=sys.argv[2]
filename=sys.argv[3]
conf = XmlDict.loadXml("global.xml")
for option in conf["menu"]["option"]:
  if ((option["type"].lower()==function.lower()) and (option["name"]==user)):
    option_selected = option 


msg = MIMEMultipart()
msg['Subject'] = conf["subject"]
msg['From'] = conf["source"]
msg['To'] = COMMASPACE.join([option_selected["config"]])
msg['Date'] = formatdate(localtime=True)

text = "Your scanner happely delivered this pdf to your mailbox.\n"
msg.attach( MIMEText(text) )


part = MIMEBase('application', "pdf")
part.set_payload( open(filename,"rb").read() )
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename)  )
msg.attach(part)

mailer = smtplib.SMTP(conf["smtp"])
#mailer.connect()
mailer.sendmail(conf["source"],option_selected["config"] , msg.as_string())
mailer.close()

