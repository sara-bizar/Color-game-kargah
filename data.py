import psycopg2
from dotenv import load_dotenv
import os


class UserDataManager:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.dbname = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")

    def connect_db(self):
        return psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def create_table_users(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(50),
                score INTEGER,
                trys INTEGER
            );
        """
        )
        conn.commit()
        cursor.close()
        conn.close()

    def create_colors_table(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS colors (
                color_name VARCHAR(50),
                hex_value VARCHAR(7)
            );
        """
        )
        conn.commit()
        cursor.close()
        conn.close()

    # Function to store user data
    def store_user_data(self, username, score, trys):
        conn = self.connect_db()
        cursor = conn.cursor()

        # Check if the user already exists
        cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
        exists = cursor.fetchone()

        if exists:
            # Update the existing user's score and trys
            cursor.execute(
                "UPDATE users SET score = %s, trys = %s WHERE username = %s",
                (score, trys, username),
            )
        else:
            # Insert a new user
            cursor.execute(
                "INSERT INTO users (username, score, trys) VALUES (%s, %s, %s)",
                (username, score, trys),
            )

        conn.commit()
        cursor.close()
        conn.close()

    def store_color_data(self, color_name, hex_value):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO colors (color_name, hex_value) VALUES (%s, %s)",
            (color_name, hex_value),
        )
        conn.commit()
        cursor.close()
        conn.close()

    # Function to retrieve user data
    def retrieve_user_data(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT username, score, trys FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def retrieve_all_colors(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT color_name, hex_value FROM colors")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # Function to retrieve data for a specific user by username
    def retrieve_user_by_name(self, username):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, score, trys FROM users WHERE username = %s", (username,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def retrieve_color_by_name(self, color_name):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT color_name, hex_value FROM colors WHERE color_name = %s",
            (color_name,),
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    # Function to clear all user data
    def clear_all_users(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        conn.commit()
        cursor.close()
        conn.close()

    def clear_all_colors(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM colors")
        conn.commit()
        cursor.close()
        conn.close()

    # Function to remove a specific user by username
    def remove_user_by_name(self, username):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
        cursor.close()
        conn.close()

    def remove_color_by_name(self, color_name):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM colors WHERE color_name = %s", (color_name,))
        conn.commit()
        cursor.close()
        conn.close()


# Example usage
if __name__ == "__main__":
    manager = UserDataManager()

    manager.create_table_users()
    manager.clear_all_users()
    # Store initial data
    manager.store_user_data("Melika", 6, 3)
    manager.store_user_data("Sara", 4, 2)
    manager.store_user_data("Arman", 2, 1)
    manager.store_user_data("Fatemeh", 1, 5)

    # Retrieve and print all data
    users = manager.retrieve_user_data()
    print("users: ", users)
    print(type(users))
    # for user, score, trys in users:
    #     print(user, score, trys)

    # Retrieve and print data for a specific user
    # specific_user = manager.retrieve_user_by_name("Sara")
    # print(specific_user)

    # Remove a specific user
    # manager.store_user_data("Melika", 6, 3)
    # manager.remove_user_by_name("Melika")

    # manager.create_colors_table()
    # manager.clear_all_colors()
    # colors = {
    #     "orange": "#ee541a",
    #     "blue": "#1a6dec",
    #     "yellow": "#f3d332",
    #     "purple": "#b244d3",
    #     "pink": "#e6869a",
    #     "green": "#52d734",
    #     "red": "#ea2e35",
    # }
    # for color_name, hex_value in colors.items():
    #     manager.store_color_data(color_name, hex_value)

    colors = manager.retrieve_all_colors()
    print("colors: ", colors)
    print(type(colors))
    # for color in colors:
    #     print(color)
    print([i[0] for i in colors])
    print(next((code for name, code in colors if name == "pink"), None))
