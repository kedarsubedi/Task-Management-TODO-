from django.shortcuts import render, redirect, get_object_or_404
from . models import TodoLists
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_page')
def todoapp_view(request):
    accuser = request.user
    template_name = "todoapp/index.html"
    todo_id = request.GET.get('todoId', None)
    try:
        if todo_id:
            todo = TodoLists.objects.get(user=accuser, id=todo_id)
        else:
            todo = None
    except:
        todo = None
    if request.method == 'POST':
        task = request.POST['taskfield']
        if task == '':
            messages.warning(request, 'Fields cannot be empty')
        else:
            if TodoLists.objects.filter(user=accuser, tasks=task).exists():
                messages.warning(request, 'Task Already exists')
            else:
                savetask = TodoLists.objects.create(user=accuser ,tasks=task)
                savetask.save()
                messages.success(request, 'Saved Sucessfully')
    
    # Pagination Stuff
    listasks = TodoLists.objects.filter(user=accuser).order_by('-id')
    if not listasks:
        messages.info(request, 'No tasks to display')
        context = {'todo':todo}
        return render(request, template_name, context)
    paginator = Paginator(listasks,3)

    try:
        tasklistfinal = paginator.page(request.GET.get('page'))
    except PageNotAnInteger:
        tasklistfinal = paginator.page(1)
    except EmptyPage:
        tasklistfinal= paginator.page(paginator.num_pages)
        messages.warning(request,'Page doesnot exist')
    lasttask = tasklistfinal.paginator.num_pages
    context = {
        'listasks':tasklistfinal,
        'todo':todo,
        'lastpage': lasttask,
        'totalTask':[n+1 for n in range(lasttask)],
    }
    
    return render(request, template_name, context)

@login_required(login_url='login_page')
def update_todo(request, id):
    todo = get_object_or_404(TodoLists ,id=id)
    if not request.user!=todo:
        messages.warning(request, "Not Authorized to edit this task!")
    if request.method == "POST":
        task = request.POST.get('taskfield')
        if task == '':
            messages.warning(request, 'Fields cannot be empty')
        else:
            todo.tasks = task
            todo.save()
            messages.success(request, 'Updated Successfully')
        return redirect('todoapp_view')
    else:
        # return redirect('todoapp_view')
        pass

@login_required(login_url='login_page')
def todo_delete(request, id):
    taskdel = get_object_or_404(TodoLists, id=id)
    if not request.user!=taskdel:
        messages.warning(request, "You are not authorized to delete!")
        return redirect('todoapp_view')
    if request.method=='POST':
        taskdel.delete()
        messages.success(request, "Task Deleted Successfully!")
    else:
        messages.warning(request, "Request method is not allowed")
    return redirect('todoapp_view')
