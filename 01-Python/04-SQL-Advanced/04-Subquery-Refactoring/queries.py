# pylint:disable=C0111,C0103

def get_average_purchase(db):
    # return the average amount spent per order for each customer ordered by customer ID
    query = """WITH results AS (
WITH for_mean AS (
SELECT 
	ord.*,
	SUM(OrdD.UnitPrice*OrdD.Quantity) AS cost,
	COUNT(ord.OrderID) OVER(
		PARTITION BY CustomerID) AS nb
	FROM Orders ord
	INNER JOIN OrderDetails ordD ON ord.OrderID = OrdD.OrderID
	GROUP BY ord.OrderID
	ORDER BY CustomerID )
SELECT
	CustomerID,
	SUM(ROUND(cost/nb,2)) OVER(
		PARTITION BY CustomerID) AS sum_cost
FROM for_mean
)
SELECT *
FROM results
GROUP BY CustomerID"""
    db.execute(query)
    return db.fetchall()

def get_general_avg_order(db):
    # return the average amount spent per order
    query = """WITH results AS (
WITH for_mean AS (
SELECT 
	ord.*,
	SUM(OrdD.UnitPrice*OrdD.Quantity) AS cost,
	COUNT(ord.OrderID) OVER(
		PARTITION BY CustomerID) AS nb
	FROM Orders ord
	INNER JOIN OrderDetails ordD ON ord.OrderID = OrdD.OrderID
	GROUP BY ord.OrderID
	ORDER BY CustomerID )
SELECT
	CustomerID, nb,
	SUM(ROUND(cost/nb,2)) OVER(
		PARTITION BY CustomerID) AS mean_cost
FROM for_mean
)
SELECT mean_cost, nb, nb*mean_cost
FROM results
GROUP BY CustomerID"""
    db.execute(query)
    results = db.fetchall()
    truc = round(sum([k[2] for k in results])/sum([nb[1] for nb in results]),2)
    return truc

def best_customers(db):
    # return the customers who have an average purchase greater than the general average purchase
    pass  # YOUR CODE HERE

def top_ordered_product_per_customer(db):
    # return the list of the top ordered product by each customer based on the total ordered amount
    pass  # YOUR CODE HERE

def average_number_of_days_between_orders(db):
    # return the average number of days between two consecutive orders of the same customer
    pass  # YOUR CODE HERE
