from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root@localhost:3306/usuariospython")
#engine = create_engine("mysql+mysqlclient://root@localhost:3306/usuariospython")

#conn = engine.connect()

meta_data = MetaData()