from django.urls import path
from . import views as views
from .views import *

urlpatterns = [
    path('test', views.test, name='test'),
    path('index/ ', views.index, name='index'),
    path('historique/ ', views.historique, name='historique'),
    path('apropos/ ', views.apropos, name='apropos'),
    path('profile/', views.users, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('details_ipo/ ', views.details_ipo, name='details_ipo'),
    path('details_iqe/ ', views.details_iqe, name='details_iqe'),
    path('details_iqa/ ', views.details_iqa, name='details_iqa'),
    path('upload/', FileUploadView.as_view(), name='upload'),
    # path('tableau_de_bord/', view.tableau_de_bord, name='tableau_de_bord'),
]