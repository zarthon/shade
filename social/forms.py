from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from shade.social.models import UserProfile, Message, Comment, Picture
import hashlib

class SettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('url', 'gender', 'hometown', 'home_state', 'home_country',
                'current_town', 'current_state', 'current_country',
                'bio',)

    def clean(self):
        super(forms.ModelForm, self).clean()
        if ' ' in self.cleaned_data['url']:
            self._errors['url'] = [u'URL cannot contain spaces.']
        return self.cleaned_data

class MessageForm(forms.ModelForm):
    class  Meta:
        model = Message
        fields = ('recipient', 'subject', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 7}),
        }

    def clean(self):
        super(forms.ModelForm, self).clean()
        subject = self.cleaned_data['subject']
        if subject.isspace():
            self.cleaned_data['subject'] = 'No Subject'

        recipient = self.cleaned_data['recipient']
        author = self.instance.author
        if recipient not in author.get_profile().friends.all():
            self._errors['url'] = [u'User not in your friends.']

        return self.cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('post',)
        widgets = {
            'post': forms.Textarea(attrs={'cols': 80, 'rows': 7}),
        }

class AlbumForm(forms.Form):
    name = forms.CharField()

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('image', 'caption',)

class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    def clean(self):
        name = self.cleaned_data['name']
        name_l = name.split(' ')
        if len(name_l) != 2:
            self._errors['name'] = [u'Use first name and last name']
        return self.cleaned_data

