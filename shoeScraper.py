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
driver.execute_script("window.scrollTo(0, 150000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 300000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 450000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 600000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 800000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 1000000)")
time.sleep(3)


# if there is a link to continue loading, we should click that now.
if driver.find_element_by_partial_link_text('Load more items'):
    print('Loading more items')
    driver.find_element_by_partial_link_text('Load more items').click()
else:
    print('Scrolling down more')

# then see if there's more to load, just in case.
driver.execute_script("window.scrollTo(0, 1200000)")
time.sleep(3)
driver.execute_script("window.scrollTo(0, 1400000)")
time.sleep(3)

# parse the generated html using beautifulsoup4 and lxml
soup = BeautifulSoup(driver.page_source, 'lxml')
surls = soup.find_all('a', class_="product-image")

# set up a few empty arrays from which we will copy to a csv later on
links = []
names = []
prices = []
styles = []
items = []

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

    '''
    # todo:
    # 
    # get colors
    swatch_tags = []
    for color in color_tags:
        color.click()
        color_str = []
        item['color'] = color_str
        
        singleColor = subSoup.find('div', class_="input-box").ul.li.img['alt']

        # get sizes
        size_width_list = []
        size_tags = []
        for size in size_tags:
            size.click()
            size_str = []

            # get widths
            width_tags = []
            for width in width_tags:
                width.click()
                width_str = []
                availability_tag = []
                size_width_list.append([size_str, width_str, availability_tag.text])

        item['size_width_list'] = size_width_list
        items.append(item)

    return items
    '''

# after each page has been processed, we append each list of variables to a new column in a csv
df = pandas.DataFrame(data={"Name": names, "Price": prices, "Style Number": styles})  # "SKU": items,
df.to_csv("./mezlan.csv", sep=",", index="False")
