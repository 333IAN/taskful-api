from rest_framework import permissions


class IsAllowedToEditTaskListElseNone(permissions.BasePermission):
    def has_permission(self,request,view):
        if not request.user.is_anonymous:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.user.profile==obj.created_by
    
class IsAllowedToEditTaskElseNone(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.profile.house!=None
        return False
    def has_object_permission(self, request, view, obj):
        return request.user.profile.house==obj.task_list.house
    

class IsAllowedToEditAttachmentElseNone(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        return request.user.profile.house==obj.task.task_list.house
    
