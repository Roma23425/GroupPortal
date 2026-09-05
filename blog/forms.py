from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Comment, Post


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="Електронна пошта",
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@mail.com'
        })
    )
    name = forms.CharField(
        label="Ваше ім'я",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Тарас Шевченко'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()
            
class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['username'].widget.attrs['placeholder'] = 'Введіть ваш логін'
        self.fields['password'].widget.attrs['placeholder'] = 'Введіть пароль'
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Ваш коментар',
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Поділіться своїми думками...', 
                'style': 'resize: vertical;' 
            }),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        labels = {
            'title': 'Заголовок',
            'content': 'Контент',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть заголовок...'}),
            # The CKEditor5 widget is automatically applied to the content field because of the model definition.
        }