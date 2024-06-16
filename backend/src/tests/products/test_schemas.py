import uuid

from main.utils import get_url

from products import urls
from products.schemas import (
    BaseProduct,
    WriteProduct,
    UpdateProduct,
    ReadProductShort
)


class TestBaseProduct:
    obj = BaseProduct()

    def test__clean_category(self):
        assert self.obj._clean_category(['100']) == ['100']
        assert self.obj._clean_category(['200,100,500']) == ['100', '200', '500']

        assert self.obj._clean_category(['400', '100']) == ['100', '400']


class TestWriteProduct:
    obj1 = WriteProduct(
        title='Product-1',
        description='...about Product-1',
        price=1230.89,
        category=['300', '100']
    )

    obj2 = WriteProduct(
        title='Product-2',
        description=None,
        price=30,
        category=['100', '400', '500']
    )

    def test_dict(self):
        assert self.obj1.dict == {
            'title': 'Product-1',
            'description': '...about Product-1',
            'price': 1230.89,
            'category': ['100', '300']
        }

        assert self.obj2.dict == {
            'title': 'Product-2',
            'description': None,
            'price': 30,
            'category': ['100', '400', '500']
        }


class TestUpdateProduct:
    obj1 = UpdateProduct(
        title='UPDATE Product-1',
        description='UPDATE ...about Product-1',
        price=777.77,
        category=['300']
    )

    obj2 = UpdateProduct(
        title=None,
        description=None,
        price=None,
        category=[]
    )

    def test_dict(self):
        assert self.obj1.dict == {
            'title': 'UPDATE Product-1',
            'description': 'UPDATE ...about Product-1',
            'price': 777.77,
            'category': ['300']
        }

        assert self.obj2.dict == {}


class TestReadProductShort:
    obj = ReadProductShort(product_id=uuid.uuid4())

    def test_serializer(self):
        path = urls.Retrieve_Product.replace(':product-id', str(self.obj.product_id))
        assert self.obj.model_dump() == {'product': get_url(path=path)}

