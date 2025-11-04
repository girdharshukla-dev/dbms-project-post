from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor(dictionary=True)

# == CUSTOMERS ==
@app.route("/customers")
def list_customers():
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    return render_template("customers.html", customers=customers)

@app.route("/customers/add", methods=["POST"])
def add_customer():
    name = request.form["customer_name"]
    address = request.form.get("address", "")
    phone = request.form.get("phone", "")
    cursor.execute(
        "INSERT INTO Customers (customer_name, address, phone) VALUES (%s, %s, %s)",
        (name, address, phone)
    )
    db.commit()
    return redirect(url_for("list_customers"))

@app.route("/customers/delete/<int:customer_id>")
def delete_customer(customer_id):
    cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
    db.commit()
    return redirect(url_for("list_customers"))

@app.route("/customers/update", methods=["POST"])
def update_customer():
    customer_id = request.form["customer_id"]
    name = request.form["customer_name"]
    address = request.form.get("address", "")
    phone = request.form.get("phone", "")
    cursor.execute(
        "UPDATE Customers SET customer_name=%s, address=%s, phone=%s WHERE customer_id=%s",
        (name, address, phone, customer_id)
    )
    db.commit()
    return redirect(url_for("list_customers"))


# == PARCELS ==
@app.route("/parcels")
def list_parcels():
    query = """
        SELECT p.*, c.customer_name AS sender_name
        FROM Parcels p
        JOIN Customers c ON p.sender_id = c.customer_id
    """
    cursor.execute(query)
    parcels = cursor.fetchall()
    return render_template("parcels.html", parcels=parcels)

@app.route("/parcels/add", methods=["POST"])
def add_parcel():
    sender_id = request.form["sender_id"]
    receiver_name = request.form["receiver_name"]
    destination = request.form.get("destination", "")
    weight = request.form.get("weight", 0)
    cursor.execute(
        "INSERT INTO Parcels (sender_id, receiver_name, destination, weight) VALUES (%s, %s, %s, %s)",
        (sender_id, receiver_name, destination, weight)
    )
    db.commit()
    return redirect(url_for("list_parcels"))

@app.route("/parcels/delete/<int:parcel_id>")
def delete_parcel(parcel_id):
    cursor.execute("DELETE FROM Parcels WHERE parcel_id = %s", (parcel_id,))
    db.commit()
    return redirect(url_for("list_parcels"))

@app.route("/parcels/update", methods=["POST"])
def update_parcel():
    parcel_id = request.form["parcel_id"]
    sender_id = request.form["sender_id"]
    receiver_name = request.form["receiver_name"]
    destination = request.form.get("destination", "")
    weight = request.form.get("weight", 0)
    cursor.execute(
        "UPDATE Parcels SET sender_id=%s, receiver_name=%s, destination=%s, weight=%s WHERE parcel_id=%s",
        (sender_id, receiver_name, destination, weight, parcel_id)
    )
    db.commit()
    return redirect(url_for("list_parcels"))


# == DELIVERIES ==
@app.route("/deliveries")
def list_deliveries():
    query = """
        SELECT d.*, p.receiver_name, p.destination
        FROM Deliveries d
        JOIN Parcels p ON d.parcel_id = p.parcel_id
    """
    cursor.execute(query)
    deliveries = cursor.fetchall()
    return render_template("deliveries.html", deliveries=deliveries)

@app.route("/deliveries/add", methods=["POST"])
def add_delivery():
    parcel_id = request.form["parcel_id"]
    delivery_date = request.form["delivery_date"]
    status = request.form.get("status", "")
    cursor.execute(
        "INSERT INTO Deliveries (parcel_id, delivery_date, status) VALUES (%s, %s, %s)",
        (parcel_id, delivery_date, status)
    )
    db.commit()
    return redirect(url_for("list_deliveries"))

@app.route("/deliveries/delete/<int:delivery_id>")
def delete_delivery(delivery_id):
    cursor.execute("DELETE FROM Deliveries WHERE delivery_id = %s", (delivery_id,))
    db.commit()
    return redirect(url_for("list_deliveries"))

@app.route("/deliveries/update", methods=["POST"])
def update_delivery():
    delivery_id = request.form["delivery_id"]
    parcel_id = request.form["parcel_id"]
    delivery_date = request.form["delivery_date"]
    status = request.form.get("status", "")
    cursor.execute(
        "UPDATE Deliveries SET parcel_id=%s, delivery_date=%s, status=%s WHERE delivery_id=%s",
        (parcel_id, delivery_date, status, delivery_id)
    )
    db.commit()
    return redirect(url_for("list_deliveries"))


# == OFFICES ==
@app.route("/offices")
def list_offices():
    cursor.execute("SELECT * FROM Offices")
    offices = cursor.fetchall()
    return render_template("offices.html", offices=offices)

@app.route("/offices/add", methods=["POST"])
def add_office():
    name = request.form["office_name"]
    location = request.form.get("location", "")
    cursor.execute(
        "INSERT INTO Offices (office_name, location) VALUES (%s, %s)",
        (name, location)
    )
    db.commit()
    return redirect(url_for("list_offices"))

@app.route("/offices/delete/<int:office_id>")
def delete_office(office_id):
    cursor.execute("DELETE FROM Offices WHERE office_id = %s", (office_id,))
    db.commit()
    return redirect(url_for("list_offices"))

@app.route("/offices/update", methods=["POST"])
def update_office():
    office_id = request.form["office_id"]
    name = request.form["office_name"]
    location = request.form.get("location", "")
    cursor.execute(
        "UPDATE Offices SET office_name=%s, location=%s WHERE office_id=%s",
        (name, location, office_id)
    )
    db.commit()
    return redirect(url_for("list_offices"))


# == ROOT ==
@app.route("/")
def home():
    return """
    <h1>Parcel Management System</h1>
    <ul>
        <li><a href='/customers'>Customers</a></li>
        <li><a href='/parcels'>Parcels</a></li>
        <li><a href='/deliveries'>Deliveries</a></li>
        <li><a href='/offices'>Offices</a></li>
    </ul>
    """


if __name__ == "__main__":
    app.run(debug=True, port=5000)
