import psycopg2

# Database connection parameters
db_params = {
    'database': 'telebot',
    'user': 'telebot',
    'password': 'xsyusp',
    'host': 'localhost',
    'port': '5432',
}

def get_retail_orders():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)

        # Create a cursor
        cur = conn.cursor()

        # Define the SQL query to fetch retail orders
        sql_query = """
            SELECT name, sku, color, size, amount, adds
            FROM retail_order
            WHERE status_id = 1; -- Assuming status_id 1 is for "Delivered" status
        """

        # Execute the SQL query
        cur.execute(sql_query)

        # Fetch all rows from the result set
        retail_orders = cur.fetchall()

        return retail_orders

    except psycopg2.Error as e:
        print(f"Error fetching retail orders: {e}")
        return None

    finally:
        # Close the cursor and the database connection
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    retail_orders = get_retail_orders()

    if retail_orders:
        for order in retail_orders:
            name, sku, color, size, amount, adds = order
            print(f"Name: {name}, SKU: {sku}, Color: {color}, Size: {size}, Amount: {amount}, Adds: {adds}")
    else:
        print("No retail orders found.")

def get_wholesale_orders():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)

        # Create a cursor
        cur = conn.cursor()

        # Define the SQL query to fetch wholesale orders
        sql_query = """
            SELECT username, quantity, item_sku, item_color, item_size, amount
            FROM wholesaleordertelegtam
            WHERE status_id = 1; -- Assuming status_id 1 is for "Delivered" status
        """


        cur.execute(sql_query)


        wholesale_orders = cur.fetchall()

        return wholesale_orders

    except psycopg2.Error as e:
        print(f"Error fetching wholesale orders: {e}")
        return None

    finally:

        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    wholesale_orders = get_wholesale_orders()

    if wholesale_orders:
        for order in wholesale_orders:
            username, quantity, item_sku, item_color, item_size, amount = order
            print(f"Username: {username}, Quantity: {quantity}, SKU: {item_sku}, Color: {item_color}, Size: {item_size}, Amount: {amount}")
    else:
        print("No wholesale orders found.")