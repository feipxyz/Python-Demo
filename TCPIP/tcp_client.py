import socket
import threading
import time
import sys
import logging
import datetime

if __name__ == '__main__':
    """
    设置日志打印
    """
    # 日志格式
    logger = logging.getLogger(__name__)
    formatter1 = logging.Formatter(
        '%(asctime)-16s - %(thread)-4s - %(levelname)-7s - %(lineno)d - [%(funcName)s] - %(message)s')
    
    # 文件日志
    file_handler = logging.FileHandler('tcp_client.log')
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
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        logger.error('Failed to create socket. error: %s' % msg)
        sys.exit()
    
    logger.info("Socket Created")
    
    host = 'www.baidu.com'
    port = 80
    
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror as e:
        logger.error(e)
        sys.exit()
        
    logger.info("host: %s, ip: %s" % (host, remote_ip))
    
    try:
        client.connect((remote_ip, port))
    except socket.error as e:
        logger.info(e)
        sys.exit()
    
    logger.info("socket connect to %s, ip: %s" % (host, remote_ip))
    pass
    
    message = b"GET / HTTP/1.1\r\n\r\n"
    try:
        client.sendall(message)
    except socket.error as e:
        logger.error(e)
        sys.exit()
    
    logger.info("Message send successfully")
    
    rely = client.recv(1024)
    client.close()
    
    print(rely)