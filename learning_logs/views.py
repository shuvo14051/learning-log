from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import Topic,Entry
from .forms import TopicForm,EntryForm

def index(request):
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner = request.user)
    context = {'topics':topics,}
    return render(request,'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404('Please add entry to see them.')

    entries = topic.entry_set.all()
    context = {'topic':topic,'entries':entries,}
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():

            # text = form.cleaned_data['text']
            # Topic.objects.create(
            #     text = text
            # ).save()
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            
            return HttpResponseRedirect('/topics/')
    else:
        form = TopicForm()

    context = {'form':form,}
    return render(request,'learning_logs/new_topic.html',context)
    
@login_required   
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method == 'POST':
        # No data submitted; create a blank form.
         
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                        args=[topic_id]))      
    else:
        form = EntryForm() 
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context) 

@login_required
def edit_entry(request,entry_id):
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404('Please add entry to see them.')

    if request.method == 'POST':
        form = EntryForm(instance=entry,data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args = [topic.id]))

    else:
        form = EntryForm(instance=entry) 

    context = {'entry':entry,'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context) 

        



    
