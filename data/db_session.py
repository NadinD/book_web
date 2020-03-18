import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session, scoped_session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

# будем использовать для получения сессий подключения к нашей базе данных
__factory = None

# global_init принимает на вход адрес базы данных
def global_init(db_file):
    global __factory

    # проверяет, не создали ли мы уже фабрику подключений (то есть не вызываем ли мы функцию не первый раз
    if __factory:
        return

    # Проверяем, что нам указали непустой адрес базы данных
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    # создаем строку подключения :состоит из типа базы данных, адреса до базы данных и параметров подключения
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")


    # движок работы с базой данны
    # echo=True в консоль будут выводиться все SQL-запросы, которые сделает SQLAlchemy, что очень удобно для отладки
    engine = sa.create_engine(conn_str, echo=False)

    # создаем фабрику подключений к нашей базе данных, которая будет работать с нужным нам движком
    __factory = scoped_session(orm.sessionmaker(bind=engine))

    from . import __all_models

    # заставляем нашу базу данных создать все объекты, которые она пока не создала
    SqlAlchemyBase.metadata.create_all(engine)

# нужна для получения сессии подключения к нашей базе данных
def create_session():
    global __factory
    return Session( __factory())
