from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# HTML class names.
ITEM_CLASS = "cell productThumbnailItem" # li tag
ITEM_NAME_CLASS = "productDescLink" # a tag
ITEM_BRAND_CLASS = "productBrand" # div tag
PRICE_CLASS = "regular" # span tag
DISCOUNT_PRICE_CLASS = "discount" # span tag
NEXTPAGE_BUTTON_CLASS = "next-page" #li tag

# First pages.
WOMENS_SHOES = "https://www.macys.com/shop/shoes/all-womens-shoes?id=56233"

# Chrome driver and pandas dataframe for data storage.
driver = webdriver.Chrome()
df_macys = pd.DataFrame(columns=["item_brand", "item_name", "item_price", "item_link"])


def fetch_page(pageURL, dataframe):
    '''
    Fetches data from a single html page.
    Relevant only to Macy's.
    :param pageURL: http address
    :param dataframe: pandas dataframe for data storage
    :return: manipulated dataframe and a BeatifulSoup object of corresponding page
    '''
    driver.delete_all_cookies()
    driver.get(pageURL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for article in soup.find_all("li", class_=ITEM_CLASS):
        try:
            item_brand = article.find("div", class_=ITEM_BRAND_CLASS).text.lstrip().rstrip()
            print(item_brand)
            item_name = article.find("a", class_=ITEM_NAME_CLASS)["title"][1:]
            print(item_name)
            item_price = None
            if article.find("span", PRICE_CLASS):
                item_price = article.find("span", PRICE_CLASS).text
            if article.find("span", DISCOUNT_PRICE_CLASS):
                item_price = article.find("span", DISCOUNT_PRICE_CLASS).text
            item_price = item_price.\
                    replace(" ", "").replace("\t", "").replace("\n", "").replace("Sale", "").replace("Now", "")
            print(item_price)
            item_link = "https://www.macys.com" + article.find("a", class_=ITEM_NAME_CLASS)["href"]
            print(item_link)
            dataframe = dataframe.append({"item_brand": item_brand,
                                          "item_name": item_name,
                                          "item_price": item_price,
                                          "item_link": item_link}, ignore_index=True)
        except:
            None
    return dataframe, soup


def fetch_all(mainURL, dataframe):
    '''
    Fetch all pages starting from the given https address.
    Stores into `../data/macys.csv` everytime the page changes.
    Relevant only to Macy's and page must have next button.
    :param mainURL: starting http address
    :param dataframe: pandas dataframe for data storage
    :return: manipulated dataframe
    '''
    curURL = mainURL
    while True:
        tempURL = curURL
        dataframe, soup = fetch_page(curURL, dataframe)
        if soup.find("li", class_=NEXTPAGE_BUTTON_CLASS):
            link = soup.find("li", class_=NEXTPAGE_BUTTON_CLASS)
            curURL = "https://www.macys.com" + link.div.a["href"]
            print("current URL: " + curURL)
        if curURL == tempURL:
            break
    dataframe.to_csv("../data/macys.csv")
    return dataframe

    driver.quit()

# Execute for all women's shoes on Macy's.
# fetch_all(WOMENS_SHOES, df_macys)