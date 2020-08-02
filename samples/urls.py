from django.urls import path
from samples.views import SampleView, LabelView

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('label/<sample_id>/', LabelView.as_view()),
]
