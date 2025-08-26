from app import db


# I already inherited the class with db.Model, so you don't have to do anything else here
class RolesSecondary(db.Model):
    """
    Create a secondary table for a many-to-many relationship model.

    It needs to be done since an Engineer can have multiple roles
    and multiple roles might be assigned to an Engineer.
    """
    __tablename__ = 'roles_secondary'

    id = db.Column(db.Integer, primary_key=True)
    engineer_id = db.Column(db.Integer,
                            db.ForeignKey("engineer.id",
                                          ondelete="CASCADE"),
                            nullable=False)
    role_id = db.Column(db.Integer,
                        db.ForeignKey("roles.id",
                                      ondelete="CASCADE"),
                        nullable=False)

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
