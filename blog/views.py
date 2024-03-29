from django.shortcuts import render,redirect
from django.http import Http404
from .models import Posts
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,JsonResponse
from django.db.models import Count
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.html  import format_html
# from blog.utils import *
# from genai import get_posts
from django.views.decorators.csrf import requires_csrf_token
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage






def home(requests):
 
    posts = Posts.objects.all().order_by('-pub_date')
    most_liked_posts = Posts.objects.annotate(total_likes=Count('post_liked')
                                              ).filter(total_likes__gte = 1).order_by('-total_likes')
    paginate = Paginator(posts,5)
    page = requests.GET.get("page")
    try:
        final_post = paginate.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        final_post = paginate.get_page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        final_post = paginate.get_page(paginate.num_pages)

   

    context = {'posts':final_post,
               'most_liked_posts':most_liked_posts[:5],
               }
    

    return render(requests,'blog/home.html',context=context)

def about(requests):
    return render(requests, 'blog/about.html')

def articles(requests,id,title):
    isLiked = False
    p = Posts.objects.get(pk=id)

    if requests.user.is_authenticated:
        username = requests.user.username
        uid = User.objects.filter(username=username)[0]

        isLiked = bool(p.post_liked.filter(id= uid.id).exists())
    context = {'post':p,
               'isLiked':isLiked,
               'totalLikes':p.total_likes()
               }
    return render(requests,'blog/article.html',context=context)

def contact(requests):
    cont = {'heading': 'Contact Form',}
    return render(requests,'blog/contact.html', context=cont)


def error_404(requests,exception):
    return render(requests,'blog/404.html')

def register_page(requests):
    if requests.user.is_authenticated:
        return redirect("userprofile:user-profile-page")
    if requests.method != 'POST':
        return render(requests,'blog/register.html')
    first_name = requests.POST.get("first_name")
    last_name = requests.POST.get('last_name')
    username = requests.POST.get('username')
    email = requests.POST.get('email')
    password = requests.POST.get('password')


    user = User.objects.filter(username = username)

    if user.exists():
        msg = format_html("<h6>Username Already Taken <a href= '{}'>Login here</a></h6>",reverse('sign-in-user'))
        messages.info(requests, msg)
        return redirect('sign-up-user')

    user = User.objects.create(
        first_name =  first_name.strip(),
        last_name =  last_name.strip(),
        username =  username.strip(),
        email = email,
        # isLiked = False,

    )
    user.set_password(password)
    user.save()

    msg1 = format_html("<h6>User Registered <a href= '{}'>Login here</a></h6>",reverse('sign-in-user'))
    messages.success(requests, msg1)
    return redirect('sign-up-user')


def login_page(requests):

    if requests.method != 'POST':
        return render(requests,'blog/login.html')
    username = requests.POST.get('username')
    password = requests.POST.get('password')

    user = authenticate(username = username, password = password)
    nxt = requests.POST.get('next') or requests.GET.get('next')
    if user is None:
        messages.warning(requests, 'Invalid Username or Password')
        if nxt is None: return redirect('sign-in-user')
        else:
            return redirect(f'{requests.path}?next={nxt}')
    elif user:
        login(requests, user)
        messages.success(requests, "Welcome")


        if nxt:
            print(nxt)
            return redirect(nxt)
        return redirect('blog-home')
    return redirect('blog-home')








@login_required(redirect_field_name=None, login_url='sign-in-user')
def logout_page(requests):
    logout(requests)
    messages.info(requests,'Logged Out')
    return redirect('blog-home')





@requires_csrf_token
def post_liked(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status':401})
    if request.method != "POST":
        return JsonResponse({'status': 0})
    username  = request.POST.get('username')
    pk = request.POST.get('pk')
    post = Posts.objects.get(post_id = int(pk))
    uid = User.objects.get(username=username)
    csr = request.POST.get('csrfmiddlewaretoken')
    if post.post_liked.filter(id = uid.id).exists():
        post.post_liked.remove(uid)
    else:                                  
        post.post_liked.add(uid)
    isLiked = bool(post.post_liked.filter(id= uid.id).exists())
    return JsonResponse({'status':1, 'isLiked' : isLiked})
    # return redirect('article-page',id=pk,title=slugify(post.post_title))

@csrf_exempt
def share_clicked(request):
    print("f------------------function Called()")
    if request.method == "POST":
        username  = request.POST.get('username')
        pk = request.POST.get('pk')
        post = Posts.objects.get(post_id = int(pk))
        uid = User.objects.get(username=username)
        if post.post_liked.filter(id = uid.id).exists():
            post.post_liked.remove(uid)
        else:                                  
            post.post_liked.add(uid)
        isLiked = bool(post.post_liked.filter(id= uid.id).exists())
        return JsonResponse({'status':1, 'isLiked' : isLiked})
    return JsonResponse({'status': 0})


def load_more_posts(requests):
    offset = int(requests.GET.get('offset'))
    limit = 5
    posts = Posts.objects.all()[offset:offset+limit]
    data = [{'id':post.post_id,'title': post.post_title, 'content': post.post_content} for post in posts]
    
    return JsonResponse({'status':1, 'posts' : data})



def search_page(requests):
    if requests.method == "GET":
        if keyword := requests.GET.get('query', ''):
            print("Keyword: ", keyword)
            posts = Posts.objects.filter(post_content__icontains=keyword)
            if posts.exists():
                return render(requests, 'blog/search.html', {'keywords': keyword, 'posts': posts})
    return render(requests, 'blog/search.html')
