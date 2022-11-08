from rest_framework import permissions


class IsOwnerObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:

            return True

        return (
            obj.author.user == request.user
        )  # (True if request.user.id ==  User.objects.get(pk=1) else False)
