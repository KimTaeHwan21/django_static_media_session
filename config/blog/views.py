from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from django.core.paginator import Paginator
import os
from django.conf import settings

# READ
def home(request):
    blogs = Blog.objects.all().order_by('-id')
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})

# DETAIL READ
def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog': blog})


# CREATE
def create(request):
    if request.method == 'POST':
        new_blog = Blog()
        new_blog.title = request.POST['title']
        new_blog.content = request.POST['content']
        new_blog.image = request.FILES.get('image')
        new_blog.save()
        return redirect('detail', new_blog.id)
    return render(request, 'new.html')

def update(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == 'POST':
        blog.title = request.POST['title']
        blog.content = request.POST['content']
        new_image = request.FILES.get('change_image')
        delete_image = request.POST.get('file_delete')  # 삭제할 사진

        if new_image:   # 만약 수정하는게 새로운 사진을 가져오는 거라면 기존꺼에서 새로운걸로 교체
            blog.image = new_image
        elif delete_image:  # 새로운 사진을 가져오는게 아니라 사진을 없애고 싶으면 사진 삭제
            if blog.image and os.path.isfile(blog.image.path):
                os.remove(blog.image.path)
            blog.image = None

        blog.save()
        return redirect('detail', blog.id)

    return render(request, 'edit.html', {'edit_blog': blog})

def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)

    if request.method == "POST":
        blog.delete()
        return redirect('home')
    return redirect('home')