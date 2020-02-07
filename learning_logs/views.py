from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404
# Create your views here.-------------------------------------
def index(request):
    return render(request, 'learning_logs/index.html')
#------------------------------------------------------
@login_required
def topics(request):

    topics=Topic.objects.filter(owner=request.user).order_by('date')
    context={'topics':topics}
    return render(request, 'learning_logs/topics.html', context)
# it shows all entries related to a topic-------------------------------
@login_required
def topic(request,topic_id):

    topic=Topic.objects.get(id=topic_id)
    #check topic belongs to the current user
    check_topic_owner(request.user,topic.owner)
    entries=topic.entry_set.order_by('-date_added')
    context={
    'topic':topic,
    'entries':entries
    }
    return render(request,'learning_logs/topic.html',context)
#to add new topic--------------------------------------------
@login_required
def new_topic(request):
    #default request method is GET and when we try to submit the data on server side then request method "POST" is used
    if request.method !='POST':
        #when data is not submitted, create a blank form
        form= TopicForm()
    else:
        # POST data submitted;
        form= TopicForm(data=request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    #display a blank or invalid form
    context={'form':form}
    return render(request, 'learning_logs/new_topic.html', context)

#to add new entry------------------------------------------
@login_required
def new_entry(request,topic_id):
    topic=Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form=EntryForm()

    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            check_topic_owner(request.user,topic.owner)#--------------------->>>>>>>>>
            new_entry=form.save(commit=False)
            new_entry.owner=request.user
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    #display blank entry form
    context={'topic':topic, 'form':form}
    return render(request,'learning_logs/new_entry.html', context)
# to edit existing entry -----------------------------------------------
@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    check_topic_owner(request.user,topic.owner)
    if request.method != 'POST':
        form=EntryForm(instance=entry)

    else:
        form=EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context= {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)


#_________________________________________
def check_topic_owner(request_user,owner):
    if request_user!=owner:
        raise Http404
