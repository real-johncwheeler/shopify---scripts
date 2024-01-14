import requests
import json

# Authentication details
ACCESS_TOKEN = ''
SHOP_NAME = ''
BASE_URL = ''

# Headers
headers = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': ''
}

def initProject():
    with open('secrets.json') as f:
        data = json.load(f)
        ACCESS_TOKEN = data['ACCESS_TOKEN']
        SHOP_NAME = data['SHOP_NAME']
        f.close()
    BASE_URL = f'https://{SHOP_NAME}.myshopify.com/admin/api/2024-01/'
    headers['X-Shopify-Access-Token'] = ACCESS_TOKEN
    

def delete_variant(product_id, variant_id, headers):
    # Endpoint to delete a variant
    url = f"{BASE_URL}products/{product_id}/variants/{variant_id}.json"

    # Send a DELETE request to remove the variant
    response = requests.delete(url, headers=headers)
    return response

# Fetch all products
def fetch_products():
    url = f"{BASE_URL}products.json"
    response = requests.get(url, headers=headers)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        try:
            # Parse JSON and return products
            return response.json().get('products', [])
        except json.JSONDecodeError:
            # Handle JSON decode error
            print("Error: Failed to decode JSON response")
            return []
    else:
        # Handle non-OK responses
        print(f"Error: Received status code {response.content}")
        return []

# Update each product
def update_product(product):
    product_id = product['id']
    author = None

    # Check if there's an option named "Author" at the product level
    author_option_index = None
    for i, option in enumerate(product['options']):
        if option['name'].lower() == "author":
            author_option_index = i
            break

    # If an "Author" option is found, look for its value in the variants
    if author_option_index is not None:
        for variant in product['variants']:
            # The option values are ordered as per the product['options']
            author_option_value = variant['option' + str(author_option_index + 1)]
            if author_option_value:
                author = author_option_value
                print(f"author: {author}")
                break
    else:
        return

    # If an author is found, update the metafield
    if author:
        for variant in product['variants']:
            # Check if variant's title matches the 'author_option_value' option
            title = variant['title']
            print(f"title: {title}")
            if title == author_option_value:
                # Send a request to delete the variant
                response = delete_variant(product_id, variant['id'], headers)
                print(f"response: {response.content}")
                if response.status_code == 200:
                    print(f"Variant with 'author_option_value' title deleted for product {product_id}")
                else:
                    print(f"Failed to delete variant for product {product_id}: {response.status_code}")
                break

        # Prepare the update payload
        update_payload = {
            "product": {
                "id": product_id,
                "metafields": [
                    {
                        "key": "author",
                        "value": author,
                        "type": "single_line_text_field",
                        "namespace": "custom"
                    }
                ]
            }
        }

        # Add metafield to the product
        update_product_url = f"{BASE_URL}products/{product_id}.json"
        response = requests.put(update_product_url, json=update_payload, headers=headers)
        print(f"response: {response.status_code}")
        # Code to remove the variant and update the product goes here
        # ...

    else:
        # Print error if no "Author" option is found
        print(f'Error: No "Author" option found for product {product_id}')


# Main process
def main():
    initProject()
    products = fetch_products()
    for product in products:
        update_product(product)

if __name__ == '__main__':
    main()
