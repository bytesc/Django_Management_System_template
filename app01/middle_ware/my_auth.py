from django.utils.deprecation import MiddlewareMixin
# 中间件
from django.shortcuts import redirect


# class MiddleWare01(MiddlewareMixin):
#     def process_request(self,request): # process_request是特殊的函数名，不能变
#         print("01进来了")
#
#     def process_response(self, request, response): # process_response是特殊的函数名，不能变
#         print("01走了")
#         return response
#
#
# class MiddleWare02(MiddlewareMixin):
#     def process_request(self, request):
#         print("02进来了")
#
#     def process_response(self, request, response):
#         print("02走了")
#         return response

class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, req):
        if req.path_info in ["/login/", "/"]:
            return  # return表示放行
        info = req.session.get("info")
        if info:
            return  # return表示放行
        return redirect("/login/")
