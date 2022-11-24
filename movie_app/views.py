from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from datetime import date, timedelta

from .models import Movie, Actor, Director, Genre, Rating
from .forms import RatingForm, FeedbackForm
from .service import get_client_ip


class FilterData:
    """Фільтр по жанрах, роках, рейтингах"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.all().values("year")

    def get_rating(self):
        return [4, 5, 6, 7, 8, 9]

    def get_date(self):
        return [0, 1, 2, 3, 4, 5]



class BestMovies(FilterData, ListView):
    # template_name = 'movie_app/main_page.html'
    model = Movie
    context_object_name = 'movies'


class AllMovies(FilterData, ListView):
    """Список фільмів"""
    # form_class = FeedbackForm
    # success_url = ''
    # template_name = 'movie_app/movie_list.html'
    model = Movie

    # creating auto slug
    # movies = Movie.objects.all()
    # for movie in movies:
    #     movie.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["get_client_ip"] = get_client_ip(self.request)
        return context


class AllActors(ListView):
    """Список акторів"""
    # template_name = 'movie_app/actor_list.html'
    model = Actor
    context_object_name = 'actors'
    # creating auto slug
    # actors = Actor.objects.all()
    # for actor in actors:
    #     actor.save()


class AllDirectors(ListView):
    """Список режисерів"""
    # template_name = 'movie_app/director_list.html'
    model = Director
    context_object_name = 'directors'
    # creating auto slug
    # directors = Director.objects.all()
    # for director in directors:
    #     director.save()


class OneActor(FilterData, DetailView):
    """Інформація про актора"""
    # template_name = 'movie_app/actor_detail.html'
    model = Actor


class OneDirector(FilterData, DetailView):
    """Інформація про режисера"""
    # template_name = 'movie_app/director_detail.html'
    model = Director


class OneMovie(FilterData, DetailView):
    """Інформація про фільм"""
    # template_name = 'movie_app/movie_detail.html'
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = RatingForm()
        context["form_f"] = FeedbackForm()
        context["get_client_ip"] = get_client_ip(self.request)
        return context


class OneGenre(DetailView):
    """Інформація про жанр"""
    # template_name = 'movie_app/genre_detail.html'
    model = Genre


class AddRating(View):
    """Додавання рейтингу до фільму"""

    def post(self, request, pk):
        """Зберігаємо чи редагуємо форму"""
        form = RatingForm(request.POST)
        movie = Movie.objects.get(id=pk)
        ip = get_client_ip(request)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=ip,
                movie_id=movie.id,
                defaults={"rating": request.POST.get("rating")}
            )
            return redirect(movie.get_url())


class AddFeedback(View):
    """Відгуки"""

    def post(self, request, pk):
        form = FeedbackForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        return redirect(movie.get_url())


class FilterMoviesView(FilterData, ListView):
    """Фільтр фільмів"""
    paginate_by = 2

    def get_queryset(self):
        self_get = self.request.GET
        if "year" in self_get:
            get_year = self_get.getlist("year")
        else:
            get_year = self.get_years()
        if "genre" in self_get:
            get_genre = self_get.getlist("genre")
        else:
            get_genre = self.get_genres()
        if "rating_imdb" in self_get:
            get_rating_imdb = self_get.getlist("rating_imdb")[0]
        else:
            get_rating_imdb = 4
        if "my_date" in self_get:
            get_my_date = self_get.getlist("my_date")[0]
        else:
            get_my_date = 0
        today = date.today()
        get_my_date = today - timedelta(days=int(get_my_date) * 30)
        print(get_my_date)
        if "my_rating" in self_get:
            get_my_rating = self_get.getlist("my_rating")[0]
            queryset = Movie.objects.filter(year__in=get_year, genres__in=get_genre, rating_imdb__gte=get_rating_imdb,
                                            rating__ip=get_client_ip(self.request), rating__rating__gte=get_my_rating,
                                            rating__viewed_date__lte=get_my_date
                                            ).distinct()
        else:
            queryset = Movie.objects.filter(year__in=get_year, genres__in=get_genre, rating_imdb__gte=get_rating_imdb
                                            ).distinct()
        print(self_get)
        print(queryset)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class Search(FilterData, ListView):
    """Пошук фільмів"""
    paginate_by = 1

    # def get_queryset(self):
    #     return Movie.objects.filter(name__iregex=self.request.GET.get("q"))

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(name__iregex=self.request.GET.get("q")) |
            Q(original_name__iregex=self.request.GET.get("q"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["q"] = self.request.GET.get("q")
    #     return context
