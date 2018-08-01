from lxml import html
import lxml.html
import requests
import csv
from csv import writer

# variables
selection = raw_input("Path to File: ")
csv_header = ("post_title", "post_name", "ID", "post_excerpt", "post_content", "post_status", "menu_order", "post_date",
              "post_parent", "post_author", "comment_status", "sku", "downloadable", "virtual", "visibility", "stock",
              "stock_status", "backorders", "manage_stock", "regular_price", "sale_price", "weight", "length", "width",
              "height", "tax_status", "tax_class", "upsell_ids", "crosssell_ids", "featured", "sale_price_dates_from",
              "sale_price_dates_to", "download_limit", "download_expiry", "product_url", "button_text",
              "meta:_yoast_wpseo_focuskw", "meta:_yoast_wpseo_title", "meta:_yoast_wpseo_metadesc",
              "meta:_yoast_wpseo_metakeywords", "images", "downloadable_files", "tax:product_type", "tax:product_cat",
              "tax:product_tag", "tax:product_shipping_class", "meta:total_sales", "attribute:pa_color",
              "attribute_data:pa_color", "attribute_default:pa_color", "attribute:size", "attribute_data:size",
              "attribute_default:size")

# write header to output file (runs once)
with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(csv_header)


def scrape(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    title2 = str(lxml.html.parse(url).find(".//title").text)
    title2 = title2.replace('-' + title2.split("-", 1)[1], '')
    price = tree.xpath("//span[@itemprop='price']//text()")
    i = 0
    for span in tree.cssselect('span'):
        clas = span.get('class')
        rel = span.get('rel')
        if clas == "packaging-des":
            if rel != None:
                if i == 0:
                    weight = rel
                elif i == 1:
                    dim = str(rel)
                i = i + 1

    weight = weight
    height = dim.split("|", 3)[0]
    length = dim.split("|", 3)[1]
    width = dim.split("|", 3)[2]
    # Sometimes aliexpress doesn't list a price
    # This dumps a 0 into price in that case to stop the errors
    if len(price) == 1:
        price = float(str(price[0]))
    elif len(price) == 0:
        price = int(0)
    for inpu in tree.cssselect('input'):
        if inpu.get("id") == "hid-product-id":
            sku = inpu.get('value')
    for meta in tree.cssselect('meta'):
        name = meta.get("name")
        prop = meta.get("property")
        content = meta.get('content')
        if prop == 'og:image':
            image = meta.get('content')
        if name == 'keywords':
            keywords = meta.get('content')
        if name == 'description':
            desc = meta.get('content')
    listvar = (
    [str(title2), str(name), '', '', str(desc), 'publish', '', '', '0', '1', 'open', str(sku), 'no', 'no', 'visible',
     '', 'instock', 'no', 'no', str(price * 2), str(price * 1.5), str(weight), str(length), str(width), str(height),
     'taxable', '', '', '', 'no', '', '', '', '', '', '', '', '', '', str(keywords), str(image), '', 'simple', '', '',
     '', '0', '', '', '', '', '', '', '', ''])
    with open("output.csv", 'ab') as f:
        writer = csv.writer(f)
        writer.writerow(listvar)


def read(selection):
    lines = []
    j = 0
    with open(selection) as f:
        for line in f:
            lines.append(line)
        lines = map(lambda s: s.strip(), lines)
    for j in range(len(lines)):
        scrape(str(lines[j]))


read(selection)
