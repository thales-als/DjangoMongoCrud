from django.urls import re_path 
from cars import views 
 
urlpatterns = [ 
    re_path (r'^api/cars$', views.car_list),
    re_path (r'^api/cars/(?P<pk>[0-9]+)$', views.car_detail),
    re_path (r'^api/cars/published$', views.car_list_published)
]