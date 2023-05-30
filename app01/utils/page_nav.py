class PageNav:
    def __init__(self, req, queryset, page_parm="page", page_size=10, plus=5):
        """
        :param req: request
        :param queryset: queryset
        :param page_parm: URL中传递的获取分页的参数，例如：/list/?page=12
        :param page_size: 每页的数据条数
        :param plus: 底部导航栏在当前页面左右显示的页面数

        page_nav_obj = PageNav(request, queryset)
        page_queryset = page_nav_obj.page_queryset
        page_nav_string = page_nav_obj.get_html()
        content = {
            "queryset": page_queryset,
            "page_nav_string": page_nav_string,
        }

        <div style="display: flex; justify-content: center;"> {# 居中 #}
            <nav aria-label="Page navigation example" style="margin: 10px">
                <ul class="pagination">
                    {{ page_nav_string }}
                </ul>
            </nav>
        </div>
        """

        import copy
        query_dict = copy.deepcopy(req.GET)
        query_dict._mutable = True  # 让对象可被修改
        self.query_dict = query_dict
        # query_dict.setlist("page", [11])  # 修改get请求
        # self.url_code = req.GET.urlencode() # 打印请求字符串

        page = req.GET.get(page_parm, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = "1"
        self.page = page
        self.page_parm = page_parm
        self.total_count = queryset.count()
        self.page_count = self.total_count//page_size+1
        self.page_size = page_size
        self.start_page = page - plus
        self.end_page = page + plus
        self.page_queryset = queryset[page_size*(page-1):page_size*page]

    def get_html(self):
        self.query_dict.setlist(self.page_parm, [1])
        page_str_list = []
        page_str_list.append('<nav aria-label="Page navigation example" style="margin: 10px"><ul class="pagination">')

        self.query_dict.setlist(self.page_parm, [max(1, self.page - 1)])
        prv_ele = '<li class="page-item"><a class="page-link" href="?{}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
            self.query_dict.urlencode())

        self.query_dict.setlist(self.page_parm, [min(self.page_count, self.page + 1)])
        next_ele = '<li class="page-item"><a class="page-link" href="?{}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
            self.query_dict.urlencode())

        page_str_list.append(prv_ele)

        for i in range(max(1, self.start_page), min(self.end_page, self.page_count) + 1):
            self.query_dict.setlist(self.page_parm, [i])
            if i == self.page:
                ele = "<li class=\"page-item active\"><a class=\"page-link\" href=\"?{}\">{}</a></li>".format(
                    self.query_dict.urlencode(), i)
            else:
                ele = "<li class=\"page-item\"><a class=\"page-link\" href=\"?{}\">{}</a></li>".format(
                    self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        page_str_list.append(next_ele)

        page_str_list.append('</ul></nav>')
        page_nav_string = "".join(page_str_list)

        from django.utils.safestring import mark_safe
        page_nav_string = mark_safe(page_nav_string)
        return page_nav_string
