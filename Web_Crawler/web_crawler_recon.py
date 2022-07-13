#!/user/bin/env python

import requests
import re
import urllib
from urllib.parse import urlparse
# https://docs.python.org/3/library/urllib.parse.html
import time

# replace "example.com" with web server of your choice
target_url = "https://www.example.com/"
target_links = []


def extract_links_from(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))


# recursive crawling (URL extracted from HTML source code)
def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urllib.parse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)
            # time.sleep(1)


# for brute force method
def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass


# brute force method of finding subdomains using predefined dict
def discover_subdomains():
    with open("subdomains-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = word + "." + target_url
            subdomain_response = request(test_url)
            if subdomain_response:
                print("[+] Discovered subdomain -->" + test_url)


# brute force method of finding file paths using predefined dict
def discover_hidden_path():
    with open("files-and-dirs-wordlist.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = target_url + "/" + word
            hidden_path_response = request(test_url)
            if hidden_path_response:
                print("[+] Discovered URL -->" + test_url)


crawl(target_url)
