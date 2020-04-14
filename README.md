# SearchEngineSpider

## 流程

1. 發出 Request
2. pipelines
  1. parser(get main content)
  2. to db
3. put new urls into url pool

## Architecture

* engine: main spider
* item: define Item to store data
* pipelines: change item 
* utils
  * parser: html5parser to get urls, main_content, ....
  * url_pool: url queue
  * function: simple operation

### engine

* 使用 aiohttp 做異步爬蟲
* 

## Experiment

### without main content analyzer

* one thread call back: 2475 requests 1:17.10
* 10 thread call back: 2453 requests 49.472

### with main content analyzer

#### Html5-Parser

* C gumbo backend with lxml
* 10 thread: 2250 request: 1:03.99

### Full

* with Cpp Url Queue: 2:43.79 7115 requests
* with Python Url Queue: 6:55.70 23746
