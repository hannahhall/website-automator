# Automator API
Server side for [Class Website Automator](https://github.com/hannahhall/automator-client). Automates creating the class website for NSS students.

## Getting Started
1. Check the python version, `python3 --version`. If it is not 3.9.*, run the install script for your os:
* Mac: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nashville-software-school/bangazon-llc/cohort-56/book-1-kennels/chapters/scripts/mac-installs.sh)"
`
* WSL or Ubuntu: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/nashville-software-school/bangazon-llc/cohort-56/book-1-kennels/chapters/scripts/wsl-ubuntu-installs.sh)"`

2. Run the set up commands. This will set up the environment, database, and initial data.

    ```sh
    pipenv shell
    pipenv install
    ./manage.py migrate
    ./manage.py loaddata programs cohorts themes
    ```
 3. When opening vscode for the first time, there are 2 extension recommendations. Accept the extension installs when the pop up appears. These will make debugging and running tests easier.

## Commands

* Run the server: `./manage.py runserver`
* Run tests: `./manage.py test`
* Create a super user (for use with django admin): `./manage.py createsuperuser`

