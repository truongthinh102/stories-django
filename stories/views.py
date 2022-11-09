
from email import message
from django.shortcuts import render
from django.http import HttpResponse, response
from django.core.paginator import Paginator
from stories.forms import *
from MyNews.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMultiAlternatives
import feedparser
import re

from stories.models import Story, Category, Contact


# Create your views here.


def index(request):
    stories = Story.objects.order_by('-public_day')
    newest_1 = stories[0]
    new_4 = stories[1:5]
    young_stories = Story.objects.filter(category=1).order_by('-public_day')
    older_stories = Story.objects.filter(category=2).order_by('-public_day')
    categories = Category.objects.all()

    most_popular = stories[:4]

    return render(request, 'stories/index.html', {
        'newest_1': newest_1,
        'new_4': new_4,
        'young_stories': young_stories,
        'older_stories': older_stories,
        'categories': categories,
        'most_popular': most_popular,
    })

def index_2(request):
    stories = Story.objects.order_by('-public_day')
    newest_1 = stories[0]
    new_4 = stories[1:5]
    young_stories = Story.objects.filter(category=1).order_by('-public_day')
    older_stories = Story.objects.filter(category=2).order_by('-public_day')
    categories = Category.objects.all()

    # Test cookies
    value = 1

    if request.COOKIES.get('visits'):
        value = int(request.COOKIES.get('visits'))

    response = render(request, 'stories/index.html', {
        'newest_1': newest_1,
        'new_4': new_4,
        'young_stories': young_stories,
        'older_stories': older_stories,
        'categories': categories,
        'visits': value,
    })

    response.set_cookie('visits', value + 1)

    return response

def category(request, pk):
    stories = Story.objects.filter(category=pk).order_by('-public_day')
    new_stories = stories[0:6]

    #Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(stories, 4)
    stories_pager = paginator.page(page)
    
    return render(request, 'stories/category.html', {
        'stories': stories_pager,
        'pk': pk,
        'new_stories': new_stories,
    })

def story(request, pk):
    story = Story.objects.get(pk=pk)
    stories = Story.objects.order_by('-public_day')
    new_stories = stories[0:6]
    return render(request, 'stories/story.html', {
        'story': story,
        'new_stories': new_stories,
    })

def contact(request):
    result = ''
    if request.POST.get('btnSendMessage'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact_info = Contact(name=name, email=email, subject=subject, message=message)
        contact_info.save()

        # Gửi mail
        # noidung = 'Chào bạn ' + name + '. Chúng tôi đã nhận được thông tin phản hồi của bạn với nội dung "' + message + '"'
        # send_mail(subject, noidung, EMAIL_HOST_USER, [email, 'thinh.phamtruong102@gmail.com'])

        noi_dung = '<p>Chào bạn <b>' + name + '</b>,</p>'
        noi_dung += '<p>Chúng tôi đã nhận được thông tin phản hồi từ bạn với nội dung: <b><i>"' + message + '"</i></b></p>'
        noi_dung += '<p>Chúng tôi sẽ phản hồi trong thời gian sớm nhất</p>'

        msg = EmailMultiAlternatives(subject, noi_dung, EMAIL_HOST_USER, [email])
        msg.attach_alternative(noi_dung, 'text/html')
        msg.send()

        result = '''
        <div class="alert alert-success" role="alert">
            Successfully! Your feedback has been sent !
        </div>
        '''

    return render(request, 'stories/contact.html',{
        'result': result,
    })

def contact_with_form(request):
    result = ''
    form = FormContact()
    if request.POST.get('btnSendMessage'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()

            result = '''
        <div class="alert alert-success" role="alert">
            Successfully! Your feedback has been sent !
        </div>
        '''

    return render(request, 'stories/contact_with_form.html',{
        'result': result,
        'form': form,
    })

def search(request):
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword')

        # Tìm kiếm từ khóa theo tiêu đề (name)
        # keyword_search = Story.objects.filter(name__contains=keyword).order_by('-public_day')

        # Tìm kiếm từ khóa theo tiêu đề và nội dung (name and content)
        stories = Story.objects.all().values() #show ra toàn bộ thuộc tính(cột) trong đối tượng
        list_stories = list(stories)
        id_stories = []
        for story in list_stories:
            story['content'] = re.sub(r'<[^<]+?>', '', story['content']) # Loại bỏ thẻ HTML trong nội dung
            if keyword.lower() in story['name'].lower() or keyword.lower() in story['content'].lower():
                id_stories.append(story['id'])

        keyword_search = Story.objects.filter(id__in=id_stories).order_by('-public_day')

        page = request.GET.get('page', 1)
        paginator = Paginator(keyword_search, 4)
        search_pager = paginator.page(page)

    return render(request, 'stories/category.html', {
        'stories': search_pager,
        'total_stories_search': keyword_search,
    })

def read_rss(request):
    news_feed = feedparser.parse('http://feeds.feedburner.com/bedtimeshortstories/LYCF')
    # print(news_feed)
    # entry = news_feed.entries[0]
    # print(entry.keys())

    entries = news_feed.entries

    return render(request, 'stories/rss.html', {
        'entries': entries,
    })