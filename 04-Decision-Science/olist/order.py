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
        orders = self.data['orders']
        delivered_orders = orders[orders['order_status']=='delivered']
        delivered_orders['order_purchase_timestamp'] = pd.to_datetime(delivered_orders['order_purchase_timestamp'])
        delivered_orders['order_delivered_customer_date'] = pd.to_datetime(delivered_orders['order_delivered_customer_date'])
        delivered_orders['order_estimated_delivery_date'] = pd.to_datetime(delivered_orders['order_estimated_delivery_date'])
        delivered_orders['wait_time']=(delivered_orders['order_delivered_customer_date'] - \
        delivered_orders['order_purchase_timestamp']) / np.timedelta64(1, 'D')
        delivered_orders['expected_wait_time']=(delivered_orders['order_estimated_delivery_date'] - \
        delivered_orders['order_purchase_timestamp']) / np.timedelta64(1, 'D')

        delivered_orders['delay_vs_expected'] = [(delivered_orders.wait_time[i] - delivered_orders.expected_wait_time[i])\
                                         if delivered_orders.wait_time[i] > delivered_orders.expected_wait_time[i] \
                                        else 0 for i in delivered_orders.index]
        
        delivered_orders = delivered_orders[['order_id', 'order_status',    
       'wait_time', 'expected_wait_time', 'delay_vs_expected']]
        return delivered_orders
        
        
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
        location = self.data["geolocation"].groupby('geolocation_zip_code_prefix', as_index = False).first()
        seller_zip = self.data['order_items'].merge(self.data['orders'], on = "order_id").merge(self.data['sellers'], on = "seller_id")[['order_id', 'seller_id', 'seller_zip_code_prefix']]

        seller_zip.columns = ['order_id','seller_id','geolocation_zip_code_prefix']
        seller_zip = seller_zip.merge(location, on = 'geolocation_zip_code_prefix')

        seller_zip.drop_duplicates(subset =["order_id","seller_id"], keep = 'first', inplace=True)

        customer_zip = self.data['order_items'].merge(self.data['orders'], on = "order_id").merge(self.data['customers'], on = "customer_id")[['order_id', 'customer_id', 'customer_zip_code_prefix']]

        customer_zip.columns = ['order_id','customer_id', 'geolocation_zip_code_prefix']
        customer_zip = customer_zip.merge(location, on = 'geolocation_zip_code_prefix')

        customer_zip.drop_duplicates(subset =["order_id","customer_id"], keep = 'first', inplace=True)

        coord_orders = seller_zip.merge(customer_zip, on = 'order_id', how = 'inner')

        coord_orders['distance_seller_customer'] = [haversine_distance( \
                                coord_orders.geolocation_lng_x[i], coord_orders.geolocation_lat_x[i], \
                                coord_orders.geolocation_lng_y[i], coord_orders.geolocation_lat_y[i]) \
                                for i in coord_orders.index]
        coord_orders = coord_orders[['order_id', 'distance_seller_customer']]

        coord_orders.groupby('order_id', as_index=False).mean()

        return coord_orders

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
        df1 = self.get_wait_time()
        df2 = self.get_review_score()
        df3 = self.get_number_products()
        df4 = self.get_number_sellers()
        df5 = self.get_price_and_freight()
        df6 = self.get_distance_seller_customer()
        training_data = df1.merge(df2, on ='order_id').merge(df3, on ='order_id').merge(df4, on ='order_id').merge(df5, on ='order_id')#.merge(df6, on='order_id')      
        training_data.dropna(inplace = True)
        return training_data
        