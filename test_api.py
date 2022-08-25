import pytest

from api import Item, User, Store
from mock_data import FakeData
from .constants import Headers


class MockData(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MockData, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.register_body = FakeData.fake_register_body()
        self.store_number = FakeData.fake_store_number()
        self.token = None
        self.store_id = None

data = MockData()

class TestApi:

    @pytest.mark.api1
    def test_registration(self, base_url):
        response = User(url=base_url).register_user(body=data.body)
        
        print(response.headers)
        assert response.status_code == 201
        assert response.json().get('message') == 'User created successfully.'
        assert response.json().get('uuid')

    @pytest.mark.api
    def test_existing_register(self, base_url):
        response = User(url=base_url).register_user(body=data.body)

        assert response.status_code == 400
        assert response.json().get('message') == 'A user with that username already exists'
        assert response.json().get('uuid')


    @pytest.mark.api1
    def test_authentification(self, base_url):
        response = User(url=base_url).authentificate(body=data.body)
        data.token = response.json().get('access_token')
        print(response.headers)

        assert response.status_code == 200
        assert data.token
        

    @pytest.mark.api
    def test_store_creation(self, base_url):
        response = Store(url=base_url).create(name=data.store_number, auth_key=data.token)

        assert response.status_code == 201        
        assert response.json().get('name') == str(data.store_number)
        assert response.json().get('uuid')


    @pytest.mark.api
    def test_getting_store(self, base_url):
        response = Store(url=base_url).get_(name=data.store_number, auth_key=data.token)

        assert response.status_code == 200       
        assert response.json().get('name') == str(data.store_number)
        data.store_id = response.json().get('uuid')
        assert data.store_id
    

    @pytest.mark.api
    def test_existing_store_creation(self, base_url):
        response = Store(url=base_url).create(name=data.store_number, auth_key=data.token)

        assert response.status_code == 400
        assert response.json().get('message') == f'''A store with name '{data.store_number}' already exists.'''
        # TODO: CAssert response name and 
    def test_create_store_item(self, base_url):
        response = Item.create(
            url=base_url, 
            name=FakeData.fake_item_name(),
            headers=Headers.auth_header(data.token),
            body=FakeData.fake_create_item_body(self.store_id),
            )
        
        assert response.status_code == 201
        assert response.json().get('name') == 
        
