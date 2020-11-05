from django.db import models
from home.baseModel import BaseModel


class Banner(BaseModel):
    img = models.ImageField(upload_to='banner', max_length=255, verbose_name='轮播图')
    title = models.CharField(max_length=50, verbose_name='图片标题')
    link = models.CharField(max_length=300, verbose_name='图片链接')

    class Meta:
        db_table = 'banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Navigator(BaseModel):

    POSITION_OPTION = (
        (1, '顶部导航'),
        (2, '底部导航'),
    )
    title = models.CharField(max_length=50, verbose_name='导航标题')
    link = models.CharField(max_length=300, verbose_name='导航链接')
    position = models.IntegerField(choices=POSITION_OPTION, default=1, verbose_name='导航栏位置')
    is_site = models.BooleanField(default=False, verbose_name='是否为外部链接')

    class Meta:
        db_table = 'nav'
        verbose_name = '导航栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
