## Store Victor

This is me trying to see how we can use a human instead of a bot in the chat 

Major Requirement :
1. Python 3
2. SQlite3

Install packages and dependencies by invoking the command below:
```
    pip/pip3 install -r requirements.txt
```

Apply the migrations to your database by invoking the migrate command. There's no need to make the migrations again since they've already been made.
```bash
python manage.py migrate
```

Create a user account, preferrably a super user:
```bash
python manage.py createsuperuser
```

You should be good to go with:
```bash
python manage.py runserver
```

Some fixture will be added so to easily populate the db for test purposes

###
Postman collections have been shared as `Store.postman_collection.json`


