import dotenv
import os

dotenv.load_dotenv()

#misc
PRODUCTION = os.getenv('PRODUCTION') == False


#database
DB_NAME = os.getenv('DB_NAME') 
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')


