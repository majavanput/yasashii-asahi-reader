from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://yasashii.asahi.com/'

def fetch_full_html(url):
    driver.get(url)
    html_source = driver.page_source
    return html_source

def fetch_article_urls():
    urls = []
    driver.find_element(By.ID, 'toggle-furigana').click()
    elements = driver.find_elements(By.CSS_SELECTOR, 'a.text-primary.d-block')

    for element in elements:
        urls.append(element.get_attribute("href"))

    return urls

def fetch_article(html):
    return html

def fetch_articles(urls):
    articles = []

    for url in urls:
        html = fetch_full_html(url)
        print(html)
        articles.append(fetch_article(html))

    return articles

driver = webdriver.Firefox()
fetch_full_html(link)
urls = fetch_article_urls()
result = fetch_articles(urls[:1])
# print(result)

driver.close()
