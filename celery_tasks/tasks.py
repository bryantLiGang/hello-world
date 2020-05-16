from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from apps.goods.models import PromotionPc,ProductBanner,ProductCategory,ProductSKU,TypeShow
import os
app = Celery('celery_tasks.tasks',broker='redis://192.168.1.9:6379/8')


@app.task
def register_user_active_mail(to_email,username,token):
    subject = '天天生鲜欢迎信息'
    message = ''
    html_message = '<h1>%s,欢迎来到天天生鲜验证页面</h1>请点击以下链接进行账号激活<br/>' \
                   '<a href="http://127.0.0.1:8000/user/active/%s">"http://127.0.0.1:8000/user/active/%s"</a>' % (
                   username, token, token)
    sender = settings.EMAIL_FROM
    reciver = [to_email]
    send_mail(subject, message, sender, reciver, html_message=html_message)


@app.task
def get_static_index_html():
    types = ProductCategory.objects.all()

    ### 获取首页轮播商品
    banner_goods = ProductBanner.objects.all().order_by('index')

    ### 获取活动商品
    promotion_goods = PromotionPc.objects.all().order_by('index')

    ### 获取首页商品分类信息
    # types_goods = TypeShow.objects.all().order_by('index')
    for type in types:
        image_goods = TypeShow.objects.filter(product_type=type, display_type=1)
        title_goods = TypeShow.objects.filter(product_type=type, display_type=0)
        type.image_goods = image_goods
        type.title_goods = title_goods
        ### 组织上下文
    context = {
        'types': types,
        'banner_goods': banner_goods,
        'promotion_goods': promotion_goods
    }
    ### 获取模板
    temp = loader.get_template('static_index.html')
    ### 渲染模板
    static_index_html = temp.render(context)

    save_path = os.path.join(settings.BASE_DIR,'static/index.html')
    with open(save_path,'w',encoding='uft-8') as f:
        f.write(static_index_html)




    ### 构建模板上下文

    # return render(request, 'index.html', context)