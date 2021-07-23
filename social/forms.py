from django import forms
from social import models

class postForm(forms.ModelForm):
	class Meta:
		model = models.Post
		fields = ['content', "image"]


class commentForm(forms.ModelForm):
	class Meta:
		model = models.Comment
		fields = ['content']