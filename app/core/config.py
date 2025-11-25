from dotenv import load_dotenv
import os

load_dotenv()

RABBITMQ_URI=os.getenv("RABBITMQ_URI")
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

