from rest_framework.permissions import BasePermission


class CanAccess(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['accept', 'reject', 'rejected', 'carrier_available', 'carrier_accepted']:
            return request.user.is_carrier
        elif view.action in ['create', 'shipper_available', 'shipper_accepted', 'list']:
            return request.user.is_shipper
        elif view.action in ['available', 'accepted']:
            return True
        return False
