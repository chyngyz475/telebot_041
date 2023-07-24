import asyncpg

# Define the connection URL to your PostgreSQL database
# Replace the placeholders with your actual database credentials
DATABASE_URL = "postgresql://telebot:xsyusp@localhost:5432/telebot"

# Create a pool of connections to the database
async def create_pool():
    return await asyncpg.create_pool(DATABASE_URL)

# Function to insert a new wholesale order with photo into the database
async def insert_wholesale_order_with_photo(order_data, photo_bytes):
    async with create_pool() as pool:
        async with pool.acquire() as conn:
            # Convert the photo bytes to a bytea value
            photo_bytea = asyncpg.Binary(photo_bytes)

            await conn.execute(
                "INSERT INTO wholesale_orders (username, quantity, item_sku, item_color, item_size, amount, photo) "
                "VALUES ($1, $2, $3, $4, $5, $6, $7)",
                order_data['username'],
                order_data['quantitywh'],
                order_data['skuwh'],
                order_data['colorwh'],
                order_data['sizewh'],
                order_data['amountwh'],
                photo_bytea,
            )

# Function to retrieve the photo from the database for a given order
async def get_wholesale_order_photo(order_id):
    async with create_pool() as pool:
        async with pool.acquire() as conn:
            result = await conn.fetchrow("SELECT photo FROM wholesale_orders WHERE id = $1", order_id)
            if result:
                photo_bytea = result['photo']
                return bytes(photo_bytea)  # Convert bytea back to bytes
            return None
