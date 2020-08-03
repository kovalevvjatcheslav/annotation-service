from django.urls import path
from samples.views import SampleView, LabelView, ImageView

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('sample/<image_name>', ImageView.as_view()),
    path('label/<sample_id>/', LabelView.as_view()),
]
