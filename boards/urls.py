from django.urls import path

from boards.views import BoardCreateView, BoardListView, BoardReadView, BoardUpdateView, BoardDeleteView

urlpatterns = [
    path('/create', BoardCreateView.as_view()),
    path('/lists', BoardListView.as_view()),
    path('/reads/<int:board_id>', BoardReadView.as_view()),
    path('/updates', BoardUpdateView.as_view()),
    path('/delete/<int:board_id>', BoardDeleteView.as_view())
]