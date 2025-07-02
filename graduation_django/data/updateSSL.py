import certifi
import ssl
import os
import sys
import subprocess

# 获取 certifi 中的证书文件路径
ca_bundle = certifi.where()

# 设置环境变量
os.environ['SSL_CERT_FILE'] = ca_bundle

# 创建默认的 SSL 上下文
context = ssl.create_default_context(cafile=ca_bundle)

# 获取当前虚拟环境的 Python 解释器路径
python_executable = sys.executable
print(python_executable)

# 使用虚拟环境中的 pip 安装 pymysql
subprocess.check_call([python_executable, '-m', 'pip', 'install', r'D:\pyCharm\graduation_django\data\pymysql-1.1.1.tar.gz', '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple', '--trusted-host', 'pypi.tuna.tsinghua.edu.cn', '--upgrade'])