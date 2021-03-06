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

**Products_aggregator** use MariaDB. Please, install next packages:
`python-pip python-dev virtualenv mariadb-server libmariadbclient-dev 
libssl-dev`

Also we recommend to use python 3.6.

#### Install project

**Attention!**

The following steps were performed on Ubuntu 18.04. You may encounter a number of errors when trying to do this on a machine with a different operating system.


1. Run security script:
`sudo mysql_secure_installation`
2. Create database, user and grant privileges
for database to user. You can use this [manual](https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04)
if you encounter problems at this stage;
3. Clone repository:
`git clone https://github.com/HighHopesInt/products_aggregator.git`
4. Run `cd products_aggregator` 
5. Create virtualenv using command `virtualenv -p python3 <name env>`
6. Install dependencies: `pip install -r requirements.txt`
7. Create `.env` file and put it in `products_aggregator` folder.

Congratulations! We have installed **products_aggregator**.

### Documentation 

#### Run server

Run `python manage.py runserver` in your virtualenv.
Then open browser and visit `localhost:8000` or `127.0.0.1:8000`

#### Run unit test

Run `python manage.py test` in your virtualenv.
You can specify the app for running tests this way: `python manage.py test <app_name>`. 
**Attention!** You may have to grant privileges to the database user for the default test database. 
You can use this SQL code for that: `GRANT ALL PRIVILEGES ON test_myproject.* TO myprojectuser@localhost;`,
where `myproject` name of your database and `myprojectuser` name of user in database.

See also: [Django docs](https://docs.djangoproject.com/en/2.2/topics/testing/overview/#the-test-database)

Please, if you find any error, your issues are welcome.