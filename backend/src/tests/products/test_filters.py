from products.models import Product, ProductCategory
from products.filters import ProductFilter


class TestProductFilter:
    filter1 = ProductFilter(
        category=None,
        min_price=0,
        max_price=999999,
        published = 'asc'
    )

    filter2 = ProductFilter(
        category=['500', '100', '200'],
        min_price=99.99,
        max_price=299,
        published = 'desc'
    )

    filter3 = ProductFilter(
        category=None,
        min_price=999999,
        max_price=0,
        published = 'asc'
    )

    def test_errors(self):
        assert self.filter1.errors == []
        assert self.filter2.errors == []
        assert self.filter3.errors == ['Price error! min_price > max_price ({0} > {1})'.format(999999, 0)]

    def test_category(self):
        assert self.filter1.category == None

        filter2_clause = '{0}.category_key = :{1} OR {2}.category_key = :{3} OR {4}.category_key = :{5}'.format(
            ProductCategory.__tablename__,
            'category_0',
            ProductCategory.__tablename__,
            'category_1',
            ProductCategory.__tablename__,
            'category_2'
        )
        filter2_kwargs = {
            'category_0': '500',
            'category_1': '100',
            'category_2': '200'
        }
        r_filter2_clause, r_filter2_kwargs = self.filter2.category
        assert str(r_filter2_clause) == filter2_clause
        assert r_filter2_kwargs == filter2_kwargs

    def test_price(self):
        filter1_clause = '{0}.price BETWEEN :{1} AND :{2}'.format(
            Product.__tablename__,
            'min_price',
            'max_price'
        )
        filter1_kwargs = {
            'min_price': 0,
            'max_price': 999999
        }
        r_filter1_clause, r_filter1_kwargs = self.filter1.price
        assert str(r_filter1_clause) == filter1_clause
        assert r_filter1_kwargs == filter1_kwargs

        filter2_clause = '{0}.price BETWEEN :{1} AND :{2}'.format(
            Product.__tablename__,
            'min_price',
            'max_price'
        )
        filter2_kwargs = {
            'min_price': 99.99,
            'max_price': 299
        }
        r_filter2_clause, r_filter2_kwargs = self.filter2.price
        assert str(r_filter2_clause) == filter2_clause
        assert r_filter2_kwargs == filter2_kwargs

    def test_published(self):
        assert self.filter1.published == 'asc'
        assert self.filter2.published == 'desc'

