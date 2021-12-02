from threading import Thread
import requests
import time
from bs4 import BeautifulSoup
from Helper import get_login_token

class CoppingThread(Thread):
    def __init__(self, task):
        Thread.__init__(self)
        self.task = task
    
    def run(self):
        start_time = time.time()
        login_token = get_login_token()
        ses = requests.Session()
        print(f"[--{self.task.email}--] -> LOGGING IN...!!!")
        ses.post('https://maverikstudio.vn/account/login', data={
            'customer[email]': self.task.email,
            'customer[password]': self.task.password,
            'form_type': 'customer_login',
            'utf8': '✓',
            'g-recaptcha-response': login_token
        })
        size_id = ''
        keyword1 = self.task.keyword1
        keyword2 = self.task.keyword2
        while True:
            print(f"[--{self.task.email}--] -> FINDING PRODUCT...!!!")
            found = False
            prod_link = ''
            time.sleep(1)
            all_prod_get = ses.get('https://maverikstudio.vn/collections/all')
            bsoup = BeautifulSoup(all_prod_get.text, 'lxml')
            prods = bsoup.find_all('a', {'class': 'image-resize'})
            for e in prods:
                curr_prod = e['href'].split("/")[2] 
                if keyword1 in curr_prod and keyword2 in curr_prod:
                    found = True
                    prod_link = f'https://maverikstudio.vn/products/{curr_prod}.json'
                    break
            if found == True: 
                print(f"[--{self.task.email}--] -> PRODUCT FOUND: {prod_link}...!!!")
                prod_detail = ses.get(prod_link)
                for var in prod_detail.json()['product']['variants']:
                    if var['title'].lower() == self.task.size:
                        size_id = var['id']
                # size_id = prod_detail.json()['product']['variants'][3]['id']
                break
        data = {
            'quantity': self.task.quantity,
            'id': size_id
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
        print(f"[--{self.task.email}--] -> ADDING TO CARD...!!!")
        print(f"[--{self.task.email}--] -> PROCESSING TO CHECKOUT...!!!")
        final = ses.get(f'https://maverikstudio.vn/checkouts/{checkout_token}', params={
            'checkout_user[email]': self.task.email,
            'billing_address[full_name]': self.task.password,
            'billing_address[phone]': self.task.phone,
            'utf8': '✓',
            'utf8': '✓',
            'billing_address[address1]': self.task.address,
            'customer_shipping_province': self.task.province_code,
            'customer_shipping_district': self.task.district_code,
            'customer_shipping_ward': self.task.ward_code,
            'billing_address[city]': '',
            'billing_address[zip]': 70000,
            'shipping_rate_id': 1518654,
            'payment_method_id': 1002804234,
            'version': 4,
            'form_name': 'form_next_step'
        }, headers={**headers, 'Referer': f'https://maverikstudio.vn/checkouts/{checkout_token}'})
        print(final.text)
        print(f"[--{self.task.email}--] -> {str(time.time() - start_time)}")
