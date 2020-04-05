# _*_ coding: utf-8 _*_
import socket, time
from poetries import POUETRIES
import socketserver
import sys

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# sock.bind(('127.0.0.1', 56789))
# sock.listen(2)
#
# runing = True
# while runing:
#     c_sock, c_addr = sock.accept()
#     welcome = '欢迎你， 来自%s:%d的同学\r\n'%c_addr
#     c_sock.sendall(welcome.encode('gbk'))
#
#     while True:
#         cmd = b''
#         while not cmd.endswith(b'\r\n'):
#             cmd += c_sock.recv(1024)
#
#         cmd = cmd.strip()
#         if cmd in [b'bye', b'quit', b'exit']:
#             bye = '再见'.encode('gbk')
#             c_sock.sendall(bye+b'\r\n')
#             c_sock.close()
#             runing = cmd == b'bye'
#             break
#         else:
#             reply = '你说的是：'.encode('gbk')
#             c_sock.sendall(reply + cmd + b'\r\n')


def poetry_server():
    """古代诗词服务器"""

    delay = 0.1
    subjects = [item.split()[0] for item in POUETRIES]
    welcome = '欢迎来到古诗词库， 请输入序号后回车以选择你喜欢的诗词\r\n'
    welcome += '输入fast加速， 输入slow减速， 输入bye退出\r\n\r\n'
    for index, subject in enumerate(subjects):
        welcome += '%d %s\r\n'%(index+1, subject)
    welcome += '\r\n'
    welcome = welcome.encode('gbk')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 56789))
    sock.listen(2)

    runing = True
    while runing:
        c_sock, c_addr = sock.accept()
        c_sock.sendall(welcome)

        while True:
            cmd = b''
            while not cmd.endswith(b'\r\n'):
                cmd += c_sock.recv(1024)

            cmd = cmd.strip()
            if cmd in [b'bye', b'quit', b'exit']:
                c_sock.sendall('再见\r\n'.encode('gbk'))
                c_sock.close()
                runing = cmd ==b'bye'
                break
            elif cmd == b'help':
                c_sock.sendall(welcome)
            elif cmd == b'fast':
                delay /= 2
                c_sock.sendall('加速设置已完成\r\n'.encode('gbk'))
                c_sock.sendall('请选择诗词序号，输入help显示诗词目录：\r\n\r\n'.encode('gbk'))
            elif cmd == b'slow':
                delay *= 2
                c_sock.sendall('加速设置已完成\r\n'.encode('gbk'))
                c_sock.sendall('请选择诗词序号，输入help显示诗词目录：\r\n\r\n'.encode('gbk'))
            else:
                try:
                    index = int(cmd) -1
                    assert -1 < index < len(POUETRIES)
                except:
                    c_sock.sendall('请输入有效的诗词序号，输入help显示诗词目录\r\n\r\n'.
                                   encode('gbk'))
                    continue

                c_sock.sendall(b'---------------------\r\n')
                for line in POUETRIES[index].split('\n'):
                    for world in line:
                        c_sock.sendall(world.encode('gbk'))
                        time.sleep(delay)
                    c_sock.sendall(b'\r\n')
                c_sock.sendall(b'---------------------\r\n')
                c_sock.sendall('请选择诗词序号， 输入help显示诗词目录：\r\n\r\n'.encode('gbk'))


class PoetryTCPHandler(socketserver.StreamRequestHandler):
    """定义响应并处理Socket链接请求的类"""

    # def handle(self):
    #     """业务处理"""
    #
    #     delay = 0.1  # 诗词显示速度（字间隔时间）
    #     subjects = [item.split()[0] for item in POUETRIES]  # 诗词目录
    #     welcome = '欢迎来到风花雪月古诗词库, 请输入序号后回车以选择你喜欢的诗词\r\n'
    #     welcome += '输入fast加速，输入slow减速，输入bye退出\r\n\r\n'
    #     for index, subject in enumerate(subjects):
    #         welcome += '%d %s\r\n' % (index + 1, subject)
    #     welcome += '\r\n'
    #     welcome = welcome.encode('gbk')
    #     self.request.sendall(welcome)  # 发送欢迎信息和诗词目录
    #
    #     while True:
    #         cmd = self.rfile.readline().strip()
    #         if cmd == b'bye':
    #             self.request.sendall('再见\r\n'.encode('gbk'))
    #             self.request.close()
    #             break
    #         elif cmd == b'help':
    #             self.request.sendall(welcome)
    #         elif cmd == b'fast':
    #             delay /= 2
    #             self.request.sendall('加速设置已完成\r\n'.
    #                                  encode('gbk'))
    #             self.request.sendall('请选择诗词序号，输入help显示'
    #                                  '诗词目录：\r\n\r\n'
    #                                  .encode('gbk'))
    #         elif cmd == b'slow':
    #             delay *= 2
    #             self.request.sendall('加速设置已完成\r\n'.
    #                                  encode('gbk'))
    #             self.request.sendall('请选择诗词序号，输入help显示'
    #                                  '诗词目录：\r\n\r\n'
    #                                  .encode('gbk'))
    #         else:
    #             try:
    #                 index = int(cmd)-1
    #                 assert -1 < index < len(POUETRIES)
    #             except:
    #                 self.request.sendall('请输入有效的诗词序号，'
    #                                      '输入help显示诗词目录：'
    #                                      '\r\n\r\n'.encode('gbk'))
    #                 continue
    #
    #             self.request.sendall(b'----------------\r\n')
    #             for line in POUETRIES[index].split('\n'):
    #                 for word in line:
    #                     self.request.sendall(word.encode('gbk')
    #                                          )
    #                     time.sleep(delay)
    #                 self.request.sendall(b'\r\n')
    #             self.request.sendall(b'----------------\r\n')
    #             self.request.sendall('请输入有效的诗词序号，'
    #                                      '输入help显示诗词目录：'
    #                                      '\r\n\r\n'.encode('gbk'))

    def handle(self):
        print('%s:%d来了'%self.client_address)

        delay = 0.1



def poetries_server(port, use_threading):
    """古诗词服务器"""

    if use_threading:
        server = socketserver.ThreadingTCPServer(
            ('127.0.0.1', port), PoetryTCPHandler
        )
    else:
        server = socketserver.TCPServer(
            ('127.0.0.1', port), PoetryTCPHandler
        )
    server.serve_forever()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        port, use_threading = 56789, True
    elif len(sys.argv) == 2:
        port, use_threading = int(sys.argv[1]), True
    elif len(sys.argv) == 3:
        port, use_threading = int(sys.argv[1]), bool(int(sys.argv[2]))

    poetries_server(port, use_threading)
