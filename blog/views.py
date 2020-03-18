from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse 
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	) 
import time 
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post
from django.contrib.auth.models import User
from blog.forms import PostSearchForm
from django.views.generic import View
from django.contrib import messages 

class PostAboutListView(View):
	form_class = PostSearchForm
	template_name = 'blog/about.html'


	
	def get(self, request, *args, **kwargs):
		title = self.request.GET.get('title')
		context = { 
		'fm': self.form_class
		}
		return render(request, 'blog/about.html',context)






	def post(self, request, *args, **kwargs):
		paginate_by = 3
		title = self.request.POST.get('title')
		posts = Post.objects.filter(title__contains = title)
		context = { 
		'fm': self.form_class,
		'posts' : posts

		}
		if posts:
			return render(request, 'blog/about.html',context)
		else:
			messages.info(request,'No results found! Try another please...')
			return redirect('blog-about')





#it is the old version !
# def home(request):
# 	context = {
# 		'posts': Post.objects.all()
# 	}
# 	return render(request,'blog/home.html',context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5
	


class PostLatestListView(ListView):
	model = Post
	template_name = 'blog/latest.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	
	def get_queryset(self):
		return Post.objects.order_by('-date_posted')[:5]
	


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_post.html'
	context_object_name = 'posts'
	paginate_by = 5


	def get_queryset(self):
		user = get_object_or_404(User, username =self.kwargs.get('username')) # Когда вызывается эта функция 
																			  # то в SELF сохраняются данные 
																			  # передаанные из URL
		

		return Post.objects.filter(author = user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post 
	fields = ['title', 'content']


	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
# Реализация по умолчанию для метода form_valid() просто осуществляет 
#редирект на URL, хранящийся в атрибуте success_url или в get_absolute_url который записан 
#в самой модели 




class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post 
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False




class PostDetailView(DetailView):
	model = Post
	context_object_name = 'post'


# def about(request):
# 	return render(request,'blog/about.html',{'title': 'About Page'})



class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	context_object_name = 'post'
	success_url = '/'
	def test_func(self):
			post = self.get_object()
			if self.request.user == post.author:
				return True
			return False
