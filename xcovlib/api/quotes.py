from .base import BaseModel


class Quote(BaseModel):
    """
    Base Class for Quote Model as described in the documentation for xCover.

    Quote supports two methods, which are create and get. You can use both to access and manipulate quotes
    on the database
    """
    _path_to_collection = 'partners/%(partner_id)s/quotes/'
    _path_to_item = 'partners/%(partner_id)s/quotes/%(quote_package_id)s/'

    url_fields = {'partner_id', 'quote_package_id'}

    def __str__(self):
        return '[Quote ID={}]'.format(self.quote_package_id)

    @classmethod
    def get_quote(cls, partner_id, quote_package_id, query_params=dict(), **kwargs):
        """
        Get the Quote details when the Quote ID and Project ID is provided

        :param partner_id: The ID of the Partner
        :param quote_package_id: The ID of the Quote Package
        :param query_params: Any parameters you want to pass in the URL

        >>> quote = Quote.get_quote(partner_id='aaa', query_params={'limit': 10},  quote_package_id='bbbb')

        :returns: Quote object with the fields according to the API Documentation
        """
        quote = cls(partner_id=partner_id, quote_package_id=quote_package_id)
        response = quote._get(query_params, **kwargs)
        quote.set_values(response)
        return quote

    @classmethod
    def create_quote(cls, partner_id, query_params=dict(), **kwargs):
        """
        Create a New Quote under a PartnerID by passing the API Fields as described in the API Docs

        :partner_id: Id of the Partner for which the Quote is being created
        :param query_params: Any parameters you want to pass in the URL

        >>> quote = Quote.create_quote(partner_id='aaa', query_params={'limit': 10}, destination_country='AUS', data=...)

        :returns: Quote object with the response fields according to the Documentation
        """
        quote = cls(partner_id=partner_id)
        response = quote._create(query_params, **kwargs)
        quote.set_values(response)
        return quote
