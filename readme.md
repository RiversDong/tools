# 程序说明
## download_data_orthoDB.py 
从orthoDB中下载果蝇的直系同源基因，最新版本添加了处理两个同源簇的情况，比如在搜索页面发现found 2 group。最新版本允许得到每个物种的同源基因，且不需要间接解析html。 将结果存储json
## analysis1.py
远程和NR数据库做比对，并从match序列中，基于NCBI同一个基因簇得到对应的基因组，并定位到对应的match，从中获取邻居基因
## MgeDetect_v1
用来批量注释基因组中的可移动元件，这个程序依赖了MobileElementFind和blast程序
### 安装
1. 安装MobileElementFinder，参照https://pypi.org/project/MobileElementFinder/
2. 安装blast,并放到环境变量
### 运行
```
./MgeDetect_v1 -query /home/chuand/pks_dis/data/test -tmp /home/chuand/pks_dis/data/tmp/ -output /home/chuand/pks_dis/data/test_res/
```
-query 存放基因组的序列文件夹路径，比如这个路径下放了10个基因组，则会注释这10个基因组的MGEs，所以可以把所有的基因组放到一个文件夹里面\
-tmp 临时文件的存放路径\
-output会将所有的预测结果放到这个路径下面
