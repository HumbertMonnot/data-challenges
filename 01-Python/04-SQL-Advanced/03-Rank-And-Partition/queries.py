# pylint:disable=C0111,C0103

def order_rank_per_customer(db):
    query = """SELECT OrderID, CustomerID, OrderDate, RANK() OVER(PARTITION BY CustomerID
            ORDER BY OrderDate
            ) AS OrderRank
            FROM Orders"""
    db.execute(query)
    return db.fetchall()

def order_cumulative_amount_per_customer(db):
    query = """WITH per_comm AS (
SELECT 
	Orders.OrderID ,
	Orders.CustomerID,
	Orders.OrderDate,
	SUM(OrderDetails.UnitPrice*OrderDetails.Quantity) OVER(
		PARTITION BY Orders.OrderID
		) AS order_amount
FROM Orders
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
)
SELECT 
	per_comm.OrderID ,
	per_comm.CustomerID,
	per_comm.OrderDate,
	SUM(order_amount) OVER(
		PARTITION BY CustomerID
		ORDER BY OrderDate) AS Cumul
FROM per_comm
GROUP BY OrderID
ORDER BY CustomerID
"""
    db.execute(query)
    return db.fetchall()
