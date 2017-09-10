from scrapy.cmdline import execute

import sys
import  os

# os.path.abspath(__file__) 当前文件的目录地址
#os.path.dirname(os.path.abspath(__file__)) 当前目录的父目录
#当前目录
print(os.path.abspath(__file__))
#当前目录的父目录
print(os.path.dirname(os.path.abspath(__file__)))


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy","crawl","jobbole"])
execute(["scrapy","crawl","zhihu"])









































