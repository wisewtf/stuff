# Key Price Alerts for AllKeyShop

import requests

def get_offer(product_id):
    api_url = f"https://www.allkeyshop.com/blog/wp-admin/admin-ajax.php?action=get_offers&product={product_id}&currency=eur"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        offers = data.get('offers', [])
        if offers:
            first_offer = offers[0]
            price = first_offer.get('price', {}).get('eur', {}).get('priceWithoutCoupon')
            return price
    return None

def main():
    with open('product_ids.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, product_id = line.strip().split(', ')
            price = get_offer(product_id)
            if price is not None:
                print(f"Price for {name}: {price}")
            else:
                print(f"No price found for {name}")

if __name__ == "__main__":
    main()
