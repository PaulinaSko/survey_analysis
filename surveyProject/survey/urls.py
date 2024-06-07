from django.urls import path
from . import views

urlpatterns = [
    path('results/', views.survey_results, name='age_results'),
    path('main_branch/', views.main_b_results, name='main_b_results'),
    path('level_of_edu/', views.level_of_education, name='level_of_edu'),
    path('about/', views.survey_description, name='about'),
    path('tech/', views.used_tech, name='tech'),
    path('summary/', views.survey_summary, name='summary'),
    path('license/', views.stack_license, name='license'),
    path('age_compared/', views.age_compared, name='age_compared'),
    path('lang_worked_with_20/', views.lang_worked_with_20, name='lang_worked_with_20'),
    path('tree_map_20/', views.tree_map_20, name='tree_map_20'),
    path('lang_worked_with_23/', views.lang_worked_with_23, name='lang_worked_with_23'),
    path('tree_map_23/', views.tree_map_23, name='tree_map_23'),
    path('current_job/', views.current_job, name='current_job'),
    path('', views.survey_description, name='about'),
]
