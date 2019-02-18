# shoeScraper - singleShoe
# an automated tool for discovering and retrieving data
# on available merchandise from a specified distributors
import time
import pandas
from bs4 import BeautifulSoup
from selenium import webdriver

# import libraries used in this sequence
# create a selenium session with firefox
# open the assigned url
mainPage = 'http://mezlan.com/mezlan'
driver = webdriver.Firefox()
driver.get(mainPage)

# scroll down for all the items to load
driver.execute_script("window.scrollTo(0, 15000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 30000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 45000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 60000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 80000)")
time.sleep(3)

# todo: Load More Items: <div class="ias-trigger ias-trigger-next" ...
# todo: id="ias_trigger_1550457300768"><a>Load more items</a></div>

# parse the generated html using beautifulsoup4 and lxml
soup = BeautifulSoup(driver.page_source, 'lxml')
surls = soup.find_all('a', class_="product-image")

# set up a few empty arrays from which we will copy to a csv later on
links = []
names = []
prices = []
styles = []

# loops pulling the URL for each shoe into a list
for i in surls:
    links.append(i.get('href'))

# for each found url, we open a page and pull the needed information
for link in links:
    driver.get(link)
    subSoup = BeautifulSoup(driver.page_source, 'lxml')
    name = subSoup.find('span', class_='h1')
    nameClean = name.text
    price = subSoup.find('span', class_="price")
    priceClean = price.text
    style = subSoup.find('div', class_="product-style")
    styleClean = style.text
    names.append(nameClean)
    prices.append(priceClean)
    styles.append(styleClean)

# after each page has been processed, we append each list of variables to a new column in a csv
df = pandas.DataFrame(data={"Name": names, "Price": prices, "Style Number": styles})
df.to_csv("./mezlan.csv", sep=",", index="False")
