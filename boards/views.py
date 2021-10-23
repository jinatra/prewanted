import json
import re

from django.http.response import JsonResponse
from django.views     import View

from boards.models   import Board
from users.decorator import login_decorator


class BoardCreateView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            title   = data['title']
            content = data['content']
            user    = request.user

            if len(title) == 0 or len(content) == 0:
                return JsonResponse({'MESSAGE':'please fill in both title and content'}, status=400)

            board = Board(
                title   = title,
                content = content,
                user    = user,
            )
            board.save()

            board_info = {
                'title'         : board.title,
                'content'       : board.content,
                'user_id'       : board.user.id,
                'user_nickname' : board.user.nickname
            }

            return JsonResponse({'MESSAGE':board_info}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)


class BoardListView(View):
    def get(self, request):
        try:
            OFFSET = request.GET.get('offset', 0)
            LIMIT  = request.GET.get('limit', 1)

            boards = Board.objects.all()[OFFSET:LIMIT]

            board_info = {
                'count' : boards.count(),
                'data'  : [
                    {
                    'title'         : board.title,
                    'content'       : board.content,
                    'user_id'       : board.user.id,
                    'user_nickname' : board.user.nickname,
                    'created_at'    : board.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    } for board in boards
                ]
            }

            return JsonResponse({'MESSAGE':board_info}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)


class BoardReadView(View):
    def get(self, request, board_id):
        try:
            if not Board.objects.filter(id=board_id).exists():
                return JsonResponse({'MESSAGE':'non-existing board'}, status=404)

            board = Board.objects.get(id=board_id)

            board_info = {
                'title'         : board.title,
                'content'       : board.content,
                'user_id'       : board.user.id,
                'user_nickname' : board.user.nickname,
                'created_at'    : board.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }

            return JsonResponse({'MESSAGE':board_info}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)


class BoardUpdateView(View):
    @login_decorator
    def post(self, request, board_id):
        try:
            data        = json.loads(request.body)
            new_title   = data['new_title']
            new_content = data['new_content']

            if not Board.objects.filter(id=board_id).exists():
                return JsonResponse({'MESSAGE':'non-existing board'}, status=404)

            if len(new_title) == 0 or len(new_content) == 0:
                return JsonResponse({'MESSAGE':'please fill in both title and content'}, status=400)

            board = Board.objects.get(id=board_id)

            board.title   = new_title
            board.content = new_content
            board.save()

            update_time = board.updated_at.strftime('%Y-%m-%d %H:%M:%S')

            return JsonResponse({'MESSAGE':'board edited', 'UPDATE_TIME':update_time}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)


class BoardDeleteView(View):
    @login_decorator
    def delete(self, request, board_id):
        try:
            board = Board.objects.filter(id=board_id)

            if not board.exists():
                return JsonResponse({'MESSAGE':'board-not-exists'}, status=404)

            if not Board.objects.get(id=board_id).user.id == request.user.id:
                return JsonResponse({'MESSAGE':'wrong user'}, status=404)

            board.delete()

            return JsonResponse({'MESSAGE':'board deleted'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
