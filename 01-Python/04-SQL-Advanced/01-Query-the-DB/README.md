## Background & Objectives

Now it is time to make advanced SQL requets to an `ecommerce` database!

## Specs

Open the file `queries_db.py` to answer the following questions. Don't forget you can look inside the database by using DBeaver.

There are three methods to implement:


- Implement `query_orders` to get all the orders.
- Implement `get_orders_range` to get all the orders orders made between two given dates.
- Implement `get_waiting_time` to get all the orders with the delivery time in ascending order 👌

👉 **Ad a reminder**: Each method takes a `db` argument, which is a connection to the database, on which you can call the `execute` method. This `db` is **built by the test and passed along to the function**. No need to create one yourself to satisfy `make`. As a reminder your method will look like this:

```python
def the_method(db):
  results = db.execute("YOUR SQL QUERY")
  results = results.fetchall()
  # results in a list (rows) of list (columns)
  print(results)  # Inspect what you get back! Don't guess!

  # Then you'll need to return something.
  return ?
end
```



## Tools

You can use [DBeaver](https://dbeaver.io/) to visualize the databe.
