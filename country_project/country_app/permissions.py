from rest_framework import permissions

class IsCountryMyUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.my_user == request.user
    
class IsStateMyUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.country.my_user == request.user

class IsCityMyUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.state.country.my_user == request.user

