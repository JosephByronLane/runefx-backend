import dotenv
import os

dotenv.load_dotenv()

#misc
PRODUCTION = os.getenv('PRODUCTION', 'False') == 'True'


#database
DB_NAME = os.getenv('DB_NAME') 
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')

DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",") if host.strip()]
CORS_ALLOWED_ORIGINS = [host.strip() for host in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if host.strip()]