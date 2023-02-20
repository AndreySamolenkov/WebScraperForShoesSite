# Import the required libraries.
import csv
import requests
from bs4 import BeautifulSoup

# Create an empty list to store the product links.
product_links = []

# Define the URL of the web page to scrape.
url = 'https://www.blundstone.com/mens-boots'

# Send an HTTP request to the web page and get the response.
response = requests.get(url)

# Parse the HTML content of the web page using BeautifulSoup.
soup = BeautifulSoup(response.text, 'lxml')

# Find all the product links on the web page.
product_attributes = soup.find_all(class_='product-additional-attributes')

# Loop through each product attribute and get the product link.
for attribute in product_attributes:
    link = attribute.get('href')
    if link is not None:
        product_links.append(link)

# Create an empty list to store the product details.
products = []

# Loop through each product link and get its details.
for index, link in enumerate(product_links, start=1):
    # Send an HTTP request to the product page and get the response.
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    # Find the product name, price, and colors.
    name_elem = soup.find(class_='product-name')
    price_elem = soup.find(class_='normal-price')
    color_elems = [
        tooltip.text for tooltip in soup.find_all(class_='tooltip-content')]
    # Extract the text content of the product name, price, and colors.
    name = ' '.join(name_elem.text.split()[1:])
    price = price_elem.text.strip()
    colors = ', '.join(color_elems)
    # Create a list of the product details and add it to the products list.
    product = [index, name, price, colors, link]
    products.append(product)
    print(f'Product {index}: {name}')

# Write the product details to a CSV file.
with open('blundstone_products.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['№', 'Name', 'Price', 'Colors', 'Link'])
    writer.writerows(products)

# Print a message when the program finishes.
print('Done')
