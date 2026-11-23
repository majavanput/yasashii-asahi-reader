from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

link = 'https://yasashii.asahi.com/'

def fetch_full_html(url):
    driver.get(url)

    wait = WebDriverWait(driver, 30)
    toggle = driver.find_element(By.ID, 'toggle-furigana')

    if not toggle.is_selected():
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'label[for="toggle-furigana"]')
        )).click()

    wait.until(EC.element_located_to_be_selected(
        (By.ID, 'toggle-furigana')
    ))

    # Selecting the toggle starts an asynchronous furigana request.
    sections = ['#page-title']
    if driver.find_elements(By.ID, 'main'):
        sections.append('#main')

    for section in sections:
        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f'{section} .tsutaeruRuby__translation')
            ),
            message=f'Furigana did not load in {section} for {url}'
        )

    return driver.page_source

def fetch_article_urls():
    urls = []

    elements = driver.find_elements(By.CSS_SELECTOR, 'a.text-primary.d-block')

    for element in elements:
        urls.append(element.get_attribute("href"))

    return urls

def fetch_article(html):
    soup = BeautifulSoup(html, 'html.parser')
    article = {}

    for key, selector in (('title', 'h1#page-title'), ('main', 'div#main')):
        section = soup.select_one(selector)
        if section is None:
            raise ValueError(f'Article HTML is missing {selector}')

        for original in section.select('.tsutaeruRuby__phrase'):
            original.decompose()

        for tag in section.find_all(['span', 'p']):
            if tag.name == 'p':
                tag.insert_after('\n')
            tag.unwrap()

        article[key] = section.decode_contents().replace('\xa0', '').strip()

    return article

def fetch_articles(urls):
    articles = []

    for url in urls:
        html = fetch_full_html(url)
        articles.append(fetch_article(html))

    return articles

driver = webdriver.Firefox()
fetch_full_html(link)
urls = fetch_article_urls()
result = fetch_articles(urls[:1])
print(result)

driver.close()
