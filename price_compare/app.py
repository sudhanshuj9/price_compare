from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'
}


def flipkart(name):
    try:
        name1 = name.replace(" ", "+")
        flipkart_url = f'https://www.flipkart.com/search?q={name1}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
        res = requests.get(flipkart_url, headers=headers)

        print("\nSearching in Flipkart....")
        soup = BeautifulSoup(res.text, 'html.parser')

        if soup.select('._4rR01T'):
            flipkart_name = soup.select('._4rR01T')[0].getText().strip()
            if name.upper() in flipkart_name.upper():
                flipkart_price = soup.select('._30jeq3')[0].getText().strip()
                return flipkart_name, flipkart_price, flipkart_url

        elif soup.select('.s1Q9rs'):
            flipkart_name = soup.select('.s1Q9rs')[0].getText().strip()
            if name.upper() in flipkart_name.upper():
                flipkart_price = soup.select('._30jeq3')[0].getText().strip()
                return flipkart_name, flipkart_price, flipkart_url

        return None, '0', None
    except:
        return None, '0', None


def amazon(name):
    try:
        name1 = name.replace(" ", "-")
        name2 = name.replace(" ", "+")
        amazon_url = f'https://www.amazon.in/{name1}/s?k={name2}'
        res = requests.get(amazon_url, headers=headers)

        print("\nSearching in Amazon...")
        soup = BeautifulSoup(res.text, 'html.parser')
        amazon_page = soup.select('.a-color-base.a-text-normal')
        amazon_page_length = len(amazon_page)
        for i in range(amazon_page_length):
            name = name.upper()
            amazon_name = soup.select('.a-color-base.a-text-normal')[i].getText().strip()
            if name in amazon_name.upper():
                amazon_price = soup.select('.a-price-whole')[i].getText().strip()
                return amazon_name, amazon_price, amazon_url

        return None, '0', None
    except:
        return None, '0', None


def convert(price):
    price = price.replace(" ", "").replace("INR", "").replace(",", "").replace("₹", "")
    return int(float(price))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        return render_template('results.html', product_name=product_name)
    return render_template('index.html')



@app.route('/results', methods=['POST'])
def results():
    product_name = request.form.get('product_name')
    flipkart_name, flipkart_price, flipkart_url = flipkart(product_name)
    amazon_name, amazon_price, amazon_url = amazon(product_name)

    if flipkart_name is None:
        flipkart_name = "No product found!"
        flipkart_price = '0'
        flipkart_url = None
    else:
        flipkart_price = convert(flipkart_price)

    if amazon_name is None:
        amazon_name = "No product found!"
        amazon_price = '0'
        amazon_url = None



@app.route('/results', methods=['POST'])
def results():
    product_name = request.form.get('product_name')
    flipkart_name, flipkart_price = flipkart(product_name)
    amazon_name, amazon_price = amazon(product_name)

    if flipkart_name is None:
        flipkart_name = "No product found!"
        flipkart_price = '0'
    else:
        flipkart_price = convert(flipkart_price)

    if amazon_name is None:
        amazon_name = "No product found!"
        amazon_price = '0'

    else:
        amazon_price = convert(amazon_price)

    price_difference = flipkart_price - amazon_price


    # Determine which website is more affordable
    if flipkart_price == 0 and amazon_price == 0:
        affordable_website = "No product found!"
    elif flipkart_price == 0:
        affordable_website = "Amazon"
    elif amazon_price == 0:
        affordable_website = "Flipkart"
    elif flipkart_price < amazon_price:
        affordable_website = "Flipkart"
    else:
        affordable_website = "Amazon"

    return render_template('results.html', flipkart_name=flipkart_name, flipkart_price=flipkart_price,
                           amazon_name=amazon_name, amazon_price=amazon_price, affordable_website=affordable_website,
                           flipkart_url=flipkart_url, amazon_url=amazon_url)

    return render_template('results.html', flipkart_name=flipkart_name, flipkart_price=flipkart_price,
                           amazon_name=amazon_name, amazon_price=amazon_price, price_difference=price_difference)


if __name__ == '__main__':
    app.run(debug=True)
