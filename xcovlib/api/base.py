# -*- coding: utf-8 -*-
"""Contains a base model class, the subclasses of which represent
models on the xCover core.

The BaseModel class works as a framework for performing all necessary
CRUD operations for its subclasses. The subclasses typically only need
to define a set of configuration parameters (such as the expected fields
for retrieving objects, or the parameters that can be modified on an object).
For any custom functionality, subclasses may have to add override existing
functions.

Examples:
The examples below do not handle exceptions. You can find more detailed
examples in the README.

# Retrieve object
>>> obj = MyModel.get(attr1='value1', attr2='value2')

# Create object
>>> obj = MyModel(attr1='value1', attr2='value2')
>>> obj.save(
>>>     param1='...',
>>>     param2='...',
>>>     extra_param='...',
>>> )
>>> # Alternatively:
>>> obj = MyModel(attr1='value1', attr2='value2')
>>> obj.param1 = '...'
>>> obj.param2 = '...'
>>> obj.extra_param = '...'
>>> obj.save()

# Update object
>>> obj = MyModel.get(attr1='value1', attr2='value2')
>>> obj.save(
>>>     param1='...',
>>>     param2='...',
>>> )
>>> # Alternatively
>>> obj = MyModel.get(attr1='value1', attr2='value2')
>>> obj.param1 = '...'
>>> obj.param2 = '...'
>>> obj.save()


WARNING:
__getattr__ and @property do not mix well and at some point all @property
decorators were removed from BaseModel.

This note is here to warn developers to not add any properties in the future.

The issue is that, if a property raises an AttributeError, Python
(__getattribute__()) falls back to using __getattr__(). The problem is
that the traceback is lost, which makes it extremely hard to debug,
since the actual exception raised isn't shown anywhere.
"""


import json
import decimal
from xcovlib.registry import registry


# Used for designating what type of attribute is missing
ATTR_TYPE_READ = 'read'
ATTR_TYPE_WRITE = 'write'
ATTR_TYPE_URL = 'url'


class BaseModel():
    """Base class for xCover models.

    Each model has a list of fields. The model works as a proxy between the
    local application and the remote xCover server.

    The user of the class can:
      a) retrieve an existing remote instance of the model
         by using the static method `MyModel.get(...)`
      b) create a new local instance with a set of populated fields
         and call `save()` in order to save it to the remote server
    """

    # The URI prefix of all API endpoints for this model
    _prefix = ''

    # The URI for retrieving a collection of multiple items
    # (shouldn't start with a slash)
    _path_to_collection = ''

    # The URl for retrieving a single item
    # (shouldn't start with a slash)
    _path_to_item = ''

    # All fields defined here will be used for constructing
    # the URL of the request
    url_fields = set()


    # Initially False, set to True when an instance of the class is created
    _is_initialized = False

    @classmethod
    def get(cls, **kwargs):
        """Retrieve an object by making a GET request to xCover.

        Each value in `kwargs` that corresponds to a field
        defined in the xCover API Docs will be used in the URL path
        of the request, so that a particular entry of this model
        is identified and retrieved. For JSON Fields, pass the value as a
        dict

        Raises:
            xcovlib.http.exceptions.NotFoundError: if the object with these
                attributes is not found on the remote server
            xcovlib.http.exceptions.ServerError subclass: depending on
                the particular server response

        Example:
        # Note: also catch exceptions
        >>> obj = MyModel.get(attr1=value1, attr2=value2)
        """
        fields = {}
        for field in cls.url_fields:
            value = kwargs.pop(field, None)
            fields[field] = value

        # Create an instance of the model class and make the GET request
        model = cls(**fields)
        model._populate(**kwargs)
        return model

    def __init__(self, prefix='/api/v2/', **url_values):
        """Constructor.

        Initializes various variables, setup the HTTP handler and
        stores all values

        Args:
            prefix: The prefix of the urls.
            url_parameters: The parameters that are passed in the URL
        Raises:
            AttributeError: if not all values for parameters in `url_fields`
                are passed
        """
        self._http = registry.http_handler
        self._prefix = prefix
        self._modified_fields = {}
        self._populated_fields = {}

        for field in url_values:
            if field in self.url_fields:
                setattr(self, field, url_values[field])

        self._is_initialized = True

    def __getattr__(self, name, default=None):
        """Return the value of the field with the given name.

        Looks in `self._modified_fields` and `self._populated_fields`.

        Raises:
            AttributeError: if the requested attribute does not exist
        """
        if name in self._modified_fields:
            return self._modified_fields[name]

        if name in self._populated_fields:
            return self._populated_fields[name]


    def __setattr__(self, name, value):
        """Set the value of a field."""
        # If __init__() hasn't finished yet, accept anything
        if ('_is_initialized' not in self.__dict__) or (name in self.__dict__):
            return super(BaseModel, self).__setattr__(name, value)

        self._modified_fields[name] = value

    def set_values(self, response):
        if type(response) == dict:
            for key, value in response.items():
                self.__setattr__(key, value)
        else:
            for key, value in json.loads(response, parse_float=decimal.Decimal).items():
                self.__setattr__(key, value)

    def save(self, **fields):
        """Save the instance to the xCover server.

        If it was pre-populated, it updates the instance on the server,
        otherwise it creates a new object.

        Any values given in `fields` will be attempted to be saved
        on the object. The same goes for any other values already set
        to the object by `model_instance.attr = value`.
        """
        for field in fields:
            setattr(self, field, fields[field])

        if self._populated_fields:
            self._update(**self._modified_fields)
        else:
            self._create(**self._modified_fields)

    def _populate(self, **kwargs):
        """Populate the instance with the values from the server."""
        self._populated_fields = self._get(**kwargs)

    def _get(self, query_params=dict(), **kwargs):
        """Get the resource from xCover."""
        path = self._construct_path_to_item(query_params)
        return self._http.get(path)

    def _create(self, query_params=dict(), **kwargs):
        """Create a resource in the xCover."""
        path = self._construct_path_to_collection(query_params)
        return self._http.post(path, json.dumps(kwargs))

    def _update(self, query_params=dict(), **kwargs):
        """Update a resource."""
        path = self._construct_path_to_item(query_params)
        if not kwargs:
            return
        return self._http.put(path, json.dumps(kwargs))

    def _patch(self, query_params=dict(), **kwargs):
        """Patch a resource."""
        path = self._construct_path_to_item(query_params)
        if not kwargs:
            return
        return self._http.patch(path, json.dumps(kwargs))

    def _construct_path_to_collection(self, query_params):
        """Construct the path to an actual collection."""
        template = self.get_path_to_collection_template()  # flake8 fix
        path = template % self.get_url_parameters()
        if query_params:
            query_params = '&'.join(["{}={}".format(key, value) for key, value in query_params.items()])
            return '?'.join([path, query_params])
        return path

    def _construct_path_to_item(self, query_params):
        """Construct the path to an actual item."""
        path = self.get_path_to_item_template() % self.get_url_parameters()
        if query_params:
            query_params = '&'.join(["{}={}".format(key, value) for key, value in query_params.items()])
            return '?'.join([path, query_params])
        return path

    def get_url_parameters(self):
        """Create a dictionary of parameters used in URLs for this model."""
        url_fields = {}
        for field in self.url_fields:
            url_fields[field] = getattr(self, field)
        return url_fields

    def get_path_to_collection_template(self):
        """The URL to access the collection of the model."""
        return self._join_subpaths(self._prefix, self._path_to_collection)

    def get_path_to_item_template(self):
        """The URL to access a specific item of the model."""
        return self._join_subpaths(self._prefix, self._path_to_item)

    def _join_subpaths(self, *args):
        """Join subpaths (given as arguments) to form a
        well-defined URL path.
        """
        return '/'.join(args).replace('///', '/').replace('//', '/')
