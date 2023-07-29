from django import forms
from post.models import Post

class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'image', 'body',)

class PostUpdateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'image', 'body',)