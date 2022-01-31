import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        # $CHALLENGIFY_BEGIN
        # make sure to create a copy rather than a "view"
        orders = self.data['orders'].copy()

        # filter delivered orders
        if is_delivered:
            orders = orders.query("order_status=='delivered'").copy()

        # handle datetime
        orders.loc[:, 'order_delivered_customer_date'] = \
            pd.to_datetime(orders['order_delivered_customer_date'])
        orders.loc[:, 'order_estimated_delivery_date'] = \
            pd.to_datetime(orders['order_estimated_delivery_date'])
        orders.loc[:, 'order_purchase_timestamp'] = \
            pd.to_datetime(orders['order_purchase_timestamp'])

        # compute delay vs expected
        orders.loc[:, 'delay_vs_expected'] = \
            (orders['order_delivered_customer_date'] -
             orders['order_estimated_delivery_date']) / np.timedelta64(24, 'h')

        def handle_delay(x):
            # We only want to keep delay where wait_time is longer than expected (not the other way around)
            # This is what drives customer dissatisfaction!
            if x > 0:
                return x
            else:
                return 0

        orders.loc[:, 'delay_vs_expected'] = \
            orders['delay_vs_expected'].apply(handle_delay)

        # compute wait time
        orders.loc[:, 'wait_time'] = \
            (orders['order_delivered_customer_date'] -
             orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')

        # compute expected wait time
        orders.loc[:, 'expected_wait_time'] = \
            (orders['order_estimated_delivery_date'] -
             orders['order_purchase_timestamp']) / np.timedelta64(24, 'h')

        return orders[[
            'order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
            'order_status'
        ]]
        # $CHALLENGIFY_END
        
        
    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews']
        reviews['dim_is_five_star'] = [1 if reviews.review_score[i] == 5 else 0 for i in reviews.index]
        reviews['dim_is_one_star'] = [1 if reviews.review_score[i] == 1 else 0 for i in reviews.index]
        reviews = reviews[['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]
        return reviews

    def get_number_products(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        nb_product = self.data['order_items'].groupby('order_id', as_index = False).count()[['order_id','order_item_id']]
        nb_product.columns = ['order_id','number_of_products']
        return nb_product

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        nb_sellers = self.data['order_items'].groupby('order_id', as_index = False).nunique()[['order_id','seller_id']]
        nb_sellers.columns = ['order_id','number_of_sellers']
        return nb_sellers

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        return self.data['order_items'].groupby('order_id', as_index = False).sum()[['order_id', 'price', 'freight_value']]

    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        # $CHALLENGIFY_BEGIN

        # import data
        data = self.data
        orders = data['orders']
        order_items = data['order_items']
        sellers = data['sellers']
        customers = data['customers']

        # Since one zip code can map to multiple (lat, lng), take the first one
        geo = data['geolocation']
        geo = geo.groupby('geolocation_zip_code_prefix',
                          as_index=False).first()

        # Merge geo_location for sellers
        sellers_mask_columns = [
            'seller_id', 'seller_zip_code_prefix', 'geolocation_lat', 'geolocation_lng'
        ]

        sellers_geo = sellers.merge(
            geo,
            how='left',
            left_on='seller_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[sellers_mask_columns]

        # Merge geo_location for customers
        customers_mask_columns = ['customer_id', 'customer_zip_code_prefix', 'geolocation_lat', 'geolocation_lng']

        customers_geo = customers.merge(
            geo,
            how='left',
            left_on='customer_zip_code_prefix',
            right_on='geolocation_zip_code_prefix')[customers_mask_columns]

        # Match customers with sellers in one table
        customers_sellers = customers.merge(orders, on='customer_id')\
            .merge(order_items, on='order_id')\
            .merge(sellers, on='seller_id')\
            [['order_id', 'customer_id','customer_zip_code_prefix', 'seller_id', 'seller_zip_code_prefix']]
        
        # Add the geoloc
        matching_geo = customers_sellers.merge(sellers_geo,
                                            on='seller_id')\
            .merge(customers_geo,
                   on='customer_id',
                   suffixes=('_seller',
                             '_customer'))
        # Remove na()
        matching_geo = matching_geo.dropna()

        matching_geo.loc[:, 'distance_seller_customer'] =\
            matching_geo.apply(lambda row:
                               haversine_distance(row['geolocation_lng_seller'],
                                                  row['geolocation_lat_seller'],
                                                  row['geolocation_lng_customer'],
                                                  row['geolocation_lat_customer']),
                               axis=1)
        # Since an order can have multiple sellers,
        # return the average of the distance per order
        order_distance =\
            matching_geo.groupby('order_id',
                                 as_index=False).agg({'distance_seller_customer':
                                                      'mean'})

        return order_distance
        # $CHALLENGIFY_END

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=True):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_products', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        # $CHALLENGIFY_BEGIN
        training_set =\
            self.get_wait_time(is_delivered)\
                .merge(
                self.get_review_score(), on='order_id'
            ).merge(
                self.get_number_products(), on='order_id'
            ).merge(
                self.get_number_sellers(), on='order_id'
            ).merge(
                self.get_price_and_freight(), on='order_id'
            )
        # Skip heavy computation of distance_seller_customer unless specified
        if with_distance_seller_customer:
            training_set = training_set.merge(
                self.get_distance_seller_customer(), on='order_id')

        return training_set.dropna()
        # $CHALLENGIFY_END
