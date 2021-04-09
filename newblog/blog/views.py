
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, Author
from .forms import*
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.core.paginator import EmptyPage, Paginator,PageNotAnInteger,Page

# Create your views here.


def index(request):

   
    
    result = []
    la = None
    res =[]
    article = Article.objects.all().order_by('-time')
    post = Article.objects.all().order_by('-time')
 
    la = Article.objects.all().order_by('-time')[0]
   
    
    all_post = Paginator(article,5)
    page = request.GET.get('page')

    try:
        article = all_post.page(page)
    except PageNotAnInteger:
        article = all_post.page(1)
    except EmptyPage:
        article = all_post.page(all_post.num_pages)
    for art in article:
        
        if art.id==la.id:
            result.append(art)
        else:
            res.append(art)
            
    return render(request,'blog/index.html',{'article':res,'result':result,'post':post,'latest':la})



def blog_details(request,id):
    detail_post = get_object_or_404(Article,pk=id)

    related = Article.objects.filter(category = detail_post.category).exclude(id=id)[:4]

    return render(request,'blog/blog_detail.html',{'post':detail_post,'related':related})


def author(request,name):
    post_author = get_object_or_404(User,username = name)

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
        user = User.objects.create_user(first_name=name,username=username,email=email,password=password)

        user.save()
        return redirect('login')
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

            
            # return redirect('/')


    return render(request,'blog/login.html',{'user':user})

def logout_user(request):
    
    logout(request)
    return redirect('/')