# pylint:disable=C0111,C0103

def detailed_orders(db):
    '''return a list of all orders (order_id, customer.contact_name,
    employee.firstname) ordered by order_id'''
    query = "SELECT orders.OrderID, customers.ContactName, employees.FirstName \
            FROM orders\
            JOIN customers ON orders.CustomerID = customers.CustomerID\
            JOIN employees ON orders.EmployeeID = employees.EmployeeID"
    db.execute(query)
    return db.fetchall()

def spent_per_customer(db):
    '''return the total amount spent per customer ordered by ascending total
    amount (to 2 decimal places)
    Exemple :
        Jean   |   100
        Marc   |   110
        Simon  |   432
        ...
    '''
    query = "WITH CumulAmount AS (\
    WITH TotalAmount AS (\
	SELECT \
		Customers.ContactName,\
		(OrderDetails.UnitPrice * OrderDetails.Quantity) as total_amount\
	FROM Orders\
	JOIN OrderDetails ON OrderDetails.OrderID = Orders.OrderID\
	JOIN Customers ON Customers.CustomerID = Orders.CustomerID \
	ORDER BY ContactName)\
    SELECT *, SUM(TotalAmount.total_amount) OVER (\
	PARTITION BY TotalAmount.ContactName) AS sum_amount\
    FROM TotalAmount)\
    SELECT ContactName, sum_amount\
    FROM CumulAmount\
    GROUP BY sum_amount"
    db.execute(query)
    return db.fetchall()

def best_employee(db):
    '''Implement the best_employee method to determine who’s the best employee!
    By “best employee”, we mean the one who sells the most.
    We expect the function to return a tuple like: ('FirstName',
    'LastName', 6000 (the sum of all purchase)). The order of the information
    is irrelevant'''
    query = """WITH sell_emp AS (
SELECT
	Employees.FirstName,
	Employees.LastName,
	SUM(OrderDetails.UnitPrice * OrderDetails.Quantity) OVER(
		PARTITION BY Employees.LastName
		ORDER BY Employees.LastName) AS total_sell
FROM Orders
JOIN Employees ON Employees.EmployeeID = Orders.EmployeeID
JOIN OrderDetails ON OrderDetails.OrderID = Orders.OrderID
)
SELECT *
FROM sell_emp
GROUP BY sell_emp.LastName
ORDER BY sell_emp.total_sell DESC"""
    db.execute(query)
    return tuple(db.fetchone())

def orders_per_customer(db):
    '''TO DO: return a list of tuples where each tupe contains the contactName
    of the customer and the number of orders they made (contactName,
    number_of_orders). Order the list by ascending number of orders'''
    query = """SELECT customers.ContactName, COALESCE(COUNT(orders.OrderDate), 0) AS nb_comm
FROM Customers
LEFT JOIN orders ON orders.CustomerID = customers.CustomerID
GROUP BY customers.ContactName
ORDER BY nb_comm"""
    db.execute(query)
    return db.fetchall()
