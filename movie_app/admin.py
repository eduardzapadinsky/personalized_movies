from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models import QuerySet
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Movie, Actor, Director, Genre, PlaceResidence, Rating, Feedback


class MovieAdminForm(forms.ModelForm):
    """Форма з віджетом ckeditor"""
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


admin.site.register(Genre)


class RatingFilter(admin.SimpleListFilter):
    """Фільтр рейтинга IMDB"""
    title = "Rating filter"
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('<5', 'Bad rating'),
            ('<6', 'Average rating'),
            ('<7', 'Good rating'),
            ('>=7', 'Brilliant rating'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<5':
            return queryset.filter(rating_imdb__lt=5)
        if self.value() == '<6':
            return queryset.filter(rating_imdb__gte=5, rating_imdb__lt=6)
        if self.value() == '<7':
            return queryset.filter(rating_imdb__gte=6, rating_imdb__lt=7)
        if self.value() == '>=7':
            return queryset.filter(rating_imdb__gte=7)
        return queryset


class YearFilter(admin.SimpleListFilter):
    """Фільтр років"""
    title = "Year filter"
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return [
            ('<2000', 'Before 2000'),
            ('<2010', '2000 - 2009'),
            ('<2020', '2010 - 2019'),
            ('>=2020', 'After 2020'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<2000':
            return queryset.filter(year__lt=2000)
        if self.value() == '<2010':
            return queryset.filter(year__gte=2000, year__lt=2010)
        if self.value() == '<2020':
            return queryset.filter(year__gte=2010, year__lt=2020)
        if self.value() == '>=2020':
            return queryset.filter(year__gte=2020)
        return queryset


class FeedbackInline(admin.TabularInline):
    """Відгуки на сторінці фільму"""
    model = Feedback
    extra = 1
    readonly_fields = ("email",)
    classes = ['collapse']


class RatingInline(admin.TabularInline):
    """Відгуки на сторінці фільму"""
    model = Rating
    extra = 1
    readonly_fields = ("ip", "rating", "viewed_date")
    classes = ['collapse']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фільми"""
    prepopulated_fields = {'slug': ('original_name',)}
    list_display = ['name', 'original_name', 'year', 'director', 'get_image', 'rating_status']
    list_editable = ['original_name', 'year', 'director']
    ordering = ['-rating_imdb', 'name']
    list_per_page = 20
    search_fields = ['name', 'original_name', 'year', 'length', 'rating_imdb']
    list_filter = [RatingFilter, YearFilter, 'director']
    form = MovieAdminForm
    inlines = [RatingInline, FeedbackInline]
    readonly_fields = ('get_image',)
    save_on_top = True
    fieldsets = (
        (None, {"fields": (('name', 'original_name', 'slug'),)}),
        (None, {"fields": (('year', 'length', 'rating_imdb'),)}),
        (None, {"fields": (('actors', 'director'),)}),
        (None, {"fields": (("picture", "get_image"),)}),
        ("Genres", {
            "classes": ("collapse",),
            "fields": ('genres',)}),
        ("Description", {
            "classes": ("collapse",),
            "fields": ('description',)}),
    )

    @admin.display(ordering='rating_imdb')
    def rating_status(self, movie: Movie):
        """Додаткове поле сортування за рейтингом IMDB"""
        if movie.rating_imdb < 5:
            return 'Bad rating'
        if movie.rating_imdb < 6:
            return 'Average rating'
        if movie.rating_imdb < 7:
            return 'Good rating'
        return 'Brilliant rating'

    def get_image(self, obj):
        """Відображення зображень"""
        return mark_safe(f'<img src={obj.picture.url} height="150"')

    get_image.short_description = "Постер"


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    """Режисери"""
    list_display = ['first_name', 'last_name', 'director_email']
    list_editable = ['last_name', 'director_email']
    list_per_page = 20
    search_fields = ['first_name', 'last_name', 'director_email']
    fieldsets = (
        (None, {"fields": (('first_name', 'last_name', 'slug'),)}),
        (None, {"fields": ('director_email',)}),
    )


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актори"""
    list_display = ['first_name', 'last_name', 'gender', 'residence']
    list_editable = ['last_name', 'gender', 'residence']
    list_per_page = 20
    actions = ['set_gender_male', 'set_gender_female']
    search_fields = ['first_name', 'last_name']
    list_filter = ['gender']
    fieldsets = (
        (None, {"fields": (('first_name', 'last_name', 'slug'),)}),
        (None, {"fields": (('gender',),)}),
        (None, {"fields": ('residence',)}),
    )

    @admin.action(description='Set gender to male')
    def set_gender_male(self, request, qs: QuerySet):
        """Дія по статі м."""
        count_updated = qs.update(gender=Actor.MALE)
        self.message_user(request, f'It was updated {count_updated} str.')

    @admin.action(description='Set gender to female')
    def set_gender_female(self, request, qs: QuerySet):
        """Дія по статі ж."""
        count_updated = qs.update(gender=Actor.FEMALE)
        self.message_user(request, f'It was updated {count_updated} str.')


@admin.register(PlaceResidence)
class PlaceResidenceAdmin(admin.ModelAdmin):
    """Місце проживання"""
    list_display = ['country', 'city', 'street', 'number', 'map_coordinate']
    list_editable = ['city', 'street', 'number', 'map_coordinate']
    list_per_page = 20
    search_fields = ['country', 'city', 'street', 'number', 'map_coordinate']
    list_filter = ['country', 'city']
    fieldsets = (
        (None, {"fields": (('country', 'city'),)}),
        (None, {"fields": (('street', 'number'),)}),
        (None, {"fields": ('map_coordinate',)}),
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинги"""
    list_display = ['ip', 'rating', 'viewed_date', 'movie']
    list_editable = ['rating', 'viewed_date']
    list_per_page = 20
    search_fields = ['rating', 'viewed_date']
    list_filter = ['rating', 'viewed_date']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Відгуки"""
    list_display = ['id', 'email', 'name', 'surname', 'feed']
    list_editable = ['feed']
    list_per_page = 20
    search_fields = ['name', 'surname', 'feed']
    list_filter = ['name', 'surname']
