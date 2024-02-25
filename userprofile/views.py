from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from blog.models  import Posts,User

# Create your views here.

# @login_required(login_url='sign-in-user')
# def user_profile(requests):
#     uname= requests.user.username
#     uid = User.objects.filter(username=uname)[0]
#     p = Posts.post_liked.through.objects.filter(user_id=uid.id)
#     post = Posts.objects.filter(post_id__in=[i.posts_id for i in p]).values()
#     # print("user__id -------> ",post)
#     contxt = {'posts':post}


#     return render(requests,'users/profile.html',context=contxt)
    
from django.shortcuts import get_object_or_404
@login_required(login_url='sign-in-user')
def user_profile(request):
    user = get_object_or_404(User, username=request.user.username)
    uname = user.username  # Store username for later use if needed
    p = Posts.post_liked.through.objects.filter(user_id=user.id)
    post_ids = [i.posts_id for i in p]
    post = Posts.objects.filter(post_id__in=post_ids)  # Filter posts using collected IDs

    context = {'posts': post.order_by('-post_id')}
    return render(request, 'users/profile.html', context=context)