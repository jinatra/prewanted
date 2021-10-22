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
                return JsonResponse({'MESSAGE':'please fill in both title and content'})

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
            LIMIT  = request.GET.get('limit', 10)

            boards = Board.objects.all()[OFFSET:LIMIT]

            board_info = {
                'count' : boards.count(),
                'data'  : [
                    {
                    'title'     : board.title,
                    'content'   : board.content,
                    'user'      : board.user,
                    'created_at' : board.create_at
                    } for board in boards
                ]
            }

            return JsonResponse({'MESSAGE':board_info}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)


class BoardReadView(View):
    def get(self, request, board_id):
        try:
            board = Board.objects.filter(id=board_id)

            if not board.exists():
                return JsonResponse({'MESSAGE':'non-existing board'}, status=400)

            board_info = {
                'title'         : board.info,
                'content'       : board.content,
                'user_id'       : board.user.id,
                'user_nickname' : board.user.nickname,
                'created_at'    : board.create_at,
            }

            return JsonResponse({'MESSAGE':board_info}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)


class BoardUpdateView(View):
    @login_decorator
    def put(self, request):
        try:
            data        = json.loads(request.body)
            board_id    = data['board_id']
            new_title   = data['new_title']
            new_content = data['new_content']

            board = Board.objects.filter(id=board_id)

            if not board.exists():
                return JsonResponse({'MESSAGE':'non-existing board'}, status=400)

            if not len(new_title) == 0 or len(new_content) == 0:
                return JsonResponse({'MESSAGE':'Please fill in both title and content'})

            board.update(
                title = new_title,
                content = new_content,
            )

            update_time = Board.objects.get(id=board_id).updated_at

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
                return JsonResponse({'MESSAGE':'non-existing board'}, status=204)

            if not Board.objects.get(id=board_id).user.id == request.user.id:
                return JsonResponse({'MESSAGE':'wrong user'}, status=204)

            board.delete()

            return JsonResponse({'MESSAGE':'board deleted'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=204)

        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=204)
