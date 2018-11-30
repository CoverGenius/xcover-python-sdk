from xcovlib.http.auth import SignatureAuth
from xcovlib.http.http_requests import HttpRequest
from xcovlib.registry import registry
from unittest import TestCase
from ..quotes import Quote


class TestQuotes(TestCase):

    def setUp(self):
        credentials = SignatureAuth(key='XCOVAPIKEY', secret='testsecret')
        host = '127.0.0.1:8001'
        conn = HttpRequest(host, auth=credentials)
        registry.setup({'http_handler': conn})

    def test_quote_creation(self):
        data = [{
              "policy_type": "parcel_insurance",
              "policy_type_version": 1,
              "policy_start_date": "2018-12-12T13:00:00Z",
              "from_country": "AU",
              "from_zipcode": "2000",
              "to_country": "US",
              "ship_cost": 251,
              "to_zipcode": "10002",
              "cover_amount": 1000,
              "from_company_name": "company name",
              "ship_date": "2018-11-02T13:00:00Z",
              "parcel_products": [{
                "sku": "20001",
                "value": 1000
            }]
        }]

        quote = Quote.create_quote(
            partner_id='XCOV', currency='AUD', customer_country='AU', destination_country='US', request=data
        )

        # save quotes
        self.assertIsNotNone(quote.id)

        # check get request
        new_quote = Quote.get_quote(partner_id='XCOV', quote_package_id=quote.id)
        self.assertEqual(new_quote.id, quote.id)
