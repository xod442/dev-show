# dev-show
development for new sys show all

This application uses the mongo db installed by StackStorm.. Since the DB is secured
you will need to log into the StackStorm mongo DB as a StackStorm admin and create a separate DB

# sysshow mongengine to work with StackStorm mongo DB

log in with admin first
-------------------------------------------------------------------------------------
mongo -u admin -p UkIbDILcNbMhkh3KtN6xfr9h admin  (passwd in /etc/st2/st2.config)

# Then create a new user
db.createUser({user: "appUser",pwd: "passwordForAppUser",roles: [ { role: "readWrite", db: "app_db" } ]})

# Add creds to the Flask application.py file
```
app.config['MONGODB_SETTINGS'] = {
        'db': 'app_db',
        'host': 'localhost',
        'port': 27017,
        'username': 'appUser',
        'password': 'passwordForAppUser',
        'authentication_source': 'admin'
        }
```

Now Flask app can access the st2 mongo database installation

# sysshow uses multiple mongo collections.
Here is a quick tutorial for using the mongo client and adding records to the mongo db

# Create number collection and add a record to it.
```
mongo -u appUser -p passwordForAppUser admin
> use app_db
> db.createCollection('number')
> db.number.insertOne({num:1})
> db.number.find()
{ "_id" : ObjectId("5cc84e276e9abf31a65a5f1f"), "num" : 1 }
```

#To issue stackstorm commands from the command line you have to log into StackStorm
```
st2 login st2admin
```
