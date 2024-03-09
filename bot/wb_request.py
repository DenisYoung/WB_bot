import requests
import json

def qty_calc(sizes):
    qty = 0
    for size in sizes:
        for wh in size["stocks"]:
            qty += wh["qty"]
    return qty


def get_info_from_wb(article):
    r = requests.get(url=f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}").json()
    if len(r["data"]["products"]) == 0:
        return 0
    data = {
        "name": r["data"]["products"][0]["name"], 
        "article": article, 
        "price": r["data"]["products"][0]["salePriceU"], 
        "product_rating": r["data"]["products"][0]["reviewRating"], 
        "quantity_of_product": qty_calc(r["data"]["products"][0]["sizes"])

    }
    return data


#print(get_info_from_wb(200))