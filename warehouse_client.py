#!/usr/bin/python3

import http.client
import unittest
import json
import ssl
import base64


#good input

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        url = '127.0.0.1'
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.connection = http.client.HTTPSConnection(url,443,context=gcontext)
        login = base64.b64encode(b'casey:password').decode()
        self.hdrs = { 'Authorization' : 'Basic ' + login }

    def test_add_item(self):#Adds 10 cats and 5 dogs and checks that it receives the 200 error code back
        self.connection.request('POST', '/animals', body='{"Cat":40,"Dog":23,"Bat":7}')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_add_category_itema(self):#Adds category trees with no items
        self.connection.request('POST', '/fruits', body='{"Banana":3,"Peach":80}')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_add_category_itemb(self):#Adds category trees with no items
        self.connection.request('POST', '/trees', body='{"Pine":3,"Maple":12}')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_delete(self):
        self.connection.request('DELETE', '/animals/Cat')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_delete_category(self):
        self.connection.request('DELETE', '/trees')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_decrement(self):
        self.connection.request('PUT', '/animals/Bat?option=decrement&quant=1')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_increment(self):
        self.connection.request('PUT', '/animals/Bat?option=increment&quant=2')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_get_all(self):
        self.connection.request('GET','', headers = self.hdrs)
        response = json.loads(self.connection.getresponse().read().decode('utf-8'))
        self.assertEqual(response, json.loads('{"fruits": {"Banana": 3, "Peach": 80}, "animals": {"Dog": 23, "Bat": 6}}'))

    def test_get_category(self):
        self.connection.request('GET','/animals', headers = self.hdrs)
        response = json.loads(self.connection.getresponse().read().decode('utf-8'))
        self.assertEqual(response, json.loads('{"animals": {"Dog": 23, "Bat": 6}}'))

    def test_get_item(self):
        self.connection.request('GET','/animals/Dog', headers = self.hdrs)
        response = json.loads(self.connection.getresponse().read().decode('utf-8'))
        self.assertEqual(response, json.loads('{"animals": {"Dog": 23}}'))

    def test_get_max(self):
        self.connection.request('GET','?max=18', headers = self.hdrs)
        response = json.loads(self.connection.getresponse().read().decode('utf-8'))
        self.assertEqual(response, json.loads('{"fruits": {"Banana": 3}, "animals": {"Bat": 6}}'))

    def test_get_min(self):
        self.connection.request('GET','?min=4', headers = self.hdrs)
        response = json.loads(self.connection.getresponse().read().decode('utf-8'))
        self.assertEqual(response, json.loads('{"fruits": {"Peach": 80}, "animals": {"Dog": 23, "Bat": 6}}'))

    def test_get_max_min(self):
        self.connection.request('GET','?max=9&min=4', headers = self.hdrs)
        response = json.loads(self.connection.getresponse().read().decode('utf-8'))
        self.assertEqual(response, json.loads('{"animals": {"Bat": 6}}'))

    def test_get_prefix(self):
        self.connection.request('GET','/animals/D?prefix=true', headers = self.hdrs)
        response = json.loads(self.connection.getresponse().read().decode('utf-8'))
        self.assertEqual(response, json.loads('{"animals": {"Dog": 23}}'))

#error cases below.....here be dragons

    def test_add_negative(self):
        self.connection.request('POST', '/animals', body='{"Cheetah":-10,"Iguana":-7}')
        self.assertEqual(self.connection.getresponse().status, 400)

    def test_add_category_only(self):#Adds category trees with no items
        self.connection.request('POST', '/trees')
        self.assertEqual(self.connection.getresponse().status, 400)

    def test_add_category_negative(self):
        self.connection.request('POST', '/cars', body='{"Ferrari":-10}')
        self.assertEqual(self.connection.getresponse().status, 400)

    def test_delete_fake_item(self):
        self.connection.request('DELETE', '/trees/pine')
        self.assertEqual(self.connection.getresponse().status, 404)

    def test_delete_fake_category(self):
        self.connection.request('DELETE', '/gase')
        self.assertEqual(self.connection.getresponse().status, 404)

    def test_delete_root(self):
        self.connection.request('DELETE','/')
        self.assertEqual(self.connection.getresponse().status, 400)

    def test_increment_fake_item(self):
        self.connection.request('PUT', '/trees/pine?option=increment&quant=2')
        self.assertEqual(self.connection.getresponse().status, 404)

    def test_decrement_fake_item(self):
        self.connection.request('PUT', '/trees/pine?option=decrement&quant=2')
        self.assertEqual(self.connection.getresponse().status, 404)

    def test_decrement_negative(self):
        self.connection.request('PUT', '/animals/Dog?option=decrement&quant=50')
        self.assertEqual(self.connection.getresponse().status, 400)

    def test_get_fake_category(self):
        self.connection.request('GET', '/gase', headers = self.hdrs)
        self.assertEqual(self.connection.getresponse().status, 404)

    def test_get_fake_item(self):
        self.connection.request('GET', '/fruits/pine', headers = self.hdrs)
        self.assertEqual(self.connection.getresponse().status, 404)

    #HTTPS verification
    def test_http_get_auth(self):
        self.connection.request( 'GET', '', headers = self.hdrs )
        response = json.loads(self.connection.getresponse().read().decode('utf-8'))
        self.assertEqual(response, json.loads('{"fruits": {"Banana": 3, "Peach": 80}, "animals": {"Dog": 23, "Bat": 6}}'))

    def test_bad_auth(self):
        login = base64.b64encode(b'trump:password').decode()
        hdrs = { 'Authorization' : 'Basic ' + login }
        self.connection.request( 'GET', '', headers = hdrs)
        self.assertEqual(self.connection.getresponse().status, 403)

if __name__ == '__main__':
    unittest.main()
