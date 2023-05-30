from django.apps import AppConfig


class App01Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"  # 可自动创建id
    name = "app01"
# 需要把app注册到setting.py
