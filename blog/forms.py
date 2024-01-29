# from django import forms
# from .models import Comment

# class EmailPostForm(forms.Form):
#     # для имени человека, отправляющего пост
#     name = forms.CharField(max_length=25)
#     # адрес электронной почты человека, отправившего пост
#     email = forms.EmailField()
#     # используется адрес электронной почты получателя
#     to = forms.EmailField()
#     # для комментариев которые будут вставляться в электронное письмо
#     comments = forms.CharField(required=False, widget=forms.Textarea)


# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         # В форме CommentForm мы включили поля name, email и body в явном виде
#         fields = ['name', 'email', 'body']

from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                            widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

# для поискового запроса
class SearchForm(forms.Form):
    query = forms.CharField()
