
# from selenium.webdriver import Remote, ChromeOptions
# from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
# from bs4 import BeautifulSoup


# SBR_WEBDRIVER = 'https://brd-customer-hl_fc6b1f7b-zone-scraping_browser1:n5j1ffnzeb7b@brd.superproxy.io:9515'
# def scrape_website(website):
#     print("Launching EDGE...")

#     sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
#     with Remote(sbr_connection, options=ChromeOptions()) as driver:
        
#         driver.get(website)
        
#         print('Waiting captcha to solve...')
#         solve_res = driver.execute('executeCdpCommand', {
#             'cmd': 'Captcha.waitForSolve',
#             'params': {'detectTimeout': 10000},
#         })
#         print('Captcha solve status:', solve_res['value']['status'])
#         print('Navigated! Scraping page content...')
#         html = driver.page_source
#         return html


#we are no longer using 3rd party browser for scraping with captcha required websites and above code works for that


import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from bs4 import BeautifulSoup
import time

def create_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
        options=options
    )
    return driver

def scrape_website(website):
    print("Launching Chrome...")
    driver = create_driver()
    
    try:
        driver.get(website)
        print("Spiders are weaving their web... Please wait while we gather the information for you!")
        time.sleep(4)  # You might want to use WebDriverWait instead for more reliable waiting
        html = driver.page_source
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def cleanBC(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip() 
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=3000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]

print("successful execution")

