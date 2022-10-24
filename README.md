# Social network


### Description
This project is like a social network.
There is a main page, an author's page with his posts, as well as a page of the post with comments to it.
Posts can be left in thematic groups. It is possible to subscribe to an author.
The full functionality of registration and password recovery via mail has been implemented.


### Technology stack
- Python 3.9
- Django 2.2.16
- Pillow 8.3.1
- sorl-thumbnail 12.7.0


### Project run on local server
- Install and activate the virtual environment:
```py -m venv venv```
```. venv/Scripts/activate```

- Install dependencies from requirements.txt:
```pip install -r requirements.txt```

- Perform all migrations:
```py manage.py makemigrations```
```py manage.py migrate```

- Run the command:
```py manage.py runserver```


#### Author
Karapetyan Zorik

Russian Federation, St. Petersburg, Kupchino.