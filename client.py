# _*_ coding: utf-8 _*_
import socket
import time


def poetries_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    fp = sock.makefile(mode='rw')

    cmd = ''
    while True:
        while True:
            line = fp.readline().strip()
            if line == 'over':
                break
            elif cmd.isdigit():
                if line:
                    for word in line:
                        print(word, end='', flush=True)
                        time.sleep(1)
                    print()
            else:
                print(line)

        if cmd == 'bye':
            print('再见\n')
            break
        else:
            print('\n请选择诗词序号，输入bye退出，输入help查看目录', end='')
            cmd = input().strip()
            sock.sendall(cmd.encode('gbk')+b'\r\n')
            print()

    fp.close()
    sock.close()


if __name__ == '__main__':
    poetries_client('127.0.0.1', 56789)
