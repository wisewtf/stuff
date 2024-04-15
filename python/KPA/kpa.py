# Key Price Alerts for AllKeyShop

import requests

def send_telegram_message(message):
    bot_token = 'TOKEN'
    chat_id = 'ID'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        pass
    else:
        print(response.text)

def get_offer(product_id):
    api_url = f"https://www.allkeyshop.com/blog/wp-admin/admin-ajax.php?action=get_offers&product={product_id}&currency=eur"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        offers = data.get('offers', [])
        if offers:
            first_offer = offers[0]
            eur_data = first_offer.get('price', {}).get('eur', {})
            price = eur_data.get('price')
            affiliate_url = first_offer.get('affiliateUrl')
            if eur_data.get('bestCoupon', {}):
                code = eur_data.get('bestCoupon', {}).get('code')
            else:
                code = 'no coupon'

            return price, affiliate_url, code
    return None, None, None

def main(product_ids):
    for product_id in product_ids:
        name, product_id = product_id.strip().split(', ')
        price, affiliate_url, code = get_offer(product_id)
        if price is not None and price <= 30:
            message = f"<b>{name}</b> @ <b>{price}EUR</b>.\n\nGet it <a href='{affiliate_url}'>here</a> (<code>{code}</code>)"
            send_telegram_message(message)
        else:
            exit

if __name__ == "__main__":
    product_ids = [
        "Dragon's Dogma, 102079",
    ]
    main(product_ids)