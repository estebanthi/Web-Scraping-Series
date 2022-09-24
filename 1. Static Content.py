import requests
from bs4 import BeautifulSoup
import pandas as pd


if __name__ == "__main__":
    keywords = "It Stephen King"
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={}&_sacat=0&LH_TitleDesc=0&_odkw={}".format(keywords, keywords)
    response = requests.get(url)
    source_code = response.text
    soup = BeautifulSoup(source_code, "html.parser")

    items = soup.find_all("li", {"class": "s-item"})
    scraped_items = []
    for item in items:
        title = item.find("span", {"role": "heading"}).text
        price = float(item.find("span", {"class": "s-item__price"}).text.split("$")[1].replace(",", ""))
        is_a_bid = item.find("span", {"class": "s-item__bids"}) is not None
        link = item.find("a", {"class": "s-item__link"})["href"]
        scraped_items.append({
            "title": title,
            "price": price,
            "is_a_bid": is_a_bid,
            "link": link
        })

    sorted_items = sorted(scraped_items, key=lambda x: x["price"])
    items_df = pd.DataFrame(sorted_items)

    filename = "ebay_{}.csv".format(keywords.replace(" ", "_"))
    items_df.to_csv(filename, index=False)
