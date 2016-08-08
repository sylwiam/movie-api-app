# Movie API app
This app is built on top of Django Python framework. It loads movie metadata from a text file into a database. It also provides a lightweight api to quickly get filtered movie information. See below for details.

### Project setup instructions:
##### Create settings.ini file:
- copy settings-template.ini to settings.ini
```
cp settings-template.ini settings.ini
```
- update default values with your own configs (host, port, db name, username, password)
- settings.py will read private attributes from settings.ini (which is not part of repository)

##### Create and run migrations:
- create your database
- run migrations:
```
python manage.py makemigrations metadata_api
python manage.py sqlmigrate metadata_api 0001
python manage.py migrate
```
##### Load data into temporary table:
- you can either use this helper url: /api/load-data
- or you can load data by executing metadata_api.views.loadData method

##### Migrate data into real tables now:
- you can either use this helper ur: /api/migrate-records
- or you can load data by executing metadata_api.views.migrateRecords method

------------
### API endpoints:
- /api/titles
    - gets all movie titles
- /api/titles/latest
    - gets newwest 50 movie titles organized by year, most recent ones first
- /api/titles/movie-title-id-here/
    - gets details about one specific movie, given movie id (primary key)
- /api/titles/year/year-here/
    - gets all movies released in a given year
- /api/titles/genre/genre-name-here/
    - gets all movies that belong to a given genre

#### Helper api:
- /api/load-data
    - load data from text file into Temp table
- /api/migrate-records
    - migrates records from Temp table into movie/genre/moviegenre tables

------------