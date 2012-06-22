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

    def connect(self):
        return create_engine('sqlite:///:memory:', echo=False)

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
