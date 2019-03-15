from xcovlib.http.auth import SignatureAuth
from xcovlib.http.http_requests import HttpRequest
from xcovlib.registry import registry
from xcovlib.api.quotes import Quote
from xcovlib.api.bookings import Bookings
from xcovlib.api.renewals import Renewal
from xcovlib.api.policytypes import PolicyTypes


class Client:
    """
    Base Class which lets you access the xCover-Core Client
    and make requests to the service.

    >>> client = Client(host=host, key=key, secret=secret)
    """
    def __init__(self, host, key, secret, partner, prefix='/xcover/'):
        """
        :param host: Host URL of the xCover Service
        :param key: Key for Auth
        :param secret: Secret for Auth
        :param partner: The partner to use for requests
        :param prefix: API Prefix which defaults to "/xcover/"
        """
        self.credentials = SignatureAuth(key=key, secret=secret)
        self.host = host
        self.prefix = prefix
        self.partner = partner
        conn = HttpRequest(self.host, auth=self.credentials, )
        registry.setup({'http_handler': conn})

    def create_quote(self, query_params=dict(), **kwargs):
        """
        Create a New Quote under a PartnerID by passing the API Fields as described in the API Docs

        :param query_params: Any parameters you want to pass in the URL

        >>> quote = client.create_quote(query_params={'limit': 10}, destination_country='AUS', data=...)

        :returns: Quote object with the response fields according to the Documentation
        """
        quote = Quote(partner_id=self.partner, prefix=self.prefix)
        response = quote._create(query_params, **kwargs)
        quote.set_values(response)
        return quote

    def get_quote(self, quote_package_id, query_params=dict(), **kwargs):
        """
        Get the Quote details when the Quote ID and Project ID is provided

        :param quote_package_id: The ID of the Quote Package
        :param query_params: Any parameters you want to pass in the URL

        >>> quote = Quote.get_quote(query_params={'limit': 10},  quote_package_id='bbbb')

        :returns: Quote object with the fields according to the API Documentation
        """
        quote = Quote(partner_id=self.partner, quote_package_id=quote_package_id, prefix=self.prefix)
        response = quote._get(query_params, **kwargs)
        quote.set_values(response)
        return quote

    def get_booking(self, quote_package_id, query_params=dict(), **kwargs):
        """
        Get the Booking details when the Quote Package ID and Project ID is provided

        :param quote_package_id: The ID of the Quote Package
        :param query_params: Any parameters you want to pass in the URL
        :returns: Booking object

        """
        kwargs['quote_package_id'] = quote_package_id

        booking = Bookings(partner_id=self.partner, quote_package_id=quote_package_id, prefix=self.prefix)
        response = booking._get(query_params, **kwargs)
        booking.set_values(response)
        return booking

    def create_booking(self, quote_package_id, query_params=dict(), **kwargs):
        """
        Create a New Booking under a PartnerID by passing the API Fields as described in the API Docs

        :param quote_package_id: The ID of the quote package under which the booking can be created
        :param query_params: Any parameters you want to pass in the URL

        :returns: Booking object with all the data as in the API Documentation
        """
        booking = Bookings(partner_id=self.partner, quote_package_id=quote_package_id, prefix=self.prefix)
        response = booking._create(query_params, **kwargs)
        booking.set_values(response)
        return booking

    def confirm_renewal(self, renewal_id, paid_on, query_params=dict()):
        """
        Confirm the Renewal by the Client

        :param renewal_id: The ID of the Renewal
        :param paid_on: The date the renewal was paid on in ISO 8601 format
        :param query_params: Any parameters you want to pass in the URL

        >>> Renewal.confirm_renewal(renewal_id='bbbb', paid_on='DD:MM:YYYY', query_params={'limit': 10})

        :returns: Success based on Response Status Code
        """
        return Renewal().patch(query_params, **{
            'partner_id': self.partner,
            'renewal_id': renewal_id,
            'paid_on': paid_on
        })

    def get_policies(self, query_params=dict(), **kwargs):
        """
        Get all Policy Types. Admin API Only. Wont work with all keys

        :param query_params: Any parameters you want to pass in the URL
        """
        policy_types = PolicyTypes(prefix=self.prefix, **kwargs)
        response = policy_types._get(query_params, **kwargs)
        policy_types.set_values(response)
        return policy_types
