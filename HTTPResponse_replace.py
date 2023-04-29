'''
Commit message (English):
feat: replace HTTP/0.0 with HTTP/1.0 in HTTP response version

This commit adds a modification to the _read_status method of http.client.HTTPResponse, which replaces the HTTP version "HTTP/0.0" with "HTTP/1.0" in the response header. This improvement ensures that the returned version is always valid and compliant with the HTTP/1.0 specification.

Commit message (中文):
feat: 在HTTP响应版本中将HTTP/0.0替换为HTTP/1.0

本次提交对http.client.HTTPResponse的_read_status方法进行了修改，将HTTP响应头中的版本号"HTTP/0.0"替换为"HTTP/1.0"。该改进确保返回的版本号始终有效，并符合HTTP/1.0规范。
'''

import http.client
import ssl
from http.client import HTTPException, LineTooLong, RemoteDisconnected, BadStatusLine

_MAXLINE = 65536


def read_line(fp):
    line = str(fp.readline(_MAXLINE + 1), "iso-8859-1")
    if len(line) > _MAXLINE:
        raise LineTooLong("status line")
    if not line:
        # Presumably, the server closed the connection before
        # sending a valid response.
        raise RemoteDisconnected("Remote end closed connection without"
                                 " response")
    return line


def parse_status_line(line):
    try:
        version, status, reason = line.split(None, 2)
    except ValueError:
        try:
            version, status = line.split(None, 1)
            reason = ""
        except ValueError:
            # empty version will cause next test to fail.
            version = ""
    return version, status, reason


def check_version(version, line):
    if not version.startswith("HTTP/"):
        raise BadStatusLine(line)
    if version == "HTTP/0.0":
        version = "HTTP/1.0"
    return version


def check_status_code(status, line):
    try:
        status = int(status)
        if status < 100 or status > 999:
            raise BadStatusLine(line)
    except ValueError:
        raise BadStatusLine(line)
    return status


def _read_status(self):
    line = read_line(self.fp)
    version, status, reason = parse_status_line(line)
    version = check_version(version, line)
    status = check_status_code(status, line)
    return version, status, reason


http.client.HTTPResponse._read_status = _read_status

# 创建一个忽略SSL错误的HTTPS连接
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
conn = http.client.HTTPSConnection('Your IP Addess', context=context)

# 发送GET请求
conn.request('GET', '/')

# 获取响应并打印状态码、原因、版本信息和响应内容
resp = conn.getresponse()

content = resp.read().decode('utf-8')

# 接下来想做什么都行
print(f'Status: {resp.status}')
print(f'Reason: {resp.reason}')
print(f'Version: {resp.version}')
print(f'Content: {content}')
