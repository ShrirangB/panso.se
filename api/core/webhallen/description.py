"""This file contains the description for Swagger and ReDoc."""

list_product_description = r"""
This is a mirror of `https://www.webhallen.com/api/product/{id}`.

## Warning ⚠️
This is not only products, the API also returns categories.

### Product example:
The following URL returns a product:
[https://www.webhallen.com/api/product/20000](https://www.webhallen.com/api/product/20000)

### Category example:
The following URL returns a category:
[https://www.webhallen.com/api/product/4](https://www.webhallen.com/api/product/4)

### How to tell the difference?

Product has:
* `product`: dict

Category has:
* `id`: int
* `section`: dict
* `mainCategoryPath`: list
* `CategoryTree`: str
* `categories`: list
"""
