# SearchEngineSpider

## Architechture

## Experiment

### without main content analyzer

* one thread call back: 2475 requests 1:17.10
* 10 thread call back: 2453 requests 49.472

### with main content analyzer

#### Html5-Parser

* C gumbo backend with lxml

* 10 thread: 2250 request: 1:03.99
