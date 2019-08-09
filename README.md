# products_aggregator

## Table of contents


* [Getting Started](#Getting-Started)
  * [Required packages](#Required-packages)
  * [Install project](#Install-project)
* [Documentation](#Documentation)
  * [Run server](#Run-server)
  * [Run unit tests](#Run-unit-tests)

### Getting Started

#### Required packages

Products_aggregator use MariaDB. Please, install next packages:
`python-pip python-dev virtualenv mariadb-server libmariadbclient-dev 
libssl-dev`

Also we recommend use python 3.6

#### Install project

1. Complete security script by running:
`sudo mysql_secure_installation`
2. After create database for project and user and give him privileges
for database. You can use this [manual](https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04)
if you encountered problems at this stage
3. Clone repository with commands:
`git clone https://github.com/HighHopesInt/products_aggregator.git`
4. Use command `cd products_aggregator` 
5. Create virtualenv using command `virtualenv -p python3 <name env>`
6. Install packages from PyPI using command `pip install -r requirements.txt`
7. Get `.env` config and put it in `products_aggregator`

Congratulations! We install products_aggregator.

### Documentation 

#### Run server

Use command `python manage.py runserver` in your virtualenv.
After open browser and input localhost:8000 or 127.0.0.1:8000

#### Run unit test

Use command `python manage.py test` in your virtualenv that run unit tests.
We also can add name of kind application that run tests for it. **Attention!** You may have to give the user rights in MariaDB to the default test database for tests. More details in [documentation](https://docs.djangoproject.com/en/2.2/topics/testing/overview/#the-test-database)

Please, if you search error tell us in issue.