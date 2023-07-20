from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User, auth
from .models  import *
from .forms import *
from math import ceil
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# Create your views here.


def Home(request):

    if   request.user.is_authenticated:
        return redirect('dashboard')

    else:
        allnews= latest_news.objects.all().order_by('-date').exclude(delete_status='deleted')
        main_cat=Main_category.objects.all()
        new_news= allnews.filter(status='New').exclude(show_front='Dont Show')
        for news in new_news:
            if news.details:
                news.details=re.compile(r'<[^>]+>').sub('', news.details)
                news.details=re.sub("&nbsp;", " ", news.details)
        new1=new_news.first()
        new3=new_news[1:4]

        trending= allnews.filter(status='Trending')
        for news in trending:
            if news.details:
                news.details = re.compile(r'<[^>]+>').sub('', news.details)
                news.details=re.sub("&nbsp;", " ", news.details)
        allvideos=Videos.objects.all().order_by('-date')
        vid1=allvideos.first()
        vid3=allvideos[1:4]


        n= len(allnews)
        nSlides= n//4 + ceil((n/4)-(n//4))
        params = {'no_of_slides':nSlides, 'range': range(1,nSlides),
        'product': allnews,'allnews':allnews,'new1':new1,'new3':new3,
        'main_cat':main_cat,'vid1':vid1,'vid3':vid3, 'trending':trending}

        return render(request,'index.html', params)
import re
import html
def detail(request,slug):
    main_cat=Main_category.objects.all()
    allnews= latest_news.objects.all().order_by('-date').exclude(delete_status='deleted')
    news=latest_news.objects.get(slug=slug)
    author_news=allnews.filter(author=news.author).exclude(slug=slug)[:4]
    new_news= allnews.filter(status='New').exclude(slug=slug)[:3]
    news.details=html.unescape(news.details)
    print(news.details)
    # if news.details:
    #     news.details=re.compile(r'<[^>]+>').sub('', news.details)
    #     news.details=re.sub("&nbsp;", " ", news.details)
    # if news.img2_details:
    #     news.img2_details = re.compile(r'<[^>]+>').sub('', news.img2_details)
    #     news.img2_details=re.sub("&nbsp;", " ", news.img2_details)
    # if news.img3_details:
    #     news.img3_details = re.compile(r'<[^>]+>').sub('', news.img3_details)
    #     news.img3_details=re.sub("&nbsp;", " ", news.img3_details)
    # author_news=re.compile(r'<[^>]+>').sub('', author_news)
    # new_news=re.compile(r'<[^>]+>').sub('', new_news)
    context={'allnews':allnews,'author_news':author_news,'news':news,'new_news':new_news,'main_cat':main_cat}
    return render(request,'detail.html',context)


def status_news(request,str):
    main_cat=Main_category.objects.all()
    allnews= latest_news.objects.all().order_by('-date').exclude(delete_status='deleted')
    news_list=allnews.filter(status=str)
    context={'allnews':allnews,'news_list':news_list,'str':str,'main_cat':main_cat}

    return render(request,'status.html',context)

def main_category(request,str):
    main_cat=Main_category.objects.all()
    main_category=main_cat.get(title=str)
    allnews= latest_news.objects.all().exclude(delete_status='deleted')
    news_list=Category.objects.filter(main_category=main_category)

    context={'allnews':allnews,'news_list':news_list,'str':str,'main_cat':main_cat}

    return render(request,'main_category.html',context)

def category(request,str):
    main_cat=Main_category.objects.all()
    category=Category.objects.get(title=str)
    allnews= latest_news.objects.all().exclude(delete_status='deleted')
    news_list=allnews.filter(category=category)
    context={'allnews':allnews,'news_list':news_list,'str':str,'main_cat':main_cat}

    return render(request,'category.html',context)

def donate(request):
    main_cat=Main_category.objects.all()
    thank=False
    if request.method=="POST":
        first_name = request.POST.get('first_name', '')
        duration = str(request.POST.get('options1'))
        amount = request.POST.get('amount')
        if amount == 'other':
            amount=request.POST.get('amt','')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone1 = str(request.POST.get('phone', ''))
        phone='+91 ' + phone1
        

        try:
            Donation.objects.create(first_name=first_name,last_name=last_name,duration=duration,
            amount=int(amount),email=email,phone=phone)
            thank=True
        
        except:
            print('error submiting')

    return render(request,'donate.html',{'main_cat':main_cat,'thank':thank})


def Login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
       if request.method=="POST":
        name=request.POST.get('username')
        pwd=request.POST.get('password')

        user=authenticate(request,username=name,password=pwd)

        if user is not None:
                login(request,user)
                return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def search(request):
    
    main_cat=Main_category.objects.all()
    allnews= latest_news.objects.all().exclude(delete_status='deleted')

       
    squery= request.GET.get('search1')
    

    if(squery == '' ):
        squery=0
    
    try:
        news_list=allnews.filter(title__icontains=squery) or allnews.filter(author__icontains=squery)  or allnews.filter(category__icontains=squery) 
    except:
        news_list=None

    context={'news_list':news_list,'str':'Search Result','main_cat':main_cat}
    return render(request,'status.html',context)



@login_required(login_url='login')
def Admin_panel(request):
    allnews= latest_news.objects.all().order_by('-date').exclude(delete_status='deleted')
    navbar = 'dashboard'

    today=datetime.today().date()
    news_today=allnews.filter(date__icontains=today).count()
    total_news=allnews.count()

    donations=Donation.objects.all()

    earn_month=donations.filter(date__icontains=today.strftime("%Y-%m"))
    Earning_monthly=earn_month.aggregate(Sum('amount'))['amount__sum']
    
    earn_year=donations.filter(date__icontains=today.strftime("%Y"))
    Earning_yearly=earn_year.aggregate(Sum('amount'))['amount__sum']

    once=donations.filter(duration='Once').count()
    monthly=donations.filter(duration='Monthly').count()
    yearly=donations.filter(duration='Yearly').count()

    main_cat=Main_category.objects.all().count()
    sub_cat=Category.objects.all().count()

    ylinks=Videos.objects.all().count()

    context={'allnews':allnews,'navbar':navbar,'total_news':total_news,'news_today':news_today,'once':once,
    'monthly':monthly,'yearly':yearly,'Earning_monthly':Earning_monthly,'Earning_yearly':Earning_yearly,'main_cat':main_cat
    ,'sub_cat':sub_cat,'ylinks':ylinks}

    return render(request,'for_admin/admin_panel.html',context)

@login_required(login_url='login')
def Admin_news(request):
    user=request.user
    allnews= latest_news.objects.all().order_by('-date').exclude(delete_status='deleted')
    navbar = 'news'


    form = AddNewsForm()


    if request.method == 'POST':
        form = AddNewsForm(request.POST,instance=user)
        
        if form.is_valid():
            print('valid')


    context={'allnews':allnews,'navbar':navbar,'form':form}
    return render(request,'for_admin/admin_news.html',context)

@login_required(login_url='login')

def delNews(request,slug):

    ednews=latest_news.objects.get(slug=slug)
    ednews.delete_status='deleted'
    ednews.save()

    return redirect('admin_news')

@login_required(login_url='login')

def delMainCat(request,title):

    edcat=Main_category.objects.filter(title=title).delete()
    # edcat.delete_status='deleted'
    # edcat.save()

    return redirect('admin_category')


@login_required(login_url='login')

def delCat(request,title):

    edcat=Category.objects.filter(title=title).delete()
    # edcat.delete_status='deleted'
    # edcat.save()

    return redirect('admin_category')

@login_required(login_url='login')

def AddNews(request):

    page_title='Add News'
    navbar = 'news'
    saveform=False
    ret_url='admin_news'
    form = AddNewsForm()


    if request.method == 'POST':
        form = AddNewsForm(request.POST,request.FILES)
        
        if form.is_valid():

            form.save()
            saveform=True

    context={'navbar':navbar,'form':form,'saveform':saveform,'page_title':page_title,'ret_url':ret_url}
    return render(request,'for_admin/edit_page.html',context)

@login_required(login_url='login')

def editNews(request,slug):

    page_title='Edit News'
    navbar = 'news'
    ret_url='admin_news'
    ednews=latest_news.objects.get(slug=slug)
    saveform=False
    form = AddNewsForm(instance=ednews)


    if request.method == 'POST':
        form = AddNewsForm(request.POST,request.FILES,instance=ednews)
       
        if form.is_valid():

            form.save()
            saveform=True

   

    context={'navbar':navbar, 'form':form,'saveform':saveform,'page_title':page_title,'ret_url':ret_url}
    return render(request,'for_admin/edit_page.html',context)


def register(request):
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     email = request.POST['email']
    #     password1 = request.POST['password1']
    #     passwrod2 = request.POST['password1']

    #     user = User.objects.create_user(username=username, email=email, password=password1)
    #     user.save()
    #     print('user created.')
    #     return redirect('/')
    # else: 
    return render(request,'register.html')


@login_required(login_url='login')
def Admin_category(request):

    main_cat= Main_category.objects.all().order_by('title')
    sub_cat= Category.objects.all()
    navbar = 'category'

    context={'main_cat':main_cat,'navbar':navbar,'sub_cat':sub_cat}
    return render(request,'for_admin/admin_category.html',context)

@login_required(login_url='login')

def AddCategory(request,main):


    mc=Main_category.objects.get(title=main)
    navbar = 'category'
    saveform=False
    page_title='Add Category'
    ret_url='admin_category'
    form = CategoryForm(initial={'main_category':mc})

    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            saveform=True

    context={'navbar':navbar,'form':form,'saveform':saveform,'page_title':page_title,'ret_url':ret_url}
    return render(request,'for_admin/edit_page.html',context)


@login_required(login_url='login')

def AddMainCategory(request):

    navbar = 'category'
    saveform=False
    page_title='Add Main Category'
    ret_url='admin_category'
    form = MainCategoryForm()

    if request.method == 'POST':
        form = MainCategoryForm(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            saveform=True

    context={'navbar':navbar,'form':form,'saveform':saveform,'page_title':page_title,'ret_url':ret_url}
    return render(request,'for_admin/edit_page.html',context)


@login_required(login_url='login')

def editMainCategory(request,title):

    navbar = 'category'
    page_title='Edit Main Category'
    edcat=Main_category.objects.get(title=title)
    saveform=False
    form = MainCategoryForm(instance=edcat)
    ret_url='admin_category'

    if request.method == 'POST':
        form = MainCategoryForm(request.POST,request.FILES,instance=edcat)
        
        if form.is_valid():

            form.save()
            saveform=True

    context={'navbar':navbar, 'form':form,'saveform':saveform,'page_title':page_title,'ret_url':ret_url}
    return render(request,'for_admin/edit_page.html',context)

@login_required(login_url='login')

def editCategory(request,title):

    navbar = 'news'
    page_title='Edit Category'
    edcat=Category.objects.get(title=title)
    saveform=False
    form = CategoryForm(instance=edcat)
    ret_url='admin_category'

    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES,instance=edcat)
        
        if form.is_valid():

            form.save()
            saveform=True

    context={'navbar':navbar, 'form':form,'saveform':saveform,'page_title':page_title,'ret_url':ret_url}
    return render(request,'for_admin/edit_page.html',context)



@login_required(login_url='login')

def Admin_Videos(request):

    videos= Videos.objects.all().order_by('-date')
    navbar = 'videos'

    context={'navbar':navbar,'videos':videos}
    return render(request,'for_admin/admin_videos.html',context)


@login_required(login_url='login')

def delVideos(request,id):

    edcat=Videos.objects.get(pk=id)
    edcat.delete()

    return redirect('videos')



@login_required(login_url='login')

def editVideo(request,id):

    vc=Videos.objects.get(pk=id)
    navbar = 'videos'
    saveform=False
    page_title='Edit Video'
    ret_url='videos'
    form = VideosForm(instance=vc)

    if request.method == 'POST':
        form = VideosForm(request.POST,instance=vc)
        
        if form.is_valid():
            form.save()
            saveform=True

    context={'navbar':navbar,'form':form,'saveform':saveform,'page_title':page_title,'ret_url':ret_url}
    return render(request,'for_admin/edit_page.html',context)

@login_required(login_url='login')

def AddVideo(request):

    navbar = 'videos'
    saveform=False
    page_title='Add Video'
    ret_url='videos'
    form = VideosForm()

    if request.method == 'POST':
        form = VideosForm(request.POST)
        
        if form.is_valid():
            form.save()
            saveform=True

    context={'navbar':navbar,'form':form,'saveform':saveform,'page_title':page_title,'ret_url':ret_url}
    return render(request,'for_admin/edit_page.html',context)



@login_required(login_url='login')

def Admin_donation(request):
    alldonate=Donation.objects.all()
    navbar = 'donations'

    context={'navbar':navbar,'alldonate':alldonate}
    return render(request,'for_admin/admin_donation.html',context)