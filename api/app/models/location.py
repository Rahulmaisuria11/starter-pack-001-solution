from app import db


# I already inherited the class with db.Model, so you don't have to do anything else here
class Location(db.Model):
    """
    Create a model of a Location with some relevant columns, for example,
    name, country, team, custodian, etc.
    
    Needs a one-to-many relationship with the Engineer table.
    Since we would like for one Engineer have multiple Locations as custodian.

    As optional, you can create a method __repr__ 
    """
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    country = db.Column(db.String(128))
    team = db.Column(db.String(128))

    """
    One to Many Relationships
    """
    engineer_id = db.Column(
        db.Integer, db.ForeignKey("engineer.id", ondelete="CASCADE"),
        unique=False, nullable=False
    )
    custodian = db.relationship("Engineer",
                                back_populates="locations")

    def __init__(self, name, country, team, engineer_id,):
        self.name = name
        self.country = country
        self.team = team
        self.engineer_id = engineer_id

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
            'country': self.country,
            'team': self.team,
            # OPTIONAL: we can omit the engineer_id if we are getting the name:
            'engineer_id': self.engineer_id,
            'custodian': self.custodian.name
        }
