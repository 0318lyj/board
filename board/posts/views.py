from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Post, Comments

#글 목록
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/list.html', {'posts': posts})

#글 상세
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})

#글 쓰기
@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        file = request.FILES.get('file')
        Post.objects.create(title=title, content=content, author=request.user, file=file)
        return redirect('post_list')
    return render(request, 'posts/form.html')

#글 수정
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        if request.FILES.get('file'):
            post.file = request.FILES['file']
        post.save()
        return redirect('post_detail', pk=pk)
    return render(request, 'posts/form.html', {'post': post})

#글 삭제
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

#회원가입
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'posts/register.html')

#로그인
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('post_list')
    return render(request, 'posts/login.html')

#로그아웃
def logout_view(request):
    logout(request)
    return redirect('login')

#댓글 작성
@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST['content']
        Comments.objects.create(post=post, author=request.user, content=content)
    return redirect('post_detail', pk=pk)

#댓글 삭제
@login_required
def comment_delete(request, pk, comment_pk):
    comment = get_object_or_404(Comments, pk=comment_pk)
    comment.delete()
    return redirect('post_detail', pk=pk)