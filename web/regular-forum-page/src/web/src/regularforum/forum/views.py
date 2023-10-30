from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.utils import timezone

from ratelimit.decorators import ratelimit

from .models import ForumTopic, ForumText
from .filter import filterText

class IndexView(generic.ListView):
    template_name = "forum/index.html"
    context_object_name = "forums"

    def get_queryset(self):
        if (self.request.user.is_authenticated):
            if (self.request.user in Group.objects.get(name="moderators").user_set.all()):
                return ForumTopic.objects.order_by('-pub_date')
            else:
                user_forums = ForumTopic.objects.filter(user=self.request.user)
                return user_forums.order_by('-pub_date')
        else:
            return ForumTopic.objects.none()

def signUp_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('index'))
    else:
        form = UserCreationForm()
    return render(request, 'forum/signup.html', {'form': form})

def login_view(request):
    if (request.user.is_authenticated):
        return redirect(reverse('index'))
    elif (request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if (user is not None):
            login(request, user)
            return redirect(reverse('index'))
        else:
            return redirect(reverse('login'))
    else: 
        return render(request, 'forum/login.html')

def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

@login_required(login_url='/login')
def viewForum(request, forumid):
    forum = get_object_or_404(ForumTopic, pk=forumid)
    if (forum.user == request.user or request.user in Group.objects.get(name="moderators").user_set.all()):
        return render(request, 'forum/view.html', {'forumtopic' : forum})
    else:
        return HttpResponseForbidden("Forbidden")

@login_required(login_url='/login')
@ratelimit(key="user", rate="1/m", method="POST", block=False)
def createForum(request):
    if (request.method == "POST"):
        if (request.limited):
            return render(request, 'forum/create.html', {'limited' : True})
        try:
            title = request.POST['title']
            text = filterText(request.POST['forumText'])
            forum = ForumTopic(topicTitle=title, user=request.user, pub_date=timezone.now())
            forum.save()
            forumText = ForumText(textTitle=title, forumText=text, forumTopic=forum, user=request.user)
            forumText.save()
        except(KeyError):
            return HttpResponseBadRequest("Bad Request")
        except:
            return HttpResponseServerError("Internal Error")
        else:
            return redirect(reverse("viewForum", args=(forum.id,)))
    else:
        return render(request, 'forum/create.html', {'limited' : False})

@login_required(login_url='/login')
@ratelimit(key="user", rate="1/m", method="POST", block=False)
def writeForum(request, forumid):
    forum = get_object_or_404(ForumTopic, pk=forumid)
    if (request.user != forum.user and not request.user in Group.objects.get(name="moderators").user_set.all()):
        return HttpResponseForbidden("Forbidden")
    if (request.user in Group.objects.get(name="moderators").user_set.all() and len(forum.forumtext_set.filter(user=request.user)) >= 1):
        # Avoid unlimited spam caused by xss
        return redirect(reverse('index'))
    if (request.limited):
        return redirect(reverse('viewForum', args=(forum.id,)))
    try:
        text = filterText(request.POST["forumText"])
        forumtext = ForumText(textTitle=request.POST["title"], forumText=text, forumTopic=forum, user=request.user)
        forumtext.save()
    except (KeyError):
        return HttpResponseBadRequest("Bad Request")
    except:
        return HttpResponseServerError("Internal Error")
    else:
        return redirect(reverse('viewForum', args=(forum.id,)))
