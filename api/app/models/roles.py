from app import db


# I already inherited the class with db.Model, so you don't have to do anything else here
class Roles(db.Model):
    """
    Create a model of roles with some relevant columns, for example,
    name and description of the role

    Needs a many-to-many relationship with the Engineer table.
    Since we would like for one Engineer have multiple roles and vice-versa.

    As optional, you can create a method __repr__
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(128))

    """
    Many to Many relationships
    """
    engineers = db.relationship("Engineer",
                                lazy=True,
                                back_populates="roles",
                                secondary="roles_secondary",
                                cascade="all, delete")

    def __init__(self, name, description,):
        self.name = name
        self.description = description

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
            'description': self.description,
            'engineers': [engineer.name for engineer in self.engineers]
        }
