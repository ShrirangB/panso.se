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

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

We have a [CONTRIBUTING.md](CONTRIBUTING.md) file with more information.

## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/) or later.

If you want to use this project with a different license, please contact me.

## Contact

- Email: [hello@panso.se](mailto:hello@panso.se)
- GitHub issues: [panso.se/issues](https://github.com/TheLovinator1/panso.se/issues)
