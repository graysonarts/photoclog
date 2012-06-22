import os
import os.path as path

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

    def connect(self):
        return create_engine('sqlite:///:memory:', echo=True)

    def setup_engine(self):
        self.engine = self.connect()
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def testCreation(self):
        self.setup_engine()
        assert self.engine is not None
    
    
    def testBasicTagCreation(self):
        self.setup_engine()
        session = self.Session()
        for tag in self.tags:
            tag_object = Tag(**tag)
            session.add(tag_object)
        session.commit()
        
        actual_tags = session.query(Tag).order_by('tag_id').all()
        assert len(actual_tags) == len(self.tags)
        for actual_tag in actual_tags:
            tag_id = actual_tag.tag_id
            ok_(actual_tag.name,self.tags[tag_id-1])
    
    def testPhotoGuid(self):
        self.setup_engine()
        session = self.Session()
        x = Photo()
        x.guid = None
        assert x.guid is not None
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
        