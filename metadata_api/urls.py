from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    url(r'^titles$', views.getAllTitles, name='get-all-titles'),
    url(r'^titles/latest$', views.getLatestTitles, name='get-latest-titles'),
    url(r'^titles/(?P<primaryKey>[0-9]+)/$', views.getTitleDetails, name='get-title-detail'),

    # url endpoint for loading initial data into Temp table
    url(r'^load-data$', views.loadData, name='load-data'),
    
    # url endpoint for migrating data between tables
    url(r'^migrate-records$', views.migrateRecords, name='migrate-records'),

]