from .models import Setting, Category


def send_setting_data(request):
    content = {
        'settingData': Setting.objects.last(),
        'categoryData': Category.objects.all()
    }

    return content


def make_title(request):
    content = {
        'title': 'My-Project'
    }
    return content
