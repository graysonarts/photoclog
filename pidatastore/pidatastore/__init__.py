from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import relationship

Base = declarative_base()

photo_tag_association_table = Table('photo_tag_association', Base.metadata,
   Column('photo_id', Integer, ForeignKey('photo.id')),
   Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Photo(Base):
    __tablename__ = 'photo'

    photo_id = Column(Integer, primary_key=True)
    guid = Column(String)
    location = Column(String(convert_unicode=True))
    thumbnail = Column(LargeBinary)
    shoot_date = Column(Date)

    tags = relationship('Tag', lazy='dynamic',
                        secondary=photo_tag_association_table,
                        backref='photos')

class Tag(Base):
    __tablename__ = 'tag'

    tag_id = Column(Integer, primary_key=True)
    name = Column(String(convert_unicode=True))
