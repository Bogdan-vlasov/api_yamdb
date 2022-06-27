
import django_filters

from posts.models import Title


class TitlesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')