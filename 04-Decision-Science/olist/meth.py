from operator import index
from webbrowser import get
import pandas as pd
import numpy as np
from olist.data import Olist
from olist.order import Order
from olist.seller import Seller

data = Olist().get_data()

def total_olist_profit(df):
    return df["olist_profit"].sum()


def it_cost(df):
    """Hypothèse de départ : 1) pour le nombre total de commande, 500k de coût 2) cout proportionnel à sqrt(n)
    Renvoie le cout IT pour olist"""
    coeff = 500000/(99841**(1/2))
    total_nb_orders = df["n_orders"].sum()
    return coeff*(total_nb_orders**(1/2))

def it_cost_n(n):
    """Hypothèse de départ : 1) pour le nombre total de commande, 500k de coût 2) cout proportionnel à sqrt(n)
    Renvoie le cout IT pour olist"""
    coeff = 500000/(99841**(1/2))
    initial_norders = 99841
    return 500000-coeff*((initial_norders -n)**(1/2))

def profit_including_itcost(df):
    return total_olist_profit(df) - it_cost(df)

def drop_a_nb_of_rows(df, nb):
    return df.drop(range(nb))

def drop_by_profit(df1, profit):
    return df1[df1['olist_profit']>profit]

def profit_after_droping(df1, profit):
    return total_olist_profit(drop_by_profit(df1, profit))-it_cost(drop_by_profit(df1, profit))

def nps_per_seller(df):
    data = Olist().get_data()
    _df = data['orders'].merge(data['order_reviews'], on = "order_id")
    _df['nps'] = _df['review_score'].map({5:1, 4:0, 3:-1, 2:-1, 1:-1})
    _df = _df.merge(data['order_items'], on = "order_id")
    _df = _df.groupby('seller_id', as_index = False).mean()
    _df = _df[['seller_id', "nps"]]
    return df.merge(_df, on = "seller_id")

def impact_if_never(df1):
    data = Olist().get_data()
    seller = Seller().get_training_data()
    df = df1.copy()
    total_nb_orders = data["orders"]["order_id"].count()
    coeff = 500000/(seller['n_orders'].sum()**(1/2))
    df['impact_if_never'] = -df['olist_profit']+(500000-coeff*((total_nb_orders-df['n_orders'])**(1/2)))
    return df

def drop_by_nps(df1, nps_score):
    df = nps_per_seller(df1)
    return df[df['nps']>nps_score]

def average_nps(df):
    return (df['nps']*df['n_orders']).sum()/df['n_orders'].sum()

def info_df(df, col):
    coeff = 500000/(99841**(1/2))
    recap =  pd.DataFrame.from_dict({"Nb de commande":round(df["n_orders"].sum(),0),
                         "Chiffre d'affaire":round(df["olist_revenue"].sum(),0),
                         "Cout des reviews":round(df['review_cost'].sum(),0),
                         "Cout IT": round(coeff * df['n_orders'].sum()**0.5,0),
                         "Profit Olist":round(df['olist_profit'].sum(),0)-round(coeff * df['n_orders'].sum()**0.5,0),
                         "Olist NPS": round(average_nps(df),2),                         
                         }, orient="index", columns=[col])
    recap[col].map('{:,.2}'.format)
    return recap
    
def comparative(df):
    df1 = info_df(Seller().get_training_data(), "Initiale")
    df2 = info_df(df, "Solution")
    df_compare = df1.join(df2)
    df_compare['Evolution (%)'] = round(df_compare['Solution']/df_compare['Initiale']*100-100,0)
    df.style.format({'Evolution (%)': '{:}%'})
    return df_compare


def allprod_df():
    allprod = data['order_items'].merge(data['products'], on="product_id").merge(data['orders'], on = 'order_id') \
                        .merge(data['order_reviews'], on="order_id").drop_duplicates(['order_id','product_id']) \
                        [['order_id', 'product_id', 'product_category_name', 'review_score','price']]


    allprod_count = allprod.groupby('product_category_name', as_index = False).count()[['review_score','product_category_name']]
    allprod_mean = allprod.groupby('product_category_name', as_index = False).mean()[['review_score','product_category_name']]
    allprod = allprod_count.merge(allprod_mean, on ="product_category_name")
    allprod.columns = ['Nb',"Category","Score_review"]
    allprod.sort_values('Score_review').head(50)

    allprod['indice'] = allprod['Score_review']*allprod['Nb']/allprod['Nb'].sum()
    mean_r = allprod['indice'].sum()

    allprod['diff_mean']=allprod['Score_review']-mean_r
    allprod = allprod.sort_values('diff_mean').reset_index()
    return allprod

def score_moyen(crit):
    allprod = allprod_df()
    new_ = allprod[allprod["Score_review"]>crit]
    new_['indice']= new_['Score_review']*new_['Nb']/new_['Nb'].sum()
    return new_['indice'].sum()

def nps_prd(crit):
    allprod = allprod_df()
    new_df = data['order_items'].merge(data['products'], on = "product_id").merge(data['orders'], \
                    on ='order_id').merge(data['order_reviews'], on='order_id')

    new_df = new_df[['order_id', 'product_id', 'seller_id', 'product_category_name', 'review_score']]
    list_cat_ok = list(allprod[allprod["Score_review"]>crit].Category)

    df_cat_ok = new_df[new_df['product_category_name'].isin(list_cat_ok)]

    df_cat_ok_ = df_cat_ok.groupby('order_id').mean()
    df_cat_ok_['nps'] = df_cat_ok_['review_score'].map({5:1, 4:0, 3:-1, 2:-1, 1:-1})
    return df_cat_ok_.nps.mean()