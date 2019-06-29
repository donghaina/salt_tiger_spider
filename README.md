# 电子书爬虫

### 获取代码
```shell
git clone https://github.com/donghaina/salt_tiger_spider
```

### 安装依赖
```shell
pip install -r requirements.txt
```
### 创建数据库和表
```shell
create database book
source book.sql
```

### 爬取全部电子书
```shell
python run.py
```
### 爬取指定标签的电子书
```shell
scrapy crawl english_book_spider -a tag=PHP
```
