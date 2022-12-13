# 程序说明
## download_data_orthoDB.py 
从orthoDB中下载果蝇的直系同源基因，最新版本添加了处理两个同源簇的情况，比如在搜索页面发现found 2 group。最新版本允许得到每个物种的同源基因，且不需要间接解析html。 将结果存储json
## analysis1.py
远程和NR数据库做比对，并从match序列中，基于NCBI同一个基因簇得到对应的基因组，并定位到对应的match，从中获取邻居基因
