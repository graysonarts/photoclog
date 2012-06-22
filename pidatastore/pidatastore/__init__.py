import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

photo_tag_association_table = Table('photo_tag_association', Base.metadata,
   Column('photo_id', Integer, ForeignKey('photo.photo_id')),
   Column('tag_id', Integer, ForeignKey('tag.tag_id'))
)

class Photo(Base):
    __tablename__ = 'photo'

    photo_id = Column(Integer, primary_key=True)
    _guid = Column("guid", String)
    location = Column(String(convert_unicode=True))
    _thumbnail = Column("thumbnail", LargeBinary)
    shoot_date = Column(Date)

    tags = relationship('Tag', lazy='dynamic',
                        secondary=photo_tag_association_table,
                        backref='photos')
    
    @hybrid_property
    def guid(self):
        return self._guid
    
    @guid.setter
    def guid(self, value):
        if value is None:
            if self.location is None:
                value = None
            else:
                self._guid = str(uuid.uuid5(uuid.NAMESPACE_URL, self.location))
        else:
            self._guid = value
        
    @hybrid_property
    def thumbnail(self):
        return self._thumbnail
    
    @thumbnail.setter
    def thumbnail(self, filename):
        with open(filename, "rb") as input_:
            self._thumbnail = input_.read()

class Tag(Base):
    __tablename__ = 'tag'

    tag_id = Column(Integer, primary_key=True)
    name = Column(String(convert_unicode=True))
