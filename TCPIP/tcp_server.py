
import socket
import threading
import time
import sys
import logging
import datetime


def client_thread(conn, addr):
    logger.info('Accept new connection form %s:%s...' % addr)
    conn.send(b'Welcom to the server. Type something and hit enter\n')

    while True:
        data = conn.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        reply = '\n' + 'OK...' + data.decode('utf-8') + '\n'
        conn.send(reply.encode('utf-8'))

    conn.close()
    print('Connection from %s:%s closed.' % addr)

if __name__ == '__main__':
    """
    设置日志打印
    """
    # 日志格式
    logger = logging.getLogger(__name__)
    formatter1 = logging.Formatter(
        '%(asctime)-16s - %(thread)-4s - %(levelname)-7s - %(lineno)d - [%(funcName)s] - %(message)s')
    
    # 文件日志
    file_handler = logging.FileHandler('tcp_server.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter1)
    logger.addHandler(file_handler)
    
    # 控制台日志
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger.addHandler(console)
    
    # 最低输出级别
    logger.setLevel(logging.INFO)
    logger.info("------------------------START-----------------------")
    logger.info("start at :%s" % datetime.datetime.now())

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 8902))
    except socket.error as msg:
        logger.error('Failed to create socket. error: %s' % msg)
        sys.exit()
    logger.info("Socket created and bind successfully")
    
    # 连接数10
    server.listen(10)
    logger.info("Socket now listening...")

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=client_thread, args=(conn, addr))
        t.start()

