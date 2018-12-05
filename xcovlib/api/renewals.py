from .base import BaseModel


class Renewal(BaseModel):
    """
    Base Class for Renewals Model as described in the API documentation for xCover.

    Only supports Cancelling Renewals
    """
    _path_to_item = 'partners/%(partner_id)s/renewals/%(renewal_id)s/confirmation'

    url_fields = {'partner_id', 'renewal_id'}

    def __str__(self):
        return '[Renewal ID={}]'.format(self.quote_package_id)

    @classmethod
    def confirm_renewal(cls, partner_id, renewal_id, paid_on, query_params=dict()):
        """
        Confirm the Renewal by the Client

        :param partner_id: The ID of the Partner
        :param renewal_id: The ID of the Renewal
        :param paid_on: The date the renewal was paid on in ISO 8601 format
        :param query_params: Any parameters you want to pass in the URL

        >>> Renewal.confirm_renewal(partner_id='aaa', renewal_id='bbbb', paid_on='DD:MM:YYYY', query_params={'limit': 10})

        :returns: Success based on Response Status Code
        """
        return super().patch(query_params, **{
            'partner_id': partner_id,
            'renewal_id': renewal_id,
            'paid_on': paid_on
        })
