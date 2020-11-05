import xadmin
from xadmin import views
from home.models import Banner, Navigator


class BaseSetting(object):
    # 基本配置
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    # 全局配置
    site_title = "明教管理"  # 设置站点标题
    site_footer = "明教"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


xadmin.site.register(views.CommAdminView, GlobalSettings)


# 将banner注册到后台
class BannerInfo(object):
    list_display = ['title', "orders", "is_show"]


xadmin.site.register(Banner, BannerInfo)


class NavigatorInfo(object):
    list_display = ['title', 'orders', 'is_show']


xadmin.site.register(Navigator, NavigatorInfo)
