from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    message = "You must be the owner"
    my_safe_method = ['GET', 'POST']
    # def has_permission(self, request, view):
    #     if request.method in self.my_safe_method:
    #         return True
    #     return False    


    def has_object_permission(self, request, view, obj):
        # if request.method in SAFE_METHODS:
        #     return True
        return obj.owner == request.user