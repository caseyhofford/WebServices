import http.client
import unittest


#good input

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        url = '127.0.0.1:8000'
        self.connection = http.client.HTTPConnection(url)

    def test_add_item(self):#Adds 10 cats and 5 dogs and checks that it receives the 200 error code back
        self.connection.request('POST', '/animals', body='{"Cat":10,"Dog":5,"Bat":7}')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_add_category(self):#Adds category trees with no items
        self.connection.request('POST', '/trees')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_add_category_item(self):#Adds category trees with no items
        self.connection.request('POST', '/fruits', body='{"Banana":3,"Peach":12}')
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
        self.connection.request('GET','')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_get_category(self):
        self.connection.request('GET','/animals')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_get_item(self):
        self.connection.request('GET','/animals/Dog')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_get_max(self):
        self.connection.request('GET','?max=9')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_get_min(self):
        self.connection.request('GET','?min=4')
        self.assertEqual(self.connection.getresponse().status, 200)

    def test_get_max_min(self):
        self.connection.request('GET','?max=9&min=4')
        self.assertEqual(self.connection.getresponse().status, 200)

#error cases below.....here be dragons

    def test_add_negative(self):
        self.connection.request('POST', '/animals', body='{"Cheetah":-10,"Bobcat":5,"Iguana":-7}')
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
        self.connection.request('PUT', '/animals/Cat?option=decrement&quant=50')
        self.assertEqual(self.connection.getresponse().status, 400)

    def test_get_fake_category(self):
        self.connection.request('GET', '/gase')
        self.assertEqual(self.connection.getresponse().status, 404)

    def test_get_fake_item(self):
        self.connection.request('GET', '/fruits/pine')
        self.assertEqual(self.connection.getresponse().status, 404)

if __name__ == '__main__':
    unittest.main()
