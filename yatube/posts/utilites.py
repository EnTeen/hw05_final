from django.conf import settings
from django.core.paginator import Paginator


def get_page(request, queryset, page_size=settings.PAGE_SIZE):
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
