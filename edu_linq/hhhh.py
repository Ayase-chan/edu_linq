from django_redis import get_redis_connection


redis_connection = get_redis_connection("cart")
cart_list = redis_connection.hgetall("cart_%s" % 4)
select_list = redis_connection.smembers("selected_%s" % 4)
print(cart_list)
print(select_list)
for course_id_byte, expire_id_byte in cart_list.items():
    course_id = int(course_id_byte)
    expire_id = int(expire_id_byte)
    print(course_id_byte, select_list)