from django.urls import path, re_path

from apps.home import views

urlpatterns = [
    path('', views.predict, name='home'),
    path('predict-price/', views.predict_price, name='predict-price'),
    path('average_price', views.average_price, name='average_price'),
    path('interactive_map', views.interactive_map, name='interactive_map'),
    path('data_analysis', views.data_analysis, name='data_analysis'),
    path('get-diagram-values/', views.get_diagram_values, name='get-diagram-values'),
    path('settings', views.settings, name='settings'),
    path('stored_data', views.stored_data, name='stored_data'),
    path('get-stored-data/', views.get_stored_data, name='get-stored-data'),
    path('update-property/', views.update_property, name='update-property'),
    path('scraping-service-status/', views.scraping_service_status, name='scraping-service-status'),
    path('scraping-service-interval/', views.scraping_service_interval, name='scraping-service-interval'),
    path('scraping-service-location/', views.scraping_service_location, name='scraping-service-location'),
    path('execute-scraping-service-action/', views.execute_scraping_service_action,
         name='scraping-service-execute-action'),
    path('scraping-service-website-support/', views.scraping_service_website_support,
         name='scraping-service-website-support'),
    path('scraping-service-scrape-status/', views.scraping_service_scrape_status,
         name='scraping-service-scrape-status'),
    path('realitysk-scraping-service-scrape-today/', views.realitysk_scraping_service_scrape_today,
         name='realitysk-scraping-service-scrape-today'),
    path('realitysk-scraping-service-scrape-all/', views.realitysk_scraping_service_scrape_all,
         name='realitysk-scraping-service-scrape-all'),

    re_path(r'^.*\.*', views.pages, name='pages'),
]
