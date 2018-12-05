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
    def get_policies(cls, query_params=dict(), **kwargs):
        """
        Get Policies on the System. Admin API Only

        :param query_params: Any parameters you want to pass in the URL
        """
        policy_types = cls(**kwargs)
        response = policy_types._get(query_params, **kwargs)
        policy_types.set_values(response)
        return policy_types
