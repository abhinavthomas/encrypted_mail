#!/usr/bin/env/python
"""
    Script to send your mails encrypted end to end.
    Author : Abhinav Thomas
    
"""
#importing the AES encryption module from Crypto library
from Crypto.Cipher import AES
import getpass #for entering key
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

def encrypt(key,iv,msg):
	"""
		Encypting the message using AES-CBC algorithm (minimum 24 bit level)
	"""
	obj = AES.new(key, AES.MODE_CBC, iv)
	enmsg = obj.encrypt(msg)
	return enmsg

def decrypt(key,iv,enmsg):
	"""
		Decrypting the cipher using AES-CBC algorithm
	"""
	obj = AES.new(key, AES.MODE_CBC, iv)
	msg = obj.decrypt(enmsg)
	print msg

def fileen():
	"""
		Function to enctrypt message and store it into file
	"""
	length=0
	while length<16:
		keyi = getpass.getpass(prompt='Enter the key: ',stream=None)
		length = len(keyi)
		print "Too small key" if length<16 else "key accepted"

	ivi = raw_input('Enter the initialization vector[false message]: ')
	key = keyi.zfill(24) if length<24 else keyi.zfill(32)
	iv = ivi.zfill(16)[0:16]

	texti = raw_input('Enter the message [hit enter to send]: ')
	text = texti.rjust((len(texti)//16 +1)*16)
	texttomail = encrypt(key,iv,text) # the ecyption function
	fp = open('encfile.txt','wb')
	fp.write(texttomail)
	fp.close()

def send():
	"""
		Here the key, iv, and mailing details are taken and and given to the encrypt function and send
	"""
	fromaddr = raw_input("ENTER YOUR EMAIL ADDRESS: ")
	toaddr = raw_input("ADDRESS YOU WANT TO SEND TO : ")
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = raw_input("SUBJECT OF THE MAIL: ")
	 
	body = "Find the attatchments"
	msg.attach(MIMEText(body, 'plain'))
	fileen()
	filename = "encfile.txt"
	attachment = open("encfile.txt", "rb")
	 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	 
	msg.attach(part)
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, getpass.getpass("YOUR MAIL ID PASSWORD: "))
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

def filede(loc):
	"""
		Function to decrypt message in a file given in the given location
	"""
	length=0
	while length<16:
			keyi = getpass.getpass(prompt='Enter the key: ',stream=None)
			length = len(keyi)
			print "Too small key" if length<16 else "key accepted"

	ivi = raw_input('Enter the initialization vector[false message]: ')
	key = keyi.zfill(24) if length<24 else keyi.zfill(32)
	iv = ivi.zfill(16)[0:16]
	fp = open(loc,'rb')
	msg = fp.read()
	decrypt(key,iv,msg)


def main():
	choice = raw_input('1. Send mail \n2. Decrypt message \nEnter your choice: ')
	if choice == '1':
		send() #send mails
	else:
		loc = raw_input('Enter the path to file: ')
		filede(loc)
		
if __name__ == '__main__':
	main() #getting the credentials for encrypting