# env
* python 3.8.0+
* 安装python依赖 [requirements](requirements.txt)
```shell
pip install -r requirements.txt 
```
# setting & run
1. Set the address of the crawl result file where var name is _FILE_BASE_PATH in crawler.py
```python
# like this
_FILE_BASE_PATH = '/Users/zhangqixin/web3go_workspace/web3go_github/web3go-network-data-collection-agent/ApolloX-Doc/ApolloX_Finance/result/'
```
2. run python
```shell
python crawler.py
```
# result
Find it in the path you set
![Finance_result](Finance_result.png)