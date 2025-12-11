from dotenv import load_dotenv
import os

load_dotenv(".env")

BOT_TOKEN =  os.getenv("DISCORD_TOKEN")

CMD_PREFIX = "."
CASE_INSENSITIVE = True

DB_ADDRESS = os.getenv("DB_ADDRESS")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")