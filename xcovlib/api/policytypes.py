import json
from .base import BaseModel


class PolicyTypes(BaseModel):
    """
    Base Class for PolicyTypes Model as described in the documentation for xCover Admin API Only.

    To use this method, you have to use key and secret which works with Admin
    """
    _path_to_collection = 'policytypes/'
    _path_to_item = 'policytypes/'

    def __str__(self):
        return '[Policies Object]'

    @classmethod
    def get_policies(cls, **kwargs):
        """
        Get the Booking details when the Quote Package ID and Project ID is provided

        :param Partner ID: The ID of the Partner under which the booking exists
        :param Quote Package ID: The ID of the Quote Package

        """
        policy_types = super().get(**kwargs)
        return policy_types
