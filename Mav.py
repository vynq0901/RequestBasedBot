import requests

import json
from bs4 import BeautifulSoup


ses = requests.Session()

ses.post('https://maverikstudio.vn/account/login', data={
    'customer[email]': 'trungkien11@gmail.com',
    'customer[password]': 'fireblood1',
    'form_type': 'customer_login',
    'utf8': '✓',
    'g-recaptcha-response': '03AGdBq25HleAZXwAZnplo1KxkZrQVif78pHSrv2h5IxX9KHaZqmPBnfImi0jiQqgvIDzjIW3Ha_FYVsm81qSjngZ1357xTqN7LJLPY-SFXQEVPkpvuN7ACdWsfYWlshCblJhEb-dMqTXJXHOf1LV6KzSvDa33mjKrRptcMNxeG-GVS_9ZlZvzHr5zTtygK7HSbqJ8wVSS4344GqQScw48dZBQ7h4iX_1cCX9kOzIp4aV71UwWlo04lU_3MiQIR2llX4C7bjkHrFSOJ3DK-x6u0Z_BslaZYCtbVbmMp8HRMF7EOTpAkmGn-XcAFMuBSuFvXVOlbEf07prKOLHYWY036yMsweZcrhLMkqTrjCLnyga97CGhMzQPoA6MBiT3tmVzLCilP0APE7M2_cVeojxiUqU_ZIvGALeWThIKn5sReZV4E_gX7B3GR8lngbcXB-OlfqLWrywmrVtE'
})
all_prod_get = ses.get('https://maverikstudio.vn/collections/all')
bsoup = BeautifulSoup(all_prod_get.text, 'lxml')
prods = bsoup.find_all('a', {'class': 'image-resize'})
prod_link = ''
for e in prods:
    # e['href'].split("/")[2]
    curr_prod = e['href'].split("/")[2] 
    if 'chocolate' in curr_prod and 'pant' in curr_prod:
        prod_link = f'https://maverikstudio.vn/products/{curr_prod}.json'

prod_detail = ses.get(prod_link)
# print(prod_detail.json()['product']['variants'][0]['id'])

data = {
    'quantity': 1,
    'id': '1070261055'
}
headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/80.0.3987.95 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json',
        'X-HTTP-Method-Override': 'GET', 
        'Accept-Language': 'en-US,en;q=0.5',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://maverikstudio.vn',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://maverikstudio.vn',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
}
atc = ses.post('https://maverikstudio.vn/cart/add.js', data=data, headers=headers)
checkout = ses.get('https://maverikstudio.vn/checkouts.js')
checkout_token = checkout.json()['checkouts']['checkout_token']
print(checkout_token)
final = ses.get(f'https://maverikstudio.vn/checkouts/{checkout_token}', params={
    'checkout_user[email]': 'trungkien11@gmail.com',
    'billing_address[full_name]': 'Trung Kien',
    'billing_address[phone]': '0932506969',
    'utf8': '✓',
    'utf8': '✓',
    'billing_address[address1]': '91 nguyen hue',
    'customer_shipping_province': 32,
    'customer_shipping_district': 360,
    'customer_shipping_ward': 20245,
    'billing_address[city]': '',
    'billing_address[zip]': 70000,
    'shipping_rate_id': 1713412,
    'payment_method_id': 1002841852,
    'version': 4,
    'form_name': 'form_next_step'
}, headers={**headers, 'Referer': f'https://maverikstudio.vn/checkouts/{checkout_token}'})

print(final.text)
print(prod_detail.text)
# response2 = ses.get('https://thesimplixity.com/cart.js')

