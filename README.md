# Async-cache-warmer
Asynchronous website cache warmer. Initially created to warm up magento cache. 

![alt text](http://www.smsconnexion.com/wp-content/uploads/2012/02/magento.png)  ![alt text](http://d1marr3m5x4iac.cloudfront.net/images/block/I0-001/038/274/846-1.png_/docker-containerization-and-devops-beg-46.png)

The main purpose of the script is to "warm up" magento cache after flushing it. Script parses sitemap.xml file and asynchronously loads each page. 

## Usage: 
1) ./main.py "http://example.com/sitemap.xml"

2) docker run jradik/async-cache-warmer "http://example.com/sitemap.xml"

