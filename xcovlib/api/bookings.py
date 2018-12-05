from .base import BaseModel


class Bookings(BaseModel):
    """
    Base Class for Booking Model as described in the documentation for xCover.

    Quote supports two methods, which are create_booking and get_booking.
    You can use it to access and manipulate booking on the database

    TODO: Add update field and cancel method
    """
    _path_to_collection = 'partners/%(partner_id)s/bookings/%(quote_package_id)s/'
    _path_to_item = 'partners/%(partner_id)s/bookings/%(quote_package_id)s/'

    url_fields = {'partner_id', 'quote_package_id'}

    def __str__(self):
        return '[Booking ID={}]'.format(self.quote_package_id)

    @classmethod
    def get_booking(cls, partner_id, quote_package_id, query_params=dict(), **kwargs):
        """
        Get the Booking details when the Quote Package ID and Project ID is provided

        :param partner_id ID: The ID of the Partner under which the booking exists
        :param quote_package_id Package ID: The ID of the Quote Package
        :param query_params: Any parameters you want to pass in the URL
        :returns: Booking object

        """
        kwargs['partner_id'] = partner_id
        kwargs['quote_package_id'] = quote_package_id
        booking = cls(partner_id=partner_id, quote_package_id=quote_package_id)

        response = booking._get(query_params, **kwargs)
        booking.set_values(response)
        return booking

    @classmethod
    def create_booking(cls, partner_id, quote_package_id, query_params=dict(), **kwargs):
        """
        Create a New Booking under a PartnerID by passing the API Fields as described in the API Docs

        :param partner_id: The ID of the partner for which the booking needs to be created
        :param quote_package_id: The ID of the quote package under which the booking can be created
        :param query_params: Any parameters you want to pass in the URL

        :returns: Booking object with all the data as in the API Documentation
        """
        booking = cls(partner_id=partner_id, quote_package_id=quote_package_id)
        response = booking._create(query_params, **kwargs)
        booking.set_values(response)
        return booking
