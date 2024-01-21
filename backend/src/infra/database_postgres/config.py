from config import settings as s
from sqlalchemy.engine import create_engine


engine = create_engine(str(s.POSTGRES_URL))
