from django import forms

from .models import Rating, Feedback


class RatingForm(forms.ModelForm):
    """Форма рейтингів та дати перегляду"""

    class Meta:
        MONTHS = {
            1: 'січ', 2: 'лют', 3: 'бер', 4: 'кві',
            5: 'тра', 6: 'чер', 7: 'лип', 8: 'сер',
            9: 'вер', 10: 'жов', 11: 'лис', 12: 'гру'
        }
        model = Rating
        fields = ['rating', 'viewed_date']
        widgets = {
            "viewed_date": forms.SelectDateWidget(months=MONTHS, years=range(2020, 2025))
        }
        labels = {
            'rating': 'Рейтинг*',
            'viewed_date': 'Дата останнього перегляду',
        }


class FeedbackForm(forms.ModelForm):
    """Форма відгуків"""

    # captcha = ReCaptchaField()

    class Meta:
        model = Feedback
        fields = ('name', 'surname', 'email', 'feed')
        labels = {
            'name': "Ім'я*",
            'surname': "Прізвище*",
            'email': "email*",
            'feed': "Відгук*",
        }
