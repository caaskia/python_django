from django.forms import ModelForm, Textarea
from .models import News, Comments

class NewsForm(ModelForm):

    class Meta:
        model = News
        fields = '__all__'


class CommentsForm(ModelForm):

    class Meta:
        model = Comments
        fields = [
            'username',
            'text',
        ]
        # widgets = {
        #     'content': Textarea(attrs={'cols': 10, 'rows': 3 }),
        # }
