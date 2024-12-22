import random

from django.views.generic import TemplateView

from apps.core.models import *


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['text'] = random.choice([
            'Slicing onions...',
            'Chopping carrots...',
            'Boiling broccoli...',
            'Juicing oranges...',
            'Packing watermelons...',
        ])
        return context

#         context['buyer'] = Buyer.objects.last()
#         context['seller'] = Seller.objects.last()
#         context['goal'] = Goal.objects.last()
