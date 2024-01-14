
# shopifyAddMeta.py

This project helps [shopify](https://www.shopify.com/) merchants correct an issue where they accidently used varient fields instead of metafields. Metafields are useful to dynmaically reference on our shopify webpage. 

In this example, for each product that has the [variant](https://help.shopify.com/en/manual/products/variants) "author", I'm creating an "author" [metafield](https://help.shopify.com/en/manual/custom-data/metafields). 


## Environment Variables

To run this project, you will need to add the following environment variables to the secrets.json

`ACCESS_TOKEN`  == This is your shopify api access token. https://shopify.dev/docs/apps/auth/admin-app-access-tokens

`SHOP_NAME`  == this is your shopify's store name (https://{SHOP_NAME}.myshopfiy.com)


## Installation
Download and install [Python 3.12.1](https://www.python.org/downloads/release/python-3121/)

Download and install [Visual Studio Code](https://code.visualstudio.com/)

    
## Deployment

Open visual studio code, then open the workspace, and then open a terminal window.

```bash
pip install requests
py shopifyAddMeta.py
```
To use metafields on your shopify store:
```bash
<a href=\"\/collections\/all?filter.p.m.custom.author={{ product.metafields.custom.author.value }}&sort_by=title-ascending\">Find books by this same author<\/a>
```
## Authors

- [@real-johncwheeler](https://www.github.com/real-johncwheeler)

