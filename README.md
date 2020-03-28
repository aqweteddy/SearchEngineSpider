# SearchEngineSpider

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
