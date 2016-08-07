# Movie API app

### Project setup instructions:
1. Create setting.ini file:
- copy settings-template.ini to settings.ini
```
cp settings-template.ini settings.ini
```
- update default values with yout own configs (host, port, db name, username, password)

2. Create and run migrations:
- create your database
- run migrations:
```
python manage.py makemigrations metadata_api
python manage.py sqlmigrate metadata_api 0001
python manage.py migrate
```
3. Load data into temprorary table:
- you can either use this helper ur: /api/load-data
- or you can load data by running metadata_api.views.loadData method

4. Migrate data into real tables now:
- you can either use this helper ur: /api/migrate-records
- or you can load data by running metadata_api.views.migrateRecords method

------------
### API endpoints:
- /api/titles
    - gets all movie titles
- /api/titles/latest
    - gets all movie titles organized by year, most recent ones first
- /api/titles/<movie-title-id>/
    - gets details about one specific movie, given movie id

#### Helper api:
- /api/load-data
    - load data from text file into Temp table
- /api/migrate-records
    - migrates records from Temp table into movie/genre/moviegenre tables

------------