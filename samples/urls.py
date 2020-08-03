from django.urls import path
from samples.views import SampleView, LabelView, ImageView

urlpatterns = [
    path('sample/', SampleView.as_view()),
    path('sample/<image_name>', ImageView.as_view()),
    path('label/<label_id>/', LabelView.as_view()),
    path('labels/', LabelView.as_view()),
]
