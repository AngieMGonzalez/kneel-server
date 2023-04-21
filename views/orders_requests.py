import sqlite3
import json
from models import Order, Metal, Size, Style


ORDERS = [
    {
        "id": 1,
        "metal_id": 3,
        "size_id": 2,
        "style_id": 3,
        "jewelry_id": 2,
        "timestamp": 1614659931693
    }
]


def get_all_orders():
    """get all SQL
    """
    # Open a connection to the database
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.jewelry_id,
            o.timestamp,
            m.metal,
            m.price metal_price,
            z.carets,
            z.price size_price,
            y.style,
            y.price style_price
        FROM Orders o
        JOIN Metals m
            on m.id = o.metal_id
        JOIN Sizes z
            on z.id = o.size_id
        JOIN Styles y
            on y.id = o.style_id
        """)

        # Initialize an empty list to hold all animal representations
        orders = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        # row is TACO
        for row in dataset:

            # Create an order instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Order class above.
            order = Order(row['id'], row['metal_id'], row['size_id'],
                            row['style_id'], row['jewelry_id'],
                            row['timestamp'])

            # Create a Metal instance from the current row
            metal = Metal(row['metal_id'], row['metal'], row['metal_price'])

            # Create a Style instance from the current row
            style = Style(row['style_id'], row['style'], row['style_price'])

            # Create a Size instance from the current row
            size = Size(row['size_id'], row['carets'], row['size_price'])

            # Add the dictionary representation of related object to the order instance
            # Here what added the size would look like
            order.size = size.__dict__

            order.metal = metal.__dict__

            order.style = style.__dict__

            orders.append(order.__dict__)

    return orders

def get_single_order(id):
    """gets single resource
    """
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            o.id,
            o.metal_id,
            o.size_id,
            o.style_id,
            o.jewelry_id,
            o.timestamp
        FROM Orders o
        WHERE o.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an order instance from the current row
        order = Order(data['id'], data['metal_id'], data['size_id'],
                        data['style_id'], data['jewelry_id'], data['timestamp'])

        return order.__dict__


def create_order(new_order):
    """GET POST new resource
    """
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Orders
            ( metal_id, size_id, style_id, jewelry_id, timestamp )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_order['metal_id'], new_order['size_id'],
            new_order['style_id'], new_order['jewelry_id'],
            new_order['timestamp'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the orders dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_order['id'] = id

    return new_order

def delete_order(id):
    """
    deletes a row from the DB
    """
    with sqlite3.connect("./kneeldiamonds.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Orders
        WHERE id = ?
        """, (id, ))

def update_order(id, new_order):
    """Updates order with Replacement"""
    # Iterate the ORDERS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, order in enumerate(ORDERS):
        if order["id"] == id:
            # Found the order. Update the value.
            ORDERS[index] = new_order
            break
