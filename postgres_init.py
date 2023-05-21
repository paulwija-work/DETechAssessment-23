from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import configparser

def main():
    # getting credential from config file
    config = configparser.ConfigParser()
    config.read('config')
    host = config['Postgres']['Host']
    db   = config['Postgres']['DB']
    user = config['Postgres']['User']
    pwd  = config['Postgres']['Password']

    # create engine and table object for newTable
    Base = automap_base()
    # change this for your destination database
    destEngine = create_engine(f'postgresql://{user}:{pwd}@{host}:5432/{db}', client_encoding='utf-8')
    destEngine._metadata = MetaData(bind=destEngine)
    Base.prepare(destEngine, reflect=True)
    session = Session(destEngine)
    sql_txt = open('./table_ddl/creation_tables', "r").read()
    session.execute(sql_txt)
    session.commit()

if __name__ == '__main__':
    main()
