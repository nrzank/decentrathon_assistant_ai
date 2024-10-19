from django.urls import path
from .views import (
    ClassifyAndAnswerView,
    TrainModelView,
    SubjectListView,
    SubjectDetailView,
    AnswerCreateView,
    QuestionListView,
    QuestionDetailView,
)

urlpatterns = [
    path('classify-and-answer/', ClassifyAndAnswerView.as_view(), name='classify_and_answer'),
    path('train-model/', TrainModelView.as_view(), name='train_model'),
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('subjects/<int:pk>/', SubjectDetailView.as_view(), name='subject_detail'),
    path('answers/', AnswerCreateView.as_view(), name='answer_create'),
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail')
]

