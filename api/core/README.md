# Core

This is our Django app that contains the core functionality of our project.

## Structure

Each store has its own folder in the root of the app. Each store folder contains the following files:

- `models.py` - contains the models for the store
- `api.py` - contains the API endpoints for the store
- `description.py` - contains OpenAPI descriptions so we don't have to clutter the `api.py` file with descriptions

## API

The API is built using [Django Ninja](https://django-ninja.rest-framework.com/).

The public API is available at [https://api.panso.se/](https://api.panso.se/).
Documentation for the API can be found [here](https://api.panso.se/docs). There is a [openapi.json](https://api.panso.se/openapi.json) file available as well.

### Rate limiting

There is no rate limit for this API so feel free to use it as much as you want.
