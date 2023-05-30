from django import forms


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环所有插件定义样式
        for name, field in self.fields.items():
            # print(name, field)
            field.widget.attrs["class"] = "form-control"
            if field.widget.attrs.get("placeholder") is None:
                field.widget.attrs["placeholder"] = field.label
            # .label表示verbose_name字段

