from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from social import models, forms
from django.db.models import Q
# Create your views here.


class Wall(LoginRequiredMixin, ListView):
	context_object_name = 'posts'
	template_name = 'social/wall.html'
	login_url = 'auth/login'

	def get_queryset(self):
		friendIds = [ friend.person2.id for friend in models.Friends.objects.filter(person1 = self.request.user)]
		friendIds = friendIds + [ friend.person1.id for friend in models.Friends.objects.filter(person2 = self.request.user)]
		# filtered =  models.Post.objects.filter(
		# 	(Q(user__person2 = self.request.user.pk) | Q(user__person1 = self.request.user.pk)) &
		# 	~Q(user = self.request.user.pk)
		# )
		filtered = models.Post.objects.filter(user__in = friendIds)
		return filtered[::-1]


class Home(LoginRequiredMixin, ListView):
	context_object_name = 'posts'
	template_name = 'social/home.html'
	login_url = '/auth/login'

	def get_queryset(self):
		return models.Post.objects.filter(user = self.request.user)[::-1]

	def get_context_data(self, *args, **kwargs):
		data = super().get_context_data(*args, **kwargs)
		data['post_form'] = forms.postForm()
		return data


class Post(View):
	def post(self, request):
		form = forms.postForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)     #Commit=False means form wont be saved in database but a post object will be returned
			post.user = request.user
			post.save()

		return redirect('/home/')


class likePostOnClick(View):
	def post(self, request, pk):

		already_liked = models.Like.objects.filter(user = request.user, post = pk)

		if already_liked.count() == 0:
			models.Like.objects.create(post = models.Post.objects.get(pk = pk), user = request.user)

		return HttpResponse(status = 204)

class postComment(View):
	form = forms.commentForm

	def post(self, request, pk):
		post = models.Post.objects.get(pk = pk)
		form = self.form(request.POST)

		if form.is_valid():
			comment = form.save(commit = False)
			comment.user = request.user
			comment.post = post
			comment.save()
			return HttpResponse(status = 204)

		return HttpResponse(status = 400)