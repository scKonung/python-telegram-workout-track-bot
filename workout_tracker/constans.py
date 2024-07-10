from dotenv import load_dotenv
import os

#Here I import all my variables from enviroments
#Due to cybersecurity, I will not share this infromation

load_dotenv()


BOT_TOKEN = os.environ.get("BOT_TOKEN")

DATABASE_URL = os.environ.get("DATABASE_URL")

