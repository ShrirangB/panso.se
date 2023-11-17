from __future__ import annotations

import os
from sqlite3 import IntegrityError

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from loguru import logger
from sqlmodel import Session, SQLModel, create_engine, select

from api.description import description
from api.models import WebhallenProduct, WebhallenProductIn

load_dotenv(find_dotenv(), verbose=True)

SQLITE_URL: str = os.getenv("SQLITE_URL", "sqlite:///database.db")
DEBUG = bool(os.getenv("DEBUG", "False") == "True")

engine = create_engine(SQLITE_URL, echo=DEBUG)
SQLModel.metadata.create_all(engine)


app = FastAPI(
    title="Panso API",
    description=description,
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    contact={
        "name": "Panso.se",
        "url": "https://panso.se/about",
        "email": "api@panso.se",
    },
    license_info={
        "name": "GPL-3.0 License",
        "url": "https://github.com/TheLovinator1/panso.se/blob/master/LICENSE",
    },
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)


@app.get("/", include_in_schema=False, response_class=HTMLResponse, description="Index page")
def read_root() -> HTMLResponse:
    """Index page.

    Returns:
        HTMLResponse: Index page.
    """
    html = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Panso API</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
        </head>
        <body>
            <h1>Panso API</h1>
            <p>Go to <a href="/api/v1/docs">/api/v1/docs</a> for the OpenAPI documentation.</p>
            <p>Go to <a href="/api/v1/redoc">/api/v1/redoc</a> for the ReDoc documentation.</p>
            <p>Go to <a href="/api/v1/openapi.json">/api/v1/openapi.json</a> for the API schema.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)


@app.get("/api/webhallen/products")
def get_webhallen_products() -> list[WebhallenProduct]:
    """Get Webhallen products.

    Returns:
        str: Webhallen products.
    """
    with Session(engine) as session:
        statement = select(WebhallenProduct)
        products: list[WebhallenProduct] = session.exec(statement).all()
        if products is None:
            logger.debug("No products found")
            raise HTTPException(status_code=404, detail="No products found in database")

        logger.debug("products: {}", products)
        return products


@app.get("/api/webhallen/products/{product_id}")
def get_webhallen_product(product_id: int) -> WebhallenProduct:
    """Get Webhallen product.

    Args:
        product_id (int): Product ID.

    Returns:
        str: Webhallen product.
    """
    with Session(engine) as session:
        statement = select(WebhallenProduct).where(WebhallenProduct.product_id == product_id)
        product: WebhallenProduct | None = session.exec(statement).first()
        if product is None:
            logger.debug("No product found")
            raise HTTPException(status_code=404, detail="Product not found")

        logger.debug("product: {}", product)
        return product


@app.post("/api/webhallen/products/")
def post_webhallen_product(product: WebhallenProductIn) -> WebhallenProduct:
    """Post Webhallen product.

    Args:
        product_id (int): Product ID.
        product (WebhallenProduct): Product.

    Returns:
        str: Webhallen product.
    """
    product_id: int = product.product_id
    product_json: str = product.product_json

    if not product.product_json:
        logger.warning("product_json is empty")

    with Session(engine) as session:
        p = WebhallenProduct(product_id=product_id, product_json=product_json)
        try:
            session.add(p)
            session.commit()
            logger.debug("product: {}", p)
        except IntegrityError as e:
            logger.error("IntegrityError: {}", e)
            session.rollback()
            raise HTTPException(status_code=400, detail="Product already exists") from e
        else:
            return p
