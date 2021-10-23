from django.urls import path

from boards.views import BoardCreateView, BoardListView, BoardReadView, BoardUpdateView, BoardDeleteView

urlpatterns = [
    path('/create', BoardCreateView.as_view()),
    path('/list', BoardListView.as_view()),
    path('/read/<int:board_id>', BoardReadView.as_view()),
    path('/update/<int:board_id>', BoardUpdateView.as_view()),
    path('/delete/<int:board_id>', BoardDeleteView.as_view())
]