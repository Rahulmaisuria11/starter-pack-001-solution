import json

from app import db


# I already inherited the class with db.Model, so you don't have to do anything else here
class Engineer(db.Model):
    """
    Create a model of an Engineer with some relevant columns, for example,
    name, username, email, etc.

    It needs a relationship with the roles model as many-to-many
    
    As optional, you can create a method __repr__ to return a string with the details
    of the Engineer.  
    """
    __tablename__ = 'engineer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))

    """
    One to Many relationships
    """
    locations = db.relationship("Location",
                                back_populates="custodian",
                                foreign_keys='Location.engineer_id',
                                lazy="dynamic",
                                cascade="all, delete")

    """
    Many to Many relationships
    """
    roles = db.relationship("Roles",
                            lazy=True,
                            back_populates="engineers",
                            secondary="roles_secondary",
                            cascade="all, delete")

    def __init__(self, name, username, email,):
        self.name = name
        self.username = username
        self.email = email

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'locations': [location.name for location in self.locations],
            'roles': [role.format() for role in self.roles]
        }
