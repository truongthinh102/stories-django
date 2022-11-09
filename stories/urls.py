
from django.urls import path
from stories.views import *

app_name = 'stories'
urlpatterns = [
    path('', index, name ='index'),
    path('index-2/', index_2, name ='index_2'),
    path('category/<int:pk>/', category, name = 'category'),
    path('story/<int:pk>/', story, name = 'story'),
    path('contact/', contact, name = 'contact'),
    path('contact-with-form/', contact_with_form, name = 'contact'),
    path('search/', search, name = 'search'),
    path('rss/', read_rss, name = 'rss'),

]