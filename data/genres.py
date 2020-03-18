import sqlalchemy

from .db_session import SqlAlchemyBase

book_to_genres = sqlalchemy.Table('book_to_genres', SqlAlchemyBase.metadata,
                                  sqlalchemy.Column('book_id', sqlalchemy.Integer,
                                                    sqlalchemy.ForeignKey('books.id')),
                                  sqlalchemy.Column('genres_id', sqlalchemy.Integer,
                                                    sqlalchemy.ForeignKey('genres.id'))
                                  )


class Genres(SqlAlchemyBase):
    __tablename__ = 'genres'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return '<Жанр id: {}, name: {} >'.format(self.id, self.name)
