import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import namedtuple

driver = webdriver.Chrome()
driver.maximize_window()
URL = 'https://www.pluralsight.com/search?q=python&categories=course'
driver.implicitly_wait(10)
driver.get(URL)
driver.find_element_by_css_selector(
    'body > div.cookie_notification.options > div > a.button.button--secondary.button--tiny.cookie_notification--opt_in').click()
time.sleep(4)
wait = WebDriverWait(driver, 20, poll_frequency=5)
file = open('pluralsight_14042019.csv', 'w+', encoding="utf-8")
file.write('Title,Link,Author,Level,Date,Duration,Average Rating,No of Users\n')
loadMoreButtonExists = True
details_list = []
Details = namedtuple('Details', ['title', 'link', 'author', 'level', 'date', 'length', 'rating_avg', 'no_of_users'])
while loadMoreButtonExists:
    try:
        element = wait.until(EC.element_to_be_clickable((By.ID, 'search-results-section-load-more')))
        time.sleep(5)
        driver.find_element_by_xpath("//a[@id='search-results-section-load-more']").click()
    except Exception as e:
        print(str(e))
        loadMoreButtonExists = False
pages = driver.find_elements_by_xpath("//div[@class='search-results-rows search-results-page clearfix']")
no_of_pages = len(pages)
print(no_of_pages)
for i in range(1, (no_of_pages + 1)):
    title_pages = driver.find_elements_by_xpath(
        "//div[@class='search-results-rows search-results-page clearfix'][" + str(i) + "]//a")
    for j in range(1, (len(title_pages) + 1)):
        title = driver.find_element_by_xpath("//div[@class='search-results-rows search-results-page clearfix'][" + str(
            i) + "]//div[@class='search-result columns'][" + str(j) + "]//a").text
        title = title.replace(',', ' ')
        author = driver.find_element_by_xpath("//div[@class='search-results-rows search-results-page clearfix'][" + str(
            i) + "]//div[@class='search-result columns'][" + str(
            j) + "]//div[@class='search-result__author']").text.replace('by ', '')
        author = author.replace(',',' / ')
        level = driver.find_element_by_xpath("//div[@class='search-results-rows search-results-page clearfix'][" + str(
            i) + "]//div[@class='search-result columns'][" + str(j) + "]//div[@class='search-result__level']").text
        date = driver.find_element_by_xpath("//div[@class='search-results-rows search-results-page clearfix'][" + str(
            i) + "]//div[@class='search-result columns'][" + str(j) + "]//div[@class='search-result__date']").text
        length = driver.find_element_by_xpath("//div[@class='search-results-rows search-results-page clearfix'][" + str(
            i) + "]//div[@class='search-result columns'][" + str(
            j) + "]//div[@class='search-result__length show-for-large-up']").text
        link = driver.find_element_by_xpath("//div[@class='search-results-rows search-results-page clearfix'][" + str(
            i) + "]//div[@class='search-result columns'][" + str(j) + "]//a").get_attribute("href")
        rating_count = ''
        try:
            rating_count = driver.find_element_by_xpath(
                "//div[@class='search-results-rows search-results-page clearfix'][" + str(
                    i) + "]//div[@class='search-result columns'][" + str(
                    j) + "]//div[@class='search-result__rating']").text
            rating_count = rating_count.replace('(', '')
            rating_count = rating_count.replace(')', '')
            rating = driver.find_elements_by_xpath(
                "//div[@class='search-results-rows search-results-page clearfix'][" + str(
                    i) + "]//div[@class='search-result columns'][" + str(
                    j) + "]//div[@class='search-result__rating']/i")
            avg = 0.0
            no_of_users = ''
            rating_avg = ''
            for e in rating:
                rate = e.get_attribute('class')
                if rate == 'fa fa-star':
                    avg += 1
                elif rate == 'fa fa-star-half-o':
                    avg += 0.5
            rating_avg = str(avg) + '/5.0'
            no_of_users = rating_count
        except NoSuchElementException as p:
            rating_avg = 'No Reviews Yet.'
            no_of_users = 'No Reviews Yet.'
        d1 = Details(title, link, author, level, date, length, rating_avg, no_of_users)
        details_list.append(d1)
list_sorted = list(sorted(details_list, key=lambda x: x.title))
for i in list_sorted:
    print(
        i.title + ',' + i.link + ',' + i.author + ',' + i.level + ',' + i.date + ',' + i.length + ',' + i.rating_avg
        + ',' + i.no_of_users)
    file.write(
        i.title + ',' + i.link + ',' + i.author + ',' + i.level + ',' + i.date + ',' + i.length + ',' + i.rating_avg
        + ',' + i.no_of_users + "\n")
print('Completed.')
file.close()