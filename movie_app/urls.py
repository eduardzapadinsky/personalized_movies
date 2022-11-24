from django.urls import path
from .views import AllMovies, AllActors, AllDirectors, \
    OneActor, OneMovie, OneGenre, OneDirector, BestMovies,\
    AddRating, AddFeedback, FilterMoviesView, Search

urlpatterns = [
    # path('', main_page),
    # path('', BestMovies.as_view(), name='best_movies'),
    path('', AllMovies.as_view(), name='movies'),
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    path('search/', Search.as_view(), name='search'),
    path('feedback/<int:pk>/', AddFeedback.as_view(), name='add_feedback'),
    path('review/<int:pk>/', AddRating.as_view(), name='add_rating'),
    path('movies/<int:pk>', OneGenre.as_view(), name='genre'),
    path('movies/<str:slug>', OneMovie.as_view(), name='movie'),
    path('actors/', AllActors.as_view(), name='actors'),
    path('actors/<str:slug>', OneActor.as_view(), name='actor'),
    path('directors/', AllDirectors.as_view(), name='directors'),
    path('directors/<str:slug>', OneDirector.as_view(), name='director'),

]
