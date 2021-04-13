
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, Author, Category
from .forms import*
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.core.paginator import EmptyPage, Paginator,PageNotAnInteger,Page

from django.db.models import Q

# Create your views here.


def index(request):
    first = Article.objects.first()
    last_post = Article.objects.last()
    recent = Article.objects.all().order_by('-time')[1:2]
    recent_more = Article.objects.all().order_by('-time')[1:5]

    popular = Article.objects.all().order_by('-likes')[1:5]
    trending = Article.objects.all().order_by('-comment')[1:5]
   

    catergories = Category.objects.all()

    articles = Article.objects.all()

    paginator = Paginator(articles, 8) 

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'first':first,
        'last_post':last_post,
        'recent':recent,
        'recent_more':recent_more,
        'popular':popular,
        'categories':catergories,
        'posts':posts,
        'trending':trending
    }
    return render(request,'blog/index.html',context)


def search(request):

    search = request.GET.get('q')

    if search:
        result = Article.objects.filter(
            Q(title__icontains=search)
        )

    return render(request,'blog/search.html',{'result':result})


def category(request,id):
    article = Article.objects.filter(pk=id)
    
    for p in article:
        cat = p.category
    
    print(cat)

    post = Article.objects.filter(category=cat)

    return render(request,'blog/category.html',{'post':post})

def blog_details(request,id):
    post = get_object_or_404(Article,pk=id)
    related = Article.objects.filter(category = post.category).exclude(id=id)[:4]
    comments = Comment.objects.filter(post=post,reply=None).order_by('-id')
    is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        is_liked = True


    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = request.POST.get('comment')
        reply_id = request.POST.get('comment_id')
        cmnts = None
        if reply_id:
            cmnts = Comment.objects.get(id=reply_id)
        comment = Comment.objects.create(post=post,name=request.user,comment=comment,reply = cmnts)
        comment.save()

        form=CommentForm()
    
        

    context = {
        'post':post,
        'related_post':related,
        'form':form,
        'comments':comments,
        'is_liked':is_liked,
        'total_likes':post.total_likes(),
    }


    return render(request,'blog/blog_detail.html',context)

# def update_comment(rquest,id):

#     comment = Comment.objects.filter(pk=id)
    
#     form = ArticleForm(request.POST,instance=comment)
#     if form.is_valid():
#         form.save()
#         return redirect('/')
#     else:
#         form = ArticleForm()
#     return render(request,'blog/blog_detail.html',{'form':form})


def author(request,name):


    post_author = get_object_or_404(User,username = name)
    auth = get_object_or_404(Author,name=post_author.id)
    post = Article.objects.filter(post_author=auth.id)

    context = {
        'auth':auth,
        'post':post,
    }

    return render(request,'blog/profile.html',context)


@login_required
def create_blog(request):
    form = ArticleForm()

    if request.user.is_authenticated:
        post_user = get_object_or_404(Author,name=request.user.id)

        if post_user:

            if request.method=='POST':

                # print(post_user)
                form = ArticleForm(request.POST or None,request.FILES or None)

                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.post_author = post_user
                    obj.save()
                    return redirect('/')
            return render(request,'blog/create_blog.html',{'form':form})
        else:
            return render(request,'blog/author.html')
    else:
        return redirect('login')


# def categoryView(request,name):
#     return render(request,'blog/category.html')


def like_post(request):
    post = get_object_or_404(Article,id=request.POST.get('post_id'))
    is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked = True 
    return HttpResponseRedirect(post.get_absolute_url())


def update_article(request,id):

    article = Article.objects.get(id=id)
    form = ArticleForm(instance=article)

    if request.method=='POST':
        form = ArticleForm(request.POST,instance=article)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = ArticleForm()

    return render (request,'blog/update.html',{'form':form})

  
def delete(request,id):
    article = Article.objects.get(id=id)
    if request.method=='POST':
        article.delete()
        return redirect('/')
    return render(request,'blog/delete.html',{'post':article})



def register(request):

    if request.method=='POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password == confirm:

            if len(password) >=8:

                if User.objects.filter(username=username).exists():
                    messages.warning(request,"username already taken!")
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,"Email alreay registered!")
                    return redirect('register')
                else:

                    user = User.objects.create_user(first_name=name,username=username,email=email,password=password)

                    user.save()
                    return redirect('login')
            else:
                messages.warning("Password length must 8 or more!")
                return redirect('register')
        else:
            messages.warning(request,"password is not matching!")
            return redirect('register')
    else:

        return render(request,'blog/register.html')


def login_user(request):
    user = None
    if request.method=='POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request,username=username,password=password)
        if user is not None:    
            login(request,user)
            u = get_object_or_404(User,id=request.user.id)
            author = Author.objects.filter(name=u.id)

            if author:
                return redirect('/')
                print("Login success")
            else:

                form = AuthorForm(request.POST or None,request.FILES or None)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.name = user
                    obj.save()
                    
                return render(request,'blog/author.html',{'form':form})
        


    return render(request,'blog/login.html',{'user':user})

def logout_user(request):
    
    logout(request)
    return redirect('/')