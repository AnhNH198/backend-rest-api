from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    # Allow users to update their own profiles

    def has_object_permission(self, request, view, obj):
        """check if user is trying to edit their own profile
        Everytime a request update is made, django will call this function,
        parse argument to this function(request, view, obj)
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        """if the method is safe method(GET) then allow user to send request"""

        return obj.id == request.user.id
        """check if the object they are updating matches their authenticated
        profile that is added to the authentication of the request"""

        """When you authenticate a request in Django rest framework, it will
        assign the authenticated user profile to the request and we can use
        this to compare it to the object that is being updated and make sure
        they have the same ID"""
