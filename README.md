# DA AYR Beta WebApp

This is a repo created and maintained by The National Archives for the Access Your Records (AYR) project. It holds a Flask application based from the [Land Registry GOV.UK Frontend Flask template repo](https://github.com/LandRegistry/govuk-frontend-flask). Currently the intention is to deploy this via AWS Lambda and API Gateway but you can run it however you would like.

## Getting started

### Setup Poetry environment

[Install poetry](https://python-poetry.org/docs/)
Check poetry has been installed using:

```shell
poetry --version
```

Then install the required dependencies using:

```shell
poetry install
```

You can now access the virtual environment created by poetry with:

```shell
poetry shell
```

in which you can run all of the following commands. Alternatively you can prefix all of the following commands with `poetry run`.

### Get GOV.UK Frontend assets

For convenience a shell script has been provided to download and extract the GOV.UK Frontend distribution assets

```shell
./build.sh
```

### CSS / SCSS

SASS is being used to build the local CSS files. To build the css files you can use npm to build by first installing the npm packages and then using:

```shell
npm run build
```

or if you'd like to watch for changes use:

```shell
npm run dev
```

To lint all CSS use:

```shell
npm run lint
```

### Set up SSL Certificate

For local development we have decided to require an SSL certificate so that we run our development server with SSL so we are closer to a production system where we intend to use SSL also. We specify the flask cli flags `FLASK_RUN_CERT=cert.pem` and `FLASK_RUN_KEY=key.pem` in the `.flaskenv`, which expect a `cert.pem` and corresponding `key.pem` file in the root of the repo.

You will need to create the cert-key pair with:

  ```shell
  poetry run openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
  ```

  and fill out the its prompts with information that you want (it does not matter as it is only being used for a development server).

  **Note:** this command creates a cert-key pair valid for 365 days, but you can amend this as you wish.

When you access the application in a new browser for the first time with one of these keys you will have to tell it you trust the certificate, but then you should not be asked again.

**Note:** [flask-talisman](###HTTP-security-headers) should redirect http requests to https but whenever running the flask development server with a certificate, this doesn't seem to do the redirection. We plan to investigate but for now we will have to deal without this redirection in local dev.

### Set Flask Configuration Variables

Set the Flask Configuration Variables either with either:

- Environment Variables:
  1. Set all desired environment variables for all of the variables specified in `.env.env_var.template`. For convenience you can do this by running the following in the root of the repo:

    ```shell
    cp .env.env_var.template .env
    ```

    and filling out the `.env` file as desired.

- AWS SSM Parameter Store values:
  1. Set up your AWS credentials or log into an AWS account with the AWS CLI environment so that the desired AWS IAM user or role is set up.
  1. Make sure all of the properties (not the hardcoded values) in the `BaseConfig` class are set in the AWS SSM Parameter Store for this account.
  1. Set all desired environment variables for all of the variables specified in `env.aws_parameter_store.template`. For convenience you can do this by running the following in the root of the repo:

    ```shell
    cp .env.aws_parameter_store.template .env
    ```

    and filling out the `.env` file as desired.

**Note:** `AWSParameterStoreConfig` depends on a `boto3` session which, when developing locally, can be set to use a specific AWS Profile by setting the environment variable `DEFAULT_AWS_PROFILE`.

### Run app

Ensure you set the above environment variables in the `.env` file as appropriate before running the Flask application with:

```shell
flask run
```

You should now have the app running on <https://localhost:5000/>

**Note:** Unless you have changed the `FLASK_APP` value in the `.flaskenv` file to point to another application entrypoint other than `main_app`, you must specify the `CONFIG_SOURCE` environment variable (as populated by the env file templates), to be either `AWS_PARAMETER_STORE` or `ENVIRONMENT_VARIABLES` otherwise `flask run` will raise an error.

## Flask App Configuration Details

Our application uses configuration values defined using [Flask Config classes](https://flask.palletsprojects.com/en/2.3.x/config/#development-production) to set up the application's settings and connect it to various services. The pattern we are using consists of a base config class, `BaseConfig`, which is where we specify any hardcoded values, and all other configurable values are defined as a property, for example:

```python
    @property
    def EXAMPLE_VARIABLE(self):
        return self._get_config_value("EXAMPLE_VARIABLE")
```

where `_get_config_value` is treated as an abstract method which is implemented in the child config classes that extend `BaseConfig`.

Hardcoded values:

- `RATELIMIT_HEADERS_ENABLED`: Rate-limiting headers configuration. Is `True`.
- `SESSION_COOKIE_HTTPONLY`: Configure session cookies to be HTTP-only. Is `True`.
- `SESSION_COOKIE_SECURE`: Configure session cookies to be secure. Is `True`.
- `CONTACT_EMAIL`: Email address for contact information.
- `CONTACT_PHONE`: Phone number for contact information.
- `DEPARTMENT_NAME`: The name of the department.
- `DEPARTMENT_URL`: The URL of the department's website.
- `SERVICE_NAME`: The name of the service.
- `SERVICE_PHASE`: The phase of the service.
- `SERVICE_URL`: The URL of the service.

Properties configurable at runtime:

- `AWS_REGION`: The AWS region used for AWS services.
- `DB_PORT`: The port of the database to connect to.
- `DB_HOST`: The host of the database to connect to.
- `DB_USER`: The username of the database to connect to.
- `DB_PASSWORD`: The password of the database to connect to. Note: When using `CONFIG_SOURCE=AWS_PARAMETER_STORE` then this does not need to be set in Parameter store and instead this is generated using an AWS API in the config.
- `DB_NAME`: The name of the database to connect to.
- `KEYCLOAK_BASE_URI`: The base URI of the Keycloak authentication service.
- `KEYCLOAK_CLIENT_ID`: The client ID used for Keycloak authentication.
- `KEYCLOAK_REALM_NAME`: The name of the Keycloak realm.
- `KEYCLOAK_CLIENT_SECRET`: The client secret used for Keycloak authentication.
- `KEYCLOAK_AYR_USER_GROUP`: The Keycloak user group used to check user access.
- `RATELIMIT_STORAGE_URI`: The URI for the Redis storage used for rate limiting.
- `SECRET_KEY`: Secret key used for Flask session and security.

Calculated values:

- `SQLALCHEMY_DATABASE_URI`: The PostgreSQL database URI with format `postgresql+psycopg2://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>`.

We have two usable configs which extend `BaseConfig` for running the application:

- `EnvConfig` which implements `_get_config_value` so it reads from environment variables.
- `AWSParameterStoreConfig` which implements `_get_config_value` so it reads from AWS SSM Parameter Store values.

When configuring `flask run` run the app created by `main_app.py`, as we do with the line `export FLASK_APP=main_app` in the `.flaskenv`, we can either use `EnvConfig` or `AWSParameterStoreConfig` by setting `CONFIG_SOURCE` as either `ENVIRONMENT_VARIABLES` or `AWS_PARAMETER_STORE` respectively.

We also have a `TestingConfig` that extends `BaseConfig` which is only used for Flask tests as detailed below. Its implementation of  `_get_config_value` returns an empty string for all the configurable properties just so we don't need to worry about setting values in tests we don't care about them in. We may revisit this, as the fact that config vars are unnecessary in some tests that access them seems like a code smell that could be worth addressing; specifying them in any test that needs them and refactoring the code if we still find asserting anything about them unnecessary could be a better approach long term.
As well as the confgiurable values discussed above, we also hardcode the following on the `TestingConfig`:

- `TESTING` to `True` to disable error catching (further info [here](https://flask.palletsprojects.com/en/3.0.x/config/#TESTING)), and changes certain extension's logic as well as own on (e.g. disables forcing of https) to facilitate easier testing.
- `SECRET_KEY` to `"TEST_SECRET_KEY"` so that Flask sessions work in the tests.
- `WTF_CSRF_ENABLED` to `False` so that we do not need to worry about CSRF protection in our tests.

### The .flaskenv file

In addition to the `.env` file discussed above, which can be created from template files, we have a `.flaskenv` file with Flask specific configuration values which is committed to the repo and we don't expect to change these.

### Environment loading

Both the `.env` and `.flask_env` are loaded automatically when we run the flask application as outlined in the following section, thanks to the use of `python-dotenv`. More information on Flask environment variable hierarchies can be found [here](https://flask.palletsprojects.com/en/2.3.x/cli/#environment-variables-from-dotenv).

## Deployment

Here we detail a way to run the server-side rendered Flask webapp via a "serverless" AWS Lambda-API Gateway setup.

Specific details on how this architecture works can be found in our service diagram that can be shared upon request to a maintainer of this repo.

To implement this we are currently using [Zappa](https://github.com/zappa/Zappa), as defined in our poetry depedencies. Note this is required to be part of the main dependencies group since it is not just a CLI tool but in fact has it's own code which is run in the Lambda once the application code is packaged and deployed to AWS.

### Zappa Configuration

Zappa is configurable, and can be configured differently for different deployment stages. In particular, each deployment stage's configuration is separated  by the top level environment key in the `zappa_settings.json` file.

In this repo we provide a `zappa_settings.json.template` which provides all the configuration variables except for a few values which we need to set as environment variables first so that we can use them to create our custom config from the template.

This config makes a few assumptions about each AWS account being deployed to:

- The SSM Parameter Store has been populated with all needed configuration values as detailed in [the flask configuration section above](#flask-app-configuration-details).
- An RDS database and proxy exists.
- A VPC exists which contains a private subnet connected to the internet via a NAT Gateway and a security group exists with outbound rules to the the RDS database proxy.
- A valid certificate exists in the AWS account for the domain we want to use for the deployment.

You could decide to set up this infrastructure through terraform or cloudformation to make things easier to reproduce.

Set these environment variables:

- `ZAPPA_SANDBOX_DEPLOYMENT_PROFILE_NAME` specifies the profile name we want to use to update the sandbox deployment stage with.
- `ZAPPA_SANDBOX_LAMBDA_VPC_PRIVATE_SUBNET_ID` specifies the VPC private subnet we want our lambda to use in the sandbox deployment
- `ZAPPA_SANDBOX_LAMBDA_VPC_SECURITY_GROUP_ID` specifies the VPC security group we want to our lambda to use in the sandbox deployment
- `ZAPPA_SANDBOX_CERTIFICATE_ARN` specifies the AWS  certificate we want to certify our domain with
- `ZAPPA_SANDBOX_WEBAPP_DOMAIN` specifies the domain we want to deploy the webapp to

Once all of these environment variables are set, create a `zappa_settings.json` from them by running:

  ```shell
  envsubst < zappa_settings.json.template > zappa_settings.json
  ```

Note 1: the name of each deployment stage we want to deploy to is defined as a top-level key in the `zappa_settings.json` e.g. `sandbox`.

Note 2: As part of our template, we refer to `lambda_policy.json` which defines the IAM Policy for the Lambda execution role so that it can access certain AWS resources such as SSM Parameter Store.

Note 3: As part of our template, we refer to `apigateway_policy.json` which defines the IAM Policy for the APIGateway resource created, but we only define a template file, `apigateway_policy.json.template`, so that we do not commit any IPs to source control. Details on filling out the whitelist from an environment variable is detailed below.

### Zappa deployments

Zappa packages the active virtual environment, in our case our poetry environment, into a zipfile package which will be pushed to run on AWS Lambda.
AWS Lambda has a size limit of 250MB for the unzipped code so we want to make sure we make the package as lean as possible.

Before running a zappa deployment, make sure you clean out the environment so that it is as lean as possible:

- remove all files unnecessary for running the application. We recommend stashing any files that aren't committed to the repo.
- remove all dependencies unneeded for running the application, you can do that with: `poetry install --without dev --sync`

#### Initial Deployments

Fill out the IP Whitelist in the APIGateway Policy from the environment variable `APIGATEWAY_WHITELISTED_IPS` to allow these IP addresses access to the webapp via the APIGateway with:

```shell
envsubst < apigateway_policy.json.template > apigateway_policy.json
```

Note: make sure `APIGATEWAY_WHITELISTED_IPS` is exported as an environment variable in your current terminal like: `export APIGATEWAY_WHITELISTED_IPS='["IP_1/32","IP_2/32","IP_3/32"]'`

Once your settings are configured, you can package and deploy your application to a deployment stage with a single command:

```shell
zappa deploy <DEPLOYMENT_STAGE>
```

We then need to run

```shell
zappa certify
```

to certify the domains used in each deployment utilising the certificate specified in each section.

Note: Once the application has been deployed once to a particular stage, then it can't be deployed again. You will need to run `zappa undeploy <DEPLOYMENT_STAGE` first. However, more often than not, you will only need to update the deployment, as detailed below.

#### Only Update Flask Code

If your application has already been deployed and you only need to upload new Python code, but not touch the underlying routes, you can simply run:

```shell
zappa update <DEPLOYMENT_STAGE>
```

This creates a new archive, uploads it to S3 and updates the Lambda function to use the new code, but doesn't touch the API Gateway routes.

#### Debugging a deployment

You can watch the logs of a deployment by calling the tail management command:

```shell
zappa tail <DEPLOYMENT_STAGE>
```

This is especially useful if a deployment fails.

### CI/CD

We do not currently update any deployment automatically in our CI/CD pipeline, but we will soon.

## Metadata Store Postgres Database

The webapp is set up to read data from an externally defined postgres database referred to as the Metadata Store.

We currently use the python package, Flask-SQLAlchemy to leverage some benefits of the ORM (Object Relationship Mapping) it provides, making our queries using the python classes we create as opposed to explicit SQL queries.

The database connection is configured with the `SQLALCHEMY_DATABASE_URI` variable built up in the Flask Config.

### Database Infrastructure and Connection

The database is assumed to be a PostgreSQL database.

This could be spun up by PostgreSQL or from Amazon RDS, for example.

When choosing the configuration choice `AWS_PARAMETER_STORE`, we assume the database is an RDS database with an RDS proxy sitting in front, in the same AWS account as the SSM Parameter Store and lambda and resides in a VPC which the lambda is in so that the webapp hosted in the lambda can communicate with it securely, as mentioned in the [Zappa configuration section](#zappa-configuration).

### Database Tables, Schema and Data

We do not define the database tables ourselves, nor write any information to the database, both of which are assumed to be handled externally. To leverage the use of the ORM we reflect the tables from the existing database with the following line in our Flask app setup.

`db.Model.metadata.reflect(bind=db.engine, schema="public")`

More info on relecting database tables can be found [here](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/models/#reflecting-tables).

Further, to this, we do define models and columns from the corresponding tables we do use in our queries we use so that when developing we will know what attributes are available but this has to be manually kept in sync with the externally determined schema through discussion with the maintainers of the Metadata Store database.

## Testing

### Unit and Integration tests

For running flask app tests, we have the `client` fixture which uses the `app` fixture which utilises `TestingConfig` as discussed above.

To run the unit and integration tests you can run:

```shell
python -m pytest --cov=app --cov-report=term-missing --cov-branch -vvv
```

This also will generate a test coverage report.

### End To End Tests

We have a separate End To End suite of [Playwright](https://playwright.dev/python/docs/intro) tests in the `e2e_tests/` directory. These are also written in python and use the `pytest-playwright` `PyPi` package to run the tests as specified in the poetry dependencies.

In addition to installing the package, before you run the tests for the first time on your machine, you will need to run `playwright install` to install the required browsers for the end to end tests.

Before running our Playwright tests,

- `AYR_TEST_USERNAME`
- `AYR_TEST_PASSWORD`

with appropriate test user credentials for the instance you want to test

Note: a `.env.e2e_tests.template` file has been provided, which you can then `cp .env.e2e_tests.template .env.e2e_tests`, then fill, and then source `source .env.e2e_tests`

You can then run all of our Playwright tests against an instance, localhost for example, by running:

```shell
pytest e2e_tests/ --base-url=https://localhost:5000
```

You can swap out the base-url for another if you want to run the tests against another instance of the application.

To enable this flexibility we suggest any Playwright tests added to the repo use relative paths when referring to urls of the application itself.

In addition, we recommend that any tests that have dependencies on data, do not make assumptions about any particular database or instance involved, and instead do the test data set up and teardown as part of the test suite.

### Useful playwright pytest run modes

#### slowmo

- Since our webapp has rate limiting, you may need to run playwright with --slowmo flag, e.g.
`pytest e2e_tests/ --base-url=https://localhost:5000 --slowmo 200`

#### headed

- To view the browser when the tests are running, you can add the `--headed` flag, e.g.

`pytest e2e_tests/ --base-url=https://localhost:5000 --headed`

#### PWDEBUG

- To utilise the playwright debugger, you can set the `PWDEBUG=1` environment variable, e.g.

`PWDEBUG=1 poetry run pytest e2e_tests/test_poc_search.py --base-url=http://localhost:5000 --headed`

1. individual tests in file with multiple tests (use -k):
poetry run pytest e2e_tests/test_record_metadata.py -k test_page_title_and_header --base-url=http://localhost:5000 --headed --slowmo 2000

### Generate playwright tests using GUI

Run `poetry run playwright codegen https://localhost:5000` to spin up a browser instance which you can interact with, where each interaction will be captured as a pytest playwright line, which builds out a test skeleton file for you to add assertions to.

### When to add an E2E Tests?

End to end tests have prod and cons, such as the following:

Pros:

- Testing Real User Flows
- Complex User Scenarios (such as sign in flows)

Cons:

- Execution Time
- Harder to debug errors

Therefore we should try to add them sparingly on critical workflows.

### E2E Tests (Progressive Enhancement Support)

E2E Tests by default run without JavaScript & CSS.

To enable JavaScript to run during E2E Tests the flag `java_script_enabled` should be set to True within conftest.py.

To enable a test to run with CSS ensure each test is prefixed with with the term `test_css_test_name`.

e.g.:

`
def test_css_has_title(page: Page):
`

## Logging

### Configuration

The application logger configuration is detailed in `setup_logging` in `app/logger_config.py`.

This config includes:

- a formatter specifying request-specific information such as the remote address and URL when a request context is available
- setting the logging level to `INFO`.

`setup_logging` is called during the initialization of the Flask app.

### Usage

We can utilise the Flask logger by accessing Flask's `app.logger`. Since we define our routes with blueprints rather than the app directly, we can call access app through

```python
from flask import current_app
```

for example:

```python
current_app.logger.info('Some info message')
current_app.logger.debug('Some debug message')
current_app.logger.warning('Some warning message')
current_app.logger.error('Some error message')
```

### Output

The logs from the webapp, when used as above are output as a stream to stdout in the following format:

```sh
[2023-12-15 15:40:14,119] 127.0.0.1 requested https://localhost:5000/logger_test?log_level=error
ERROR in routes: Some error
```

### Extensions and package logs

Some of the Flask extensions used,as detailed in the Features section below, may produce their own logs and may have their own configuration and format different to the above.

### Testing logs

With pytest we can assert the logs we expect to be written by utilising pytest's inbuilt `caplog` fixture.

## Features

Please refer to the specific packages documentation for more details. Details can be found in the [pytest logging documentation](https://docs.pytest.org/en/7.1.x/how-to/logging.html#how-to-manage-logging).

### Asset management

Custom CSS and JavaScript files are merged and compressed using [Flask Assets](https://flask-assets.readthedocs.io/en/latest/) and [Webassets](https://webassets.readthedocs.io/en/latest/). This takes all `*.css` files in `app/static/src/css` and all `*.js` files in `app/static/src/js` and outputs a single compressed file to both `app/static/dist/css` and `app/static/dist/js` respectively.

CSS is [minified](https://en.wikipedia.org/wiki/Minification_(programming)) using [CSSMin](https://github.com/zacharyvoase/cssmin) and JavaScript is minified using [JSMin](https://github.com/tikitu/jsmin/). This removes all whitespace characters, comments and line breaks to reduce the size of the source code, making its transmission over a network more efficient.

### Cache busting

Merged and compressed assets are browser cache busted on update by modifying their URL with their MD5 hash using [Flask Assets](https://flask-assets.readthedocs.io/en/latest/) and [Webassets](https://webassets.readthedocs.io/en/latest/). The MD5 hash is appended to the file name, for example `custom-d41d8cd9.css` instead of a query string, to support certain older browsers and proxies that ignore the querystring in their caching behaviour.

### Forms generation and validation

Uses [Flask WTF](https://flask-wtf.readthedocs.io/en/stable/) and [WTForms](https://wtforms.readthedocs.io) to define and validate forms. Forms are rendered in your template using regular Jinja syntax.

### Form error handling

If a submitted form has any validation errors, an [error summary component](https://design-system.service.gov.uk/components/error-summary/) is shown at the top of the page, along with individual field [error messages](https://design-system.service.gov.uk/components/error-message/). This follows the GOV.UK Design System [validation pattern](https://design-system.service.gov.uk/patterns/validation/) and is built into the base page template.

### Flash messages

Messages created with Flask's `flash` function will be rendered using the GOV.UK Design System [notification banner component](https://design-system.service.gov.uk/components/notification-banner/). By default the blue "important" banner style will be used, unless a category of "success" is passed to use the green version.

### CSRF protection

Uses [Flask WTF](https://flask-wtf.readthedocs.io/en/stable/) to enable [Cross Site Request Forgery](https://en.wikipedia.org/wiki/Cross-site_request_forgery) protection per form and for the whole app.

CSRF errors are handled by creating a [flash message](#flash-messages) notification banner to inform the user that the form they submitted has expired.

### HTTP security headers

Uses [Flask Talisman](https://github.com/GoogleCloudPlatform/flask-talisman) to set HTTP headers that can help protect against a few common web application security issues.

- Forces all connections to `https`, unless running with debug enabled or in testing. Note: This seems to not be working when running the local development with a SSL certificate as discussed [above](###set-up-ssl-certificate)
- Enables [HTTP Strict Transport Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security).
- Sets Flask's session cookie to `secure`, so it will never be set if your application is somehow accessed via a non-secure connection.
- Sets Flask's session cookie to `httponly`, preventing JavaScript from being able to access its content.
- Sets [X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options) to `SAMEORIGIN` to avoid [clickjacking](https://en.wikipedia.org/wiki/Clickjacking).
- Sets [X-XSS-Protection](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection) to enable a cross site scripting filter for IE and Safari (note Chrome has removed this and Firefox never supported it).
- Sets [X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options) to prevent content type sniffing.
- Sets a strict [Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) of `strict-origin-when-cross-origin` that governs which referrer information should be included with requests made.

### Content Security Policy

A strict default [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) (CSP) is set using [Flask Talisman](https://github.com/GoogleCloudPlatform/flask-talisman) to mitigate [Cross Site Scripting](https://developer.mozilla.org/en-US/docs/Web/Security/Types_of_attacks#cross-site_scripting_xss) (XSS) and packet sniffing attacks. This prevents loading any resources that are not in the same domain as the application.

### Response compression

Uses [Flask Compress](https://github.com/colour-science/flask-compress) to compress response data. This inspects the `Accept-Encoding` request header, compresses using either gzip, deflate or brotli algorithms and sets the `Content-Encoding` response header. HTML, CSS, XML, JSON and JavaScript MIME types will all be compressed.

### Rate limiting

Uses [Flask Limiter](https://flask-limiter.readthedocs.io/en/stable/) to set request rate limits on routes. The default rate limit is 2 requests per second _and_ 60 requests per minute (whichever is hit first) based on the client's remote IP address. Every time a request exceeds the rate limit, the view function will not get called and instead a [HTTP 429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) status will be returned.

Rate limit storage can be backed by [Redis](https://redis.io/) using the `RATELIMIT_STORAGE_URL` config value in `config.py`, or fall back to in-memory if not present. Rate limit information will also be added to various [response headers](https://flask-limiter.readthedocs.io/en/stable/#rate-limiting-headers).

## Support

This software is provided _"as-is"_ without warranty. Support is provided on a _"best endeavours"_ basis by the maintainers and open source community.

Please see the [contribution guidelines](CONTRIBUTING.md) for how to raise a bug report or feature request.
