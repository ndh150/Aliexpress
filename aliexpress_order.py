import csv

import requests


def _get_transactions(*, product_id, page_num):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }
    params = {
        'productId': product_id,
        'type': 'default',
        'page': page_num
    }
    url = 'https://feedback.aliexpress.com/display/evaluationProductDetailAjaxService.htm'
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json()


def get_product_transactions(*, product_id, transaction_pages=1):
    transactions = []
    for page_num in range(1, transaction_pages + 1):
        current_transactions = _get_transactions(
            product_id=product_id,
            page_num=page_num
        )
        transactions.extend(current_transactions['records'])
    return transactions


if __name__ == '__main__':
    product_id = '32821244791'
    transactions = get_product_transactions(
        product_id=product_id,
        transaction_pages=3
    )

    with open('{}_transactions.csv'.format(product_id), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=('date', 'country', 'pieces'))
        writer.writeheader()
        for transaction in transactions:
            writer.writerow({
                'date': transaction['date'],
                'country': transaction['countryCode'],
                'pieces': transaction['quantity']
            })