# panso.se

The source code for [panso.se](https://panso.se).

## Development

- You need:
  - [Poetry](https://python-poetry.org/)
  - [Python](https://www.python.org/) 3.12 or later
  - [Microsoft C++ Build Tools](https://aka.ms/vs/17/release/vs_buildtools.exe) (If you're on Windows)
    - Choose Desktop development with C++ and uncheck optional components except for Windows 10/11 SDK and MSVC.
  - [PostgreSQL 16](https://www.postgresql.org/).
  - [Redis](https://redis.io/).
- Clone the repository
- Run `poetry install` to install dependencies
- Rename `.env.example` to `.env` and fill in the values
- Run `poetry shell` to enter the virtual environment
- Run `python .\manage.py runserver` to start the server or `Run and Debug` in VSCode

### Tests

- Run `python manage.py test` to run all tests
    - Run `python manage.py test --keepdb` to keep the test database to speed up tests

## Commands

Remember to run `poetry shell` before running any commands.

- `python manage.py scrape_webhallen`
  - Downloads all the URLs from https://www.webhallen.com/sitemap.product.xml and downloads the JSON for each product from the Webhallen API.
- `python manage.py scrape_sitemaps`
  - Downloads the URLs from these sitemaps add adds them to the database:
  - https://www.webhallen.com/sitemap.xml
  - https://www.webhallen.com/sitemap.home.xml
  - https://www.webhallen.com/sitemap.section.xml
  - https://www.webhallen.com/sitemap.category.xml
  - https://www.webhallen.com/sitemap.campaign.xml
  - https://www.webhallen.com/sitemap.campaignList.xml
  - https://www.webhallen.com/sitemap.infoPages.xml
  - https://www.webhallen.com/sitemap.product.xml
  - https://www.webhallen.com/sitemap.manufacturer.xml
  - https://www.webhallen.com/sitemap.article.xml
- `python manage.py rewrite_webhallen`
  - Convert our Webhallen JSON to a Django model.
- `python manage.py add_sections`
  - Loop through all JSON objects and create a new Django model for each section.
- `python manage.py add_eans`
  - Loop through all JSON objects and create a new Django model for each [EAN](https://en.wikipedia.org/wiki/International_Article_Number).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/) or later.

If you want to use this project with a different license, please contact me.

## Contact

- Email: [hello@panso.se](mailto:hello@panso.se)
- GitHub issues: [panso.se/issues](https://github.com/TheLovinator1/panso.se/issues)
