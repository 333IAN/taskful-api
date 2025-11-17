from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Task, COMPLETE, NOT_COMPLETE

@receiver(pre_save,sender=Task)
def check_status_change(sender, instance, **kwarges):
    if instance.pk:
        try:
            old_instance=Task.objects.get(pk=instance.pk)
            instance._old_status=old_instance.status
        except Task.DoesNotExist:
            instance._old_status=None
    else:
        instance._old_status=None

@receiver(post_save,sender=Task)
def update_house_points(sender,instance,created,**kwargs):
    "Run only if it is a new task OR if the status has changed"
    if created or (instance._old_status is not None and instance._old_status!=instance.status):
        house=instance.task_list.house
        
        #Logic when tas becomes COMPLETE
        if instance.status==COMPLETE and instance._old_status!=COMPLETE:
            house.points+=10
            house.completed_tasks_count+=1

        #Logic when task becomes NOT_COMPLETE
        elif instance.status==NOT_COMPLETE and instance._old_status==COMPLETE:
            if house.points>=10:
                house.points-=10
            if house.completed_tasks_count>0:
                house.completed_tasks_count-=1
        house.save()

@receiver(post_save,sender=Task)
def update_tasklist_status(sender,instance,created,**kwargs):
    task_list=instance.task_list
    is_complete=True
    for task in task_list.tasks.all():
        if task.status!=COMPLETE:
            is_complete=False
            break
    task_list.status=COMPLETE if is_complete else NOT_COMPLETE
    task_list.save()