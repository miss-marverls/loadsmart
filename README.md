# Loadsmart
Project for the Loadsmart Women Acceleration Program 2019 - Miss Marvels

## Running the Project Locally
Clone the repository:

    ~/$ git clone https://github.com/miss-marverls/loadsmart.git

Create and activate a virtual environment, then install required packages:

    ~/$ cd loadsmart
    ~/loadsmart$ virtualenv env -p python3
    ~/loadsmart$ source env/bin/activate
    (env)~/loadsmart$ pip install -r requirements.txt

Create the database:

    (env)~/loadsmart$ python manage.py migrate

Run the development server:

    (env)~/loadsmart$ python manage.py runserver

The project is available at http://127.0.0.1:8000/.

## Tests
Run unit tests with coverage inside of project folder:

    (env)~/loadsmart$ python manage.py test

## Apps documentation
Generate documentation:

    (env)~/loadsmart$ cd docs/
    (env)~/loadsmart/docs$ make html
    
Documentation is available in loadsmart/docs/_build/html/index.html   

## API



