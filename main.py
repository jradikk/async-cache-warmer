#!/usr/bin/env python3
import asyncio
import aiohttp
import sys
from lxml import etree
import requests
import functools
import datetime
from tabulate import tabulate

## Colorize ##
red='\033[0;31m'
green='\033[0;32m'
no_color='\033[0m'

tasks = []
results=[]
time_array=[]

def get_links(mage_links):
    r = requests.get(mage_links)
    root = etree.fromstring(r.content)
    print ("The number of sitemap tags are %s" % str((len(root))) )
    links=[]
    for sitemap in root:
        children = sitemap.getchildren()
        links.append(children[0].text)
    return links

async def warm_it(url):

    connection_started_time = None
    connection_made_time = None
    global failed_links
    global success_links

    class TimedResponseHandler(aiohttp.client_proto.ResponseHandler):
        def connection_made(self, transport):
            nonlocal connection_made_time
            connection_made_time = datetime.datetime.now()
            return super().connection_made(transport)

    class TimedTCPConnector(aiohttp.TCPConnector):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._factory = functools.partial(TimedResponseHandler, loop=loop)

        async def _create_connection(self, req):
            nonlocal connection_started_time
            connection_started_time = datetime.datetime.now()
            return await super()._create_connection(req)

    async with aiohttp.ClientSession(connector=TimedTCPConnector(loop=loop)) as session:
        failed_links = 0
        success_links = 0
        async with session.get(url) as response:
            time_delta=connection_made_time - connection_started_time
            time_taken="%s sec %s microsec" % (time_delta.seconds, time_delta.microseconds)
            if response.status!= 200:
                response_output=red + str(response.status) + no_color
                failed_links+=1
            else:
                response_output=green + str(response.status) + no_color
                success_links+=1
                time_array.append(time_delta)
            results.append([url, response_output, time_taken])

loop = asyncio.get_event_loop()

mage_links=get_links(sys.argv[1])

for i in mage_links:
    task = asyncio.ensure_future(warm_it(i))
    tasks.append(task)
loop.run_until_complete(asyncio.wait(tasks))

avg_time = str((sum([ x.total_seconds() for x in time_array]))/len(time_array))
print (tabulate(results, headers=['URL', 'Response code', 'Time']))
print (tabulate([[str(failed_links), str(success_links), avg_time]], headers=['Failed', 'Successfull', 'Average Time']))
