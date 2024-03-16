import requests
import json

def qty_calc(sizes):
    qty = 0
    for size in sizes:
        for wh in size["stocks"]:
            qty += wh["qty"]
    return qty


def get_info_from_wb(article):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return None
    
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        return None
    
    if not data.get("data", {}).get("products"):
        return None
    
    product = data["data"]["products"][0]
    product_info = {
        "name": product["name"],
        "article": article,
        "price": product["salePriceU"],
        "product_rating": product["reviewRating"],
        "quantity_of_product": qty_calc(product["sizes"])
    }
    return product_info


#print(get_info_from_wb(200))