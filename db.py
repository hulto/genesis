#!/usr/bin/env python3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from typing import Union
import sys
import types

engine = create_engine('sqlite:////tmp/test.db', echo=True)
Base = declarative_base()
class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    hosts = None
    name = 'default'
    
    parent_id = Column(Integer, ForeignKey('tag.id'))
    parent = relationship("Tag")

#    parentId = Column(Integer, ForeignKey('Tag.id'), index=True)
#    parent = relationship('Tag', backref=backref('parent', remote_side='Tag.id'))


    def __init__(self, name: str, parent=None, hosts=[]):
        self.name = name
        self.hosts = hosts
        if parent is not None:
            self.parent_id = parent.id
        else:
            self.parent_id = -1

        session.add(self)
        try:
            session.commit()
        except exc.IntegrityError as err:
            session.rollback()
            if "UNIQUE constraint failed: projects.name" in str(err):
                sys.stderr.write("error, project name already exists (%s)\n" % name)
            elif "FOREIGN KEY constraint failed" in str(err):
                sys.stderr.write("supplier does not exist\n")
            else:
                sys.stderr.write("unknown error project user")

    def __repr__(self):
        return("<Tag(name='%s', parent_id='%d')>" % (self.name, self.parent_id))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String, unique=True)

    def __init__(self, name, fullname, nickname):
        self.name = name
        self.fullname = fullname
        self.nickname = nickname
        session.add(self)
        try:
            session.commit()
        except exc.IntegrityError as err:
            session.rollback()
            sys.stderr.write("unknown error project user\n")

    def __repr__(self):
       return "<User(id='%d', name='%s', fullname='%s', nickname='%s')>" % (
                            self.id, self.name, self.fullname, self.nickname)

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    ownerId = Column(Integer, ForeignKey('users.id'))
    name = Column(String, unique=True)
    proj_type = Column(String)

    def __init__(self, name, proj_type, ownerId):
        self.name = name
        self.proj_type = proj_type
        self.ownerId = ownerId
        session.add(self)
        try:
            session.commit()
        except exc.IntegrityError as err:
            session.rollback()
            if "UNIQUE constraint failed: projects.name" in str(err):
                sys.stderr.write("error, project name already exists (%s)\n" % name)
            elif "FOREIGN KEY constraint failed" in str(err):
                sys.stderr.write("supplier does not exist\n")
            else:
                sys.stderr.write("unknown error project user")


    def __repr__(self):
        return("<Project(ownerId='%d', name='%s', type='%s')>" % (self.ownerId, self.name, self.proj_type))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
if __name__ == "__main__":
    print("Starting...") 
    mytag = Tag("all")
    linuxTag = Tag("linux", mytag)
    linuxTag = Tag("windows", mytag)
    linuxTag = Tag("bsd", mytag)

    print(session.query(Tag).all())
    #mytag.child = Tag("linux")
    #myuser = User("Jack", "Jack McKenna", "Hulto")
    #myproject = Project("budlight", "private", myuser.id)
    #myproject = Project("opta", "public", myuser.id)
    #myproject = Project("genny", "public", myuser.id)
    #print("HERE")
    #print(session.query(User).all())
    #print(session.query(Project).all())
    #userId = int(session.query(User.id).filter_by(nickname="Hulto").all()[0][0])
    #for i in session.query(Project).filter_by(ownerId=userId).all():
    #    print(repr(i))
#    print(session.query(Project).filter_by(ownerId=myuser.id).all())
    #print(session.query(Project).filter_by(ownerId=myuser.id).all())
    


