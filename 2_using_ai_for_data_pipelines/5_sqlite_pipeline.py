# Create a Python pipeline that reads and writes customer orders to the SQLite database
# then review it very carefully

import sqlite3
from typing import List, Dict, Optional


class CustomerOrderDAO:
    def __init__(self, db_path: str):
        """Initialize database connection."""
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Create and return a database connection."""
        return sqlite3.connect(self.db_path)

    def create_order(self, order_data: Dict) -> int:
        """
        Create a new customer order.
        Returns the new order ID.
        """
        query = """
                INSERT INTO CUSTOMER_ORDER (ORDER_DATE, SHIP_DATE, CUSTOMER_ID, PRODUCT_ID, ORDER_QTY, SHIPPED)
                VALUES (?, ?, ?, ?, ?, ?) \
                """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    order_data['order_date'],
                    order_data.get('ship_date'),
                    order_data['customer_id'],
                    order_data['product_id'],
                    order_data['order_qty'],
                    order_data.get('shipped', 0)
                ))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            raise Exception(f"Error creating order: {str(e)}")

    def get_order(self, order_id: int) -> Optional[Dict]:
        """Retrieve a customer order by ID."""
        query = """
                SELECT ORDER_ID, ORDER_DATE, SHIP_DATE, CUSTOMER_ID, PRODUCT_ID, ORDER_QTY, SHIPPED
                FROM CUSTOMER_ORDER \
                WHERE ORDER_ID = ? \
                """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (order_id,))
                row = cursor.fetchone()
                if row:
                    return {
                        'order_id': row[0],
                        'order_date': row[1],
                        'ship_date': row[2],
                        'customer_id': row[3],
                        'product_id': row[4],
                        'order_qty': row[5],
                        'shipped': row[6]
                    }
                return None
        except sqlite3.Error as e:
            raise Exception(f"Error retrieving order: {str(e)}")

    def update_order(self, order_id: int, order_data: Dict) -> bool:
        """
        Update an existing customer order.
        Returns True if update was successful, False if order not found.
        """
        query = """
                UPDATE CUSTOMER_ORDER
                SET ORDER_DATE  = ?, \
                    SHIP_DATE   = ?, \
                    CUSTOMER_ID = ?, \
                    PRODUCT_ID  = ?, \
                    ORDER_QTY   = ?, \
                    SHIPPED     = ?
                WHERE ORDER_ID = ? \
                """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    order_data['order_date'],
                    order_data.get('ship_date'),
                    order_data['customer_id'],
                    order_data['product_id'],
                    order_data['order_qty'],
                    order_data.get('shipped', 0),
                    order_id
                ))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise Exception(f"Error updating order: {str(e)}")

    def delete_order(self, order_id: int) -> bool:
        """
        Delete a customer order by ID.
        Returns True if deletion was successful, False if order not found.
        """
        query = "DELETE FROM CUSTOMER_ORDER WHERE ORDER_ID = ?"
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (order_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            raise Exception(f"Error deleting order: {str(e)}")

    def get_all_orders(self) -> List[Dict]:
        """Retrieve all customer orders."""
        query = """
                SELECT ORDER_ID, ORDER_DATE, SHIP_DATE, CUSTOMER_ID, PRODUCT_ID, ORDER_QTY, SHIPPED
                FROM CUSTOMER_ORDER \
                """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                return [{
                    'order_id': row[0],
                    'order_date': row[1],
                    'ship_date': row[2],
                    'customer_id': row[3],
                    'product_id': row[4],
                    'order_qty': row[5],
                    'shipped': row[6]
                } for row in rows]
        except sqlite3.Error as e:
            raise Exception(f"Error retrieving orders: {str(e)}")


# Example usage
if __name__ == "__main__":
    dao = CustomerOrderDAO("database.db")

    # Example: Create a new order
    new_order = {
        'order_date': '2025-09-29',
        'ship_date': '2025-10-02',
        'customer_id': 1,
        'product_id': 1,
        'order_qty': 100,
        'shipped': 0
    }
    try:
        new_order_id = dao.create_order(new_order)
        print(f"Created order with ID: {new_order_id}")

        # Example: Retrieve the order
        order = dao.get_order(new_order_id)
        print(f"Retrieved order: {order}")

        # Example: Update the order
        updated_order = new_order.copy()
        updated_order['order_qty'] = 150
        updated = dao.update_order(new_order_id, updated_order)
        print(f"Order updated: {updated}")

        # Example: Get all orders
        all_orders = dao.get_all_orders()
        print(f"All orders: {all_orders}")

        # Example: Delete the order
        deleted = dao.delete_order(new_order_id)
        print(f"Order deleted: {deleted}")

    except Exception as e:
        print(f"Error: {str(e)}")