# Restaurant Menu
Project for a restaurant menu app, where users can add, edit and remove restaurants and menu items to their restaurants. Users can sign in using Google and Facebook via Oauth2, and can only edit and delete their own data.

## Table of contents
* [Requirements](#requirements)
* [Quick start](#quick-start)
* [Creator](#creator)

## Requirements
* Python 2.7
* Git
* Vagrant
* Install libraries in the `requirements.txt` file using pip.

## Quick start
* (Optional) Clone the repo: `git clone https://github.com/iraquitan/vagrant-trusty64-python-web.git` if you don't already have a vagrant VM configured with Flask.
* (Optional) Change directory to the newly cloned repo.
* Clone this repo `git clone https://github.com/iraquitan/udacity-fsnd-restaurant-menu restaurant-menu` inside your vagrant VM shared folder.
* Change to the `/restaurant-menu` directory.
* Create a local config file in `instance/config.py`.
* And fill with local config like database location and Oauth credentials as in the example below:
```python
DEBUG = True
SECRET_KEY = 'your_super_secret_key'
SQLALCHEMY_DATABASE_URI = "sqlite:///../restaurant-menu/restaurant-menu.db"
OAUTH_CREDENTIALS = {
    'google': {
        'id': "Google__client__id.apps.googleusercontent.com",
        'secret': "Google_client_secret_"
    },
    'facebook': {
        'id': "Facebook_client_id",
        'secret': "Facebook_client_secret"
    }
}
```
* Start vagrant virtual machine with `vagrant up`.
* Run the following code on terminal: `vagrant ssh` to connect to the virtual machine using ssh.
* Run the following code on terminal: `cd /vagrant/restaurant-menu/` to change directory to this project.
* Run the following code on terminal to populate DB: `python other/lotsofmenus-withusers.py`.
* Run the following code on terminal to run the server locally: `python runserver.py`.

## Creator
**Iraquitan Cordeiro Filho**

* <https://twitter.com/iraquitan_filho>
* <https://github.com/iraquitan>
