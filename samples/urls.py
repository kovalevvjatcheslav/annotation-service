from django.urls import path
from samples.views import SampleView

urlpatterns = [
    path('sample/', SampleView.as_view())
]
