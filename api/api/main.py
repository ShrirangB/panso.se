from __future__ import annotations

from typing import Union

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

description = """
This is the API for the Panso project.

## Authentication

Only internal endpoints need authentication, the rest is open to the public.

## Rate limiting

There is no rate limiting. Feel free to scrape the API as much as you want.

## API versioning

The API is versioned using the URL path. The current version is `v1`. The current version is also the default version.

## API documentation

The API documentation is available at [/api/v1/docs](/api/v1/docs) and [/api/v1/redoc](/api/v1/redoc).

## API schema

The API schema is available at [/api/v1/openapi.json](/api/v1/openapi.json).

## License

All the data is scraped from other websites. The data is not owned by me. The data is owned by the respective websites.
The data is licensed under the respective licenses of the websites.

The code is licensed under the GPL-3.0 License. See the
 [LICENSE](https://github.com/TheLovinator1/panso.se/blob/master/LICENSE) file for more information.

## Contact

If you have any questions, feel free to contact me at [api@panso.se](mailto:api@panso.se).

## Source code

The source code is available at [GitHub](https://github.com/TheLovinator1/panso.se/).
"""


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
