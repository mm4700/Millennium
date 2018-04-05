import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

# conn = MySQLdb.connect(user='liguifan', password='stanford',
#                               host='trading.coby8x8uwinq.us-east-1.rds.amazonaws.com',
#                               database='Portfolio')


engine = create_engine('mysql://liguifan:stanford@trading.coby8x8uwinq.us-east-1.rds.amazonaws.com/Maomi')
conn = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()


# cursor = conn.cursor()
# cursor.execute(query, (hire_start, hire_end))
# cursor.execute(query)
