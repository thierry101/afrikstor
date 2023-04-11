from rest_framework import permissions
from authentication.api.serializers import UserSerializer


class AdminPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        data = UserSerializer(request.user).data
        admin = data['role'] == 'Admin' or data['role'] == 'Root'
        read = data['role'] == 'Validator' or data['role'] == 'Viewer' or data['role'] == 'Seller'
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'GET' or request.method == 'DELETE':
            return admin
        else:
            return read


class ValidatorsPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        data = UserSerializer(request.user).data
        validator = data['role'] == 'Admin' or data['role'] == 'Root' or data['role'] == 'Validator'
        read = data['role'] == 'Viewer'
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'GET' or request.method == 'DELETE':
            return validator
        else:
            return read


class ProvidersPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        data = UserSerializer(request.user).data
        provider = data['role'] == 'Vendeur' or data['role'] == 'vendeur' or data['role'] == 'seller' or data['role'] == 'Seller'
        read = data['role'] == 'Viewer'
        if request.method == 'POST' or request.method == 'PUT' or request.method == 'GET' or request.method == 'DELETE':
            return provider
        else:
            return read


class IsOwnerOrReadOnly(permissions.BasePermission):

    # for view permission
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    # for object level permissions
    def has_object_permission(self, request, view, vacation_obj):
        return vacation_obj.owner.id == request.user.id
