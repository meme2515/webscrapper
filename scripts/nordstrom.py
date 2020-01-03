from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# HTML class names.
ITEM_CLASS = "_1AOd3 QIjwE" # article tag
ITEM_DESCRIPTION_CLASS = "YbtDD _18N5Q" # div tag
ITEM_NAME_CLASS = "_5lXiG _1sMDh _2PDR1" # a tag
ITEM_PRICE_CLASS = "_3wu-9" # span tag
NEXTPAGE_BUTTON_CLASS = "_2WIqd" # a tag

# First pages.
WOMENS_SHOES = "https://shop.nordstrom.com/c/womens-shoes"

# Chrome driver and pandas dataframe for data storage.
driver = webdriver.Chrome()
df_nordstrom = pd.DataFrame(columns=["item_name", "item_price", "item_link"])


def fetch_page(pageURL, dataframe):
    '''
    Fetches data from a single html page.
    Relevant only to Nordstrom.
    :param pageURL: http address
    :param dataframe: pandas dataframe for data storage
    :return: manipulated dataframe and a BeatifulSoup object of corresponding page
    '''
    driver.get(pageURL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for article in soup.find_all("article", class_=ITEM_CLASS):
        try:
            item_name = article.find("a", class_=ITEM_NAME_CLASS).text
            print(item_name)
            for price in article.find_all("span", class_=ITEM_PRICE_CLASS):
                item_price = price.text
            print(item_price)
            item_link = "https://shop.nordstrom.com" + article.find("a", class_=ITEM_NAME_CLASS)["href"]
            print(item_link)
            dataframe = dataframe.append({"item_name": item_name,
                                          "item_price": item_price,
                                          "item_link": item_link}, ignore_index=True)
        except:
            None
    return dataframe, soup


def fetch_all(mainURL, dataframe):
    '''
    Fetch all pages starting from the given https address.
    Stores into `nordstrom.csv` everytime the page changes.
    Relevant only to Nordstrom and page must have next button.
    :param mainURL: starting http address
    :param dataframe: pandas dataframe for data storage
    :return: manipulated dataframe
    '''
    curURL = mainURL
    while True:
        tempURL = curURL
        dataframe, soup = fetch_page(curURL, dataframe)
        nav_links = soup.find_all("a", class_=NEXTPAGE_BUTTON_CLASS)
        for link in nav_links:
            if link.span.text == "Next":
                curURL = mainURL + link["href"]
                print("current URL: " + curURL)
        if curURL == tempURL:
            break
    dataframe.to_csv("../data/nordstrom.csv")
    return dataframe

    driver.quit()

# Execute for all women's shoes on Nordstrom.
# fetch_all(WOMENS_SHOES, df_nordstrom)