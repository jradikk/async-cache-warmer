#!/usr/bin/env python3
import asyncio
import aiohttp
import sys
from lxml import etree
import requests
import functools
import datetime
import argparse
from tabulate import tabulate


parser = argparse.ArgumentParser(description='Asynchronous Magento Cache Warmer')
parser.add_argument('-s','--site', action="append", dest='sites', default=None)
parser.add_argument('-l','--limit', action="store", dest='limit', default=None)
args = parser.parse_args()
limit = args.limit
sites = args.sites


## Colorize ##
red='\033[0;31m'
green='\033[0;32m'
no_color='\033[0m'

tasks = []
results=[]
time_array=[]
failed_links=0
success_links=0

def get_links(mage_links):
    r = requests.get(mage_links)
    if "200" not in str(r):
        sys.exit(red + "Sitemap fetch failed for %s with %s. Exiting..." % (mage_links, r) + no_color)
    root = etree.fromstring(r.content)
    print ("The number of sitemap tags are %s" % str((len(root))) )
    links=[]
    for sitemap in root:
        children = sitemap.getchildren()
        links.append(children[0].text)
    return links


async def bound_warms(sem, url):
    async with sem:
        await warm_it(url)

async def warm_it(url):

    connection_started_time = None
    connection_made_time = None

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
        async with session.get(url) as response:
            time_delta=connection_made_time - connection_started_time
            time_taken="%s sec %s microsec" % (time_delta.seconds, time_delta.microseconds)
            if response.status!= 200:
                response_output=red + str(response.status) + no_color
            else:
                response_output=green + str(response.status) + no_color
                time_array.append(time_delta)
            results.append([url, response_output, time_taken])
            print('.', end='', flush=True)

if limit == None:
    print ("The concurrency limit isn't specified. Setting limit to 150")
    limit=150
else:
    print ("Setting concurrency limit to %s" % (limit))

sem = asyncio.Semaphore(int(limit))

for site in sites:
    print ("#############################################################################################")
    print ("Processing %s" % (site))
    loop = asyncio.get_event_loop()
    mage_links=get_links(str(site))
    for i in mage_links:
        task = asyncio.ensure_future(bound_warms(sem, i))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))

    for i in results:
        if "200" in i[1]:
            success_links+=1
        else:
            failed_links+=1

    avg_time = str((sum([ x.total_seconds() for x in time_array]))/len(time_array))
    print (tabulate(results, headers=['URL', 'Response code', 'Time']))
    print (tabulate([[str(failed_links), str(success_links), avg_time]], headers=['Failed', 'Successfull', 'Average Time']))
