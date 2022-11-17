import time

from django.core.exceptions import PermissionDenied



class FilterIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        allowed_ips = ['127.0.0.1']
        ip = request.META.get('REMOTE_ADDR')
        if ip not in allowed_ips:
            raise PermissionDenied

        response = self.get_response(request)

        return response


class RequestTimeMiddleware:
   def __init__(self, get_response):
       self.get_response = get_response
       self.request_count = 0

   def __call__(self, request):

       timestamp = time.monotonic()

       response = self.get_response(request)
       self.request_count +=1

       print(
           f'Запрос n{self.request_count}. Продолжительность запроса {request.path} - '
           f'{time.monotonic() - timestamp:.3f} сек.'
       )

       return response


# class CountIPReqMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#
#         count = cache.get_or_set(f'ip:{ip_address}', 0, < нужное
#         количество
#         секунд >)
#         count += 1
#         if count > < допустимое количество попыток >:
#             raise Exception('Давай, - до свидания')
#         else:
#             cache.set(f'ip:{ip_address}', count, < нужное
#             количество
#             секунд >)
#
#
#         allowed_ips = ['127.0.0.1']
#         ip = request.META.get('REMOTE_ADDR')
#         if ip not in allowed_ips:
#             raise PermissionDenied
#
#         response = self.get_response(request)
#
#         return response