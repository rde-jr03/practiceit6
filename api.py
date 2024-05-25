from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "classicmodels"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


#CREATE/GET
@app.route("/employee", methods=["GET"])
def get_actors():
    data = data_fetch("""select * from employees""")
    return make_response(jsonify(data), 200)


#EMPLOYEE ID
@app.route("/employee/<int:id>", methods=["GET"])
def get_actor_by_id(id):
    data = data_fetch("""SELECT * FROM employees WHERE employeeNumber = {}""".format(id))
    return make_response(jsonify(data), 200)


#INNER JOIN
@app.route("/order/<int:orderNumber>/details", methods=["GET"])
def get_order_details(orderNumber):
    data = data_fetch(
    """
    SELECT orders.orderNumber, orderdetails.quantityOrdered
    FROM orders
    INNER JOIN orderdetails
    ON orders.orderNumber = orderdetails.orderNumber
    WHERE orders.orderNumber = 10124
    """.format(orderNumber)
    )
    return make_response(
    jsonify({"orderNumber": orderNumber, "count": len(data), "details": data}), 200
    )


#ADD/POST
@app.route("/orders", methods=["POST"])
def add_orders():
    cur = mysql.connection.cursor()
    info = request.get_json()
    orderNumber = info["orderNumber"]
    orderDate = info["orderDate"]
    requiredDate = info["requiredDate"]
    shippedDate = info["shippedDate"]
    status = info["status"]
    comments = info["comments"]
    customerNumber = info["customerNumber"]
    cur.execute(
        """
        INSERT INTO orders (orderNumber, orderDate, requiredDate, shippedDate, status,
    comments, customerNumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (orderNumber, orderDate, requiredDate, shippedDate, status, comments,
    customerNumber),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
        {"message": "order added successfully", "rows_affected": rows_affected}
        ),
        201,
    )


#UPDATE/PUT
@app.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    orderNumber = info["orderNumber"]
    orderDate = info["orderDate"]
    requiredDate = info["requiredDate"]
    shippedDate = info.get("shippedDate") # Use .get() for optional fields
    status = info["status"]
    comments = info.get("comments") # Use .get() for optional fields
    customerNumber = info["customerNumber"]
    cur.execute(
        """
        UPDATE orders
        SET orderNumber = %s, orderDate = %s, requiredDate = %s,
        shippedDate = %s, status = %s, comments = %s, customerNumber = %s
        WHERE order_id = %s
        """,
        (orderNumber, orderDate, requiredDate, shippedDate, status, comments,
    customerNumber, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
        {"message": "order updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


#DELETE
@app.route("/orders/<int:id>", methods=["DELETE"])
def delete_actor(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM orders where orderNumber = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
        {"message": "order deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )


#URI PARAMETERS
@app.route("/orders/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    orderid = request.args.get('ordernumber')
    stat = request.args.get('status')
    return make_response(jsonify({"format":fmt, “orderId”:orderId, "stat":stat}),200)


if __name__ == "__main__":
    app.run(debug=True)