from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection

from course.models import Course, CourseExpire
from edu_linq.utils import contastnt


class CartViewSet(ViewSet):
    """购物车相关操作"""

    # 只有登录成功的用户才可以访问此接口
    permission_classes = [IsAuthenticated]

    def get_cart_count(self, request):
        redis_connection = get_redis_connection("cart")
        user_id = request.user.id
        course_len = redis_connection.hlen("cart_%s" % user_id)
        print(course_len)
        return Response({
            "message": '获取成功',
            "cart_count": course_len
        })

    def add_cart(self, request):
        """
        将用户在前端提交的信息保存至购物车
        params: 用户id  课程id  勾选状态  有效期
        """
        course_id = request.data.get("course_id")

        user_id = request.user.id
        print(user_id)
        # 是否勾选
        select = True
        # 有效期
        expire = 0

        # 校验前端参数
        try:
            Course.objects.get(is_show=True, is_del=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，课程不存在"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # 获取数据库连接
            redis_connection = get_redis_connection("cart")

            # 将数据保存到redis  使用redis管道
            pipeline = redis_connection.pipeline()
            # 保存的是商品的信息以及对应的有效期
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            # 商品的勾选状态
            pipeline.sadd("selected_%s" % user_id, course_id)

            # 执行命令
            pipeline.execute()

            # 获取购物车中商品的总数据量
            course_len = redis_connection.hlen("cart_%s" % user_id)

        except:
            return Response({"message": "参数有误，购物车添加失败"},
                            status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"message": "购物车添加成功", "cart_length": course_len})

    def list_cart(self, request):
        """展示购物车"""

        # 获取所需参数
        user_id = request.user.id
        # user_id = 1
        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall("cart_%s" % user_id)
        selected_list_bytes = redis_connection.smembers("selected_%s" % user_id)

        # 获取前端所需的商品信息
        data = []
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            try:
                # 循环找到所有需要的课程信息
                course = Course.objects.get(is_show=True, pk=course_id, is_del=False)
            except Course.DoesNotExist:
                continue

                # 将前端所需的信息返回
            data.append({
                "selected": True if course_id_byte in selected_list_bytes else False,
                "course_img": contastnt.IMG_SRC + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expire_list": course.expire_text,
                "expire_id": expire_id,
                "real_price": course.real_price(),
                "real_expire_price": 0.00
            })

        return Response(data)

    def change_selected(self, request):
        user_id = request.user.id
        course_id = request.data.get('course_id')
        print(user_id, course_id)
        redis_connection = get_redis_connection('cart')
        a = redis_connection.sismember("selected_%s" % user_id, course_id)
        if a:
            redis_connection.srem("selected_%s" % user_id, course_id)
        else:
            redis_connection.sadd("selected_%s" % user_id, course_id)
        return Response({
            'message': '修改成功',
        })

    def del_item(self, request):
        user_id = request.user.id
        course_id = request.data.get('course_id')
        print(user_id, course_id)
        redis_connection = get_redis_connection('cart')
        redis_connection.hdel("cart_%s" % user_id, course_id)
        a = redis_connection.sismember("selected_%s" % user_id, course_id)
        if a:
            pass
        else:
            redis_connection.srem("selected_%s" % user_id, course_id)
        return Response({
            'message': '删除成功',
        })

    def change_expire(self, request):
        """改变redis中课程有效期"""
        # 获取用户id  课程id  有效期id
        user_id = request.user.id
        expire_id = request.data.get("expire_id")
        course_id = request.data.get("course_id")
        real_expire_price = 0.00
        # 查询操作的课程是否存在
        try:
            course = Course.objects.get(is_del=False, is_show=True, pk=course_id)

            # 如果前端传递的有效期的id不是0 则修改对应课程的有效期
            if expire_id > 0:
                expire_obj = CourseExpire.objects.filter(is_show=True, is_del=False, pk=expire_id)
                real_expire_price = course.real_expire_price(expire_id=expire_id)
                if not expire_obj:
                    raise CourseExpire.DoesNotExist("课程有效期不存在")
            else:
                real_expire_price = course.price

        except Course.DoesNotExist:
            return Response({"message": "课程信息不存在"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection("cart")
        redis_connection.hset("cart_%s" % user_id, course_id, expire_id)
        return Response({
            "message": "有效期切换成功",
            "real_expire_price": real_expire_price,
            "expire_id": expire_id
        })

    def get_select_course(self, request):
        """
        获取购物车中选中的课程
        """
        user_id = request.user.id
        # user_id = 1
        redis_connection = get_redis_connection("cart")

        # 获取当前登录用户的购物车数据
        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        select_list = redis_connection.smembers("selected_%s" % user_id)

        # 商品总价
        total_price = 0
        data = []

        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            # 判断商品是否被勾选
            if course_id_byte in select_list:
                # 获取课程的所有信息
                try:
                    course = Course.objects.get(is_del=False, is_show=True, pk=course_id)
                except Course.DoesNotExist:
                    continue

                # TODO 计算商品最终的总价格
                # 如果课程的有效期id大于0，则需要重新计算商品的价格，id不大于0则是永久有效
                origin_price = course.price
                expire_text = "永久有效"

                if expire_id > 0:
                    try:
                        course_expire = CourseExpire.objects.get(pk=expire_id)
                        # 获取有效期对应的原价
                        origin_price = course_expire.price
                        expire_text = course_expire.expire_text
                        final_price = course.real_expire_price(expire_id=expire_id)
                    except course.DoesNotExist:
                        return ({
                            "message": "获取有效期价格出错，未找到该有效期"
                        })

                # TODO 根据已勾选的客户课程对应 的有效期的的价格计算最终价格
                else:
                    final_price = course.real_price()  # 如果是有效期  需要传递id

                # 将订单结算页的所需的数据返回
                data.append({
                    "course_img": contastnt.IMG_SRC + course.course_img.url,
                    "name": course.name,
                    # 最终的价格  参与过活动  有效期的价格
                    "final_price": final_price,
                    "id": course.id,
                    "expire_text": expire_text,
                    "price": origin_price
                })

                # 商品的总价
                total_price += float(final_price)

        return Response({"course_list": data, "total_price": total_price, "message": "获取成功"})
