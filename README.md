# Async-cache-warmer
Asynchronous website cache warmer. Initially created to warm up magento cache. 

![alt text](http://www.smsconnexion.com/wp-content/uploads/2012/02/magento.png)  ![alt text](http://d1marr3m5x4iac.cloudfront.net/images/block/I0-001/038/274/846-1.png_/docker-containerization-and-devops-beg-46.png)

The main purpose of the script is to "warm up" magento cache after flushing it. Script parses sitemap.xml file and asynchronously loads each page. 

## Usage: 
1)./main.py -h
```
usage: main.py [-h] [-s SITES] [-l LIMIT]

Asynchronous Magento Cache Warmer

optional arguments:
  -h, --help            show this help message and exit
  -s SITES, --site SITES
  -l LIMIT, --limit LIMIT
```
Example:
./main.py -s "<URL/with/path/to/sitemap.xml>" -s "<URL/with/path/to/sitemap.xml>" -l <number of concurrent threads> 

2) docker run jradik/async-cache-warmer -h
```
usage: main.py [-h] [-s SITES] [-l LIMIT]

Asynchronous Magento Cache Warmer

optional arguments:
  -h, --help            show this help message and exit
  -s SITES, --site SITES
  -l LIMIT, --limit LIMIT
```

Example:

docker run jradik/async-cache-warmer -s "<URL1/with/path/to/sitemap.xml>" -s "<URL2/with/path/to/sitemap.xml>" -l <number of concurrent threads> 

## Examples: 

 
![alt text](https://raw.githubusercontent.com/jradikk/async-cache-warmer/master/examples/example1.png)
![alt text](https://raw.githubusercontent.com/jradikk/async-cache-warmer/master/examples/example2.png)

