# pylint:disable=C0111,C0103,C0305

def query_orders(db):
    # return a list of orders displaying each column
    query = "SELECT * FROM orders"
    results = db.execute(query)
    results = results.fetchall()
    return results


def get_orders_range(db, date_from, date_to):
    # return a list of orders displaying all columns with OrderDate between date_from and date_to
    query = "SELECT * FROM orders WHERE orders.OrderDate > ? AND orders.OrderDate <= ?"
    results = db.execute(query, (date_from, date_to))
    results = results.fetchall()
    return results


def get_waiting_time(db):
    # get a list with all the orders displaying each column
    # and calculate an extra TimeDelta column displaying the number of days
    # between OrderDate and ShippedDate, ordered by ascending TimeDelta
    query = "SELECT * , JULIANDAY(orders.ShippedDate)-JULIANDAY(orders.OrderDate) \
            AS TimeDelta FROM orders ORDER BY TimeDelta ASC"
    results = db.execute(query)
    results = results.fetchall()
    return results

