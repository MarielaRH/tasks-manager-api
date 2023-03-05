# tasks-manager-api
This is a REST API made with django-rest-framework, this api allows to manage CRUD of projects, users, categories and tasks.

## Technologies used
* [Django](https://www.djangoproject.com/): The web framework for perfectionists with deadlines (Django builds better web apps with less code).
* [DRF](www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs.
* [MySQL](https://www.mysql.com/): Relational database management system.


## Installation
* If you wish to run your own build, first ensure you have python globally installed in your computer. If not, you can get python [here](https://www.python.org").

* Then, Git clone this repo to your PC
    ```bash
        $ git clone https://github.com/MarielaRH/tasks-manager-api.git
    ```

* #### Dependencies
    1. Cd into your the cloned repo as such:
        ```bash
            $ cd tasks-manager-api
        ```
    2. Create and fire up your virtual environment:
        ```bash
            $ python3 -m venv env
            $ source env/bin/activate
        ```
    3. Install the dependencies needed to run the app:
        ```bash
            $ pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```bash
            $ python manage.py makemigrations
            $ python manage.py migrate
        ```

* #### Run It
    Fire up the server using this one simple command:
    ```bash
        $ python manage.py runserver
    ```
    You can now access the file api service on your browser by using
    ```
        http://localhost:8000/
    ```
