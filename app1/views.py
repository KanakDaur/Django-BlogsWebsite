from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app1.models import post,comment,Profile
from django.urls import reverse_lazy,reverse
from django.core.paginator import Paginator
from django.db.models import Q
from app1.forms import commentform,Usereditform,Profileeditform
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

class homepage_view(ListView):
    model = post
    paginate_by = 5
    template_name = "app1/homepage.html"
    queryset = post.objects.filter(~Q(status = 'draft'))  # show the latest 5 blogs excepting the blogs whose status is draft
    context_object_name = "allblogs"

def allblogs_view(request):
    allblogs_object = post.objects.filter(~Q(status = 'draft')) # show all blogs except the blogs whose status is draft
    paginator = Paginator(allblogs_object,per_page = 10) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/allblogs.html',
    {'allblogs_object':page_obj.object_list, # for pagination
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

# class based view of blogs detail page
'''
class allblogs_detailview(DetailView):
    model = post
'''

# function based view of blogs detail page
def allblogs_detailview(request,id):
    pst = post.objects.get(id=id)
    comments = comment.objects.filter(pst=pst).order_by('-id')
    if request.method == 'POST':
        comment_form = commentform(request.POST)
        if comment_form.is_valid():
            content = request.POST.get('content')
            cmnt = comment.objects.create(pst=pst,user=request.user,content=content)
            cmnt.save()
            return HttpResponseRedirect(reverse('detail',args=[id]))
    else:
        comment_form = commentform()
    return render(request,'app1/post_detail.html',{'pst':pst,'comments':comments,'comment_form':comment_form})


@method_decorator(login_required, name='dispatch')
class postblogs_view(CreateView):
    model = post
    fields = ('title','body','status','category')
    def form_valid(self,form):
        post = form.save(commit = False)
        post.author = self.request.user # to fill author name by default as a logged in user
        post.slug = post.title
        post.save()
        return HttpResponseRedirect('/allblogs')

@login_required
def myblogs_view(request):
    myblog = post.objects.filter(author = request.user,status = 'published') # to get all the data of the current login user
    paginator = Paginator(myblog,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/myblogs.html',
    {'myblog':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

@method_decorator(login_required, name='dispatch')
class update_blogs(UpdateView):
    model = post
    fields = ('title','body','status','category')

@method_decorator(login_required, name='dispatch')
class delete_blogs(DeleteView):
    model = post
    success_url = reverse_lazy('allblogs')

class signupform_view(CreateView):
    model = User
    fields=('username','password','email','first_name','last_name')
    def form_valid(self,form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        # code to send a confirmation mail to the user that thay have been successfully registered (Mail API)
        subject = "BLOGGERS website mail"
        message = "Welcome "+user.username+",you are successfully registered on BLOGGERS"
        recipient_list = [user.email]
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject,message,email_from,recipient_list)
        Profile.objects.create(user = user)
        return HttpResponseRedirect('/accounts/login')

@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = Usereditform(data = request.POST, instance = request.user)
        profile_form = Profileeditform(data = request.POST, instance = request.user.profile,files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return HttpResponseRedirect("/")
    else:
        user_form = Usereditform(instance = request.user)
        profile_form = Profileeditform(instance = request.user.profile)
    return render(request,'app1/edit_profile.html',{'user_form':user_form,'profile_form':profile_form})

@login_required
def draft_view(request):
    draft = post.objects.filter(status__iexact = 'draft',author = request.user)
    return render(request,'app1/draft_blogs.html',{'draft':draft})


# code to make the logged in users able to delete their comment from blog detail page
class comment_delete(DeleteView):
    model = comment
    def get_success_url(self):
        pst = self.object.pst
        return reverse_lazy('detail', kwargs={'id': pst.id})


def sports_category_view(request):
    sport = post.objects.filter(category__iexact="sports blogs",status = 'published')
    paginator = Paginator(sport,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/sports_category.html',
    {'sport':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

def travel_category_view(request):
    travel = post.objects.filter(category__iexact="travel blogs",status = 'published')
    paginator = Paginator(travel,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/travel_category.html',
    {'travel':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

def fashion_category_view(request):
    fashion = post.objects.filter(category__iexact="fashion blogs",status = 'published')
    paginator = Paginator(fashion,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/fashion_category.html',
    {'fashion':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

def food_category_view(request):
    food = post.objects.filter(category__iexact="food blogs",status = 'published')
    paginator = Paginator(food,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/food_category.html',
    {'food':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

def educational_category_view(request):
    education = post.objects.filter(category__iexact="educational blogs",status = 'published')
    paginator = Paginator(education,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/education_category.html',
    {'education':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

def parenting_category_view(request):
    parent = post.objects.filter(category__iexact="parenting blogs",status = 'published')
    paginator = Paginator(parent,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/parent_category.html',
    {'parent':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

def movie_category_view(request):
    movie_music = post.objects.filter(category__iexact="movie and music blogs",status = 'published')
    paginator = Paginator(movie_music,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/movie_music_category.html',
    {'movie_music':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

def personal_category_view(request):
    personal = post.objects.filter(category__iexact="personal blogs",status = 'published')
    paginator = Paginator(personal,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/personal_category.html',
    {'personal':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })

def other_category_view(request):
    other = post.objects.filter(category__iexact="other",status = 'published')
    paginator = Paginator(other,per_page = 5) # for pagination
    page_number = request.GET.get('page',1) # for pagination
    page_obj = paginator.get_page(page_number) # for pagination
    return render(request,'app1/other_category.html',
    {'other':page_obj.object_list,
    'paginator':paginator, # for pagination
    'page_number':int(page_number) # for pagination
    })


# code to publish drafted blogs forcefully from the drfated blogs list
'''
def draft_publish(request,id):
    pub = post.objects.get(id=id)
    pub.status = "published"
    pub.save()
    return render(request,'app1/draft_blogs.html')
'''
