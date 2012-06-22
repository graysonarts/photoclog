import os
import os.path as path
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from nose.tools import ok_

from pidatastore import Base, Photo, Tag

class testBasic(object):
    def __init__(self):
        self.engine = None
        self.Session = None

        self.tags = [
            { 'tag_id': 1, 'name': 'man'},
            { 'tag_id': 2, 'name': 'woman'},
            { 'tag_id': 3, 'name': 'wedding'}
        ]
        self.test_photo_path = path.join(
            path.dirname(__file__),
            "test.jpg"
        )

        self.photo = {
            'photo_id': 1,
            'location': 'hd://photos2012/photos/blah',
            'shoot_date': date(2012, 01, 01),
            'thumbnail': self.test_photo_path
        }

    def connect(self):
        return create_engine('sqlite:///:memory:', echo=True)

    def setup_engine(self):
        self.engine = self.connect()
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def _add_tags(self):
        session = self.Session()
        for tag in self.tags:
            tag_object = Tag(**tag)
            session.add(tag_object)
        session.commit()
    
    def _add_photo(self):
        session = self.Session()
        photo = Photo(**self.photo)
        photo.guid = None
        session.add(photo)
        session.commit()
    
    def testCreation(self):
        self.setup_engine()
        assert self.engine is not None
    
    
    def testBasicTagCreation(self):
        self.setup_engine()
        self._add_tags()
        
        session = self.Session()
        actual_tags = session.query(Tag).order_by('tag_id').all()
        assert len(actual_tags) == len(self.tags)
        for actual_tag in actual_tags:
            tag_id = actual_tag.tag_id
            ok_(actual_tag.name,self.tags[tag_id-1])
    
    def testPhotoGuid(self):
        self.setup_engine()
        session = self.Session()
        x = Photo(location=self.photo['location'])
        x.guid = None
        assert x.guid is not None
        guid1 = x.guid
        
        x.guid = None
        assert x.guid is not None
        assert x.guid == guid1
        
        session.rollback()

    def testPhotoThumbnail(self):
        self.setup_engine()
        session = self.Session()
        x = Photo(photo_id=1)
        x.thumbnail = self.test_photo_path
        assert x.thumbnail is not None
        assert x.thumbnail is not self.test_photo_path
        session.add(x)
        session.commit()
        
        y = session.query(Photo).filter(Photo.photo_id==1).first()
        assert y.thumbnail is not None
        assert x.thumbnail == y.thumbnail
    
    def testTagPhotoAssociation(self):
        self.setup_engine()
        self._add_tags()
        self._add_photo()
        
        session = self.Session()
        
        