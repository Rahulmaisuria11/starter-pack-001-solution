from flask import Flask, render_template, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config

db = SQLAlchemy()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate = Migrate(app, db)

    # don't forget to import the class Engineer here, so uncomment the line below:
    from app.models.engineer import Engineer
    from app.models.location import Location
    from app.models.roles import Roles
    from app.models.roles_secondary import RolesSecondary

    """
    Engineer Routes
    """

    @app.route('/engineers', methods=['GET'])
    def get_engineers():
        """
        1. create an empty list to store the formatted data
        2. create a variable that will store the query for all engineers
        3. create a loop that will iterate through all engineers
        4. in the for loop, append each engineer to the empty list
        :return: a JSON object with the response and status
        """
        data = []
        engineers = Engineer.query.all()

        if len(engineers) == 0:
            return jsonify({
                'message': 'No engineers found',
                'status': 404
            })

        for engineer in engineers:
            data.append(engineer.format())

        # using list comprehensions:
        # data = [engineer.format() for engineer in engineers]

        return jsonify({
            'engineers': data,
            'message': 'Successfully fetched engineers',
            'status': 200
        })

    @app.route('/engineer/<int:_id>', methods=['GET'])
    def get_engineer(_id):
        """
        1. get the request
        2. query the database and filter by the id, to check if it has any
        3. if there isn't any, return a response stating that there is none
        4. create a variable with the Engineer class and add your variables
        :return: a JSON object with the response and status
        """

        engineer = Engineer.query.filter_by(id=_id).first()

        if engineer is None:
            return jsonify({
                'message': 'Could not find Engineer',
                'status': 404
            })

        return jsonify({
            'message': 'Successfully fetched engineer',
            'engineer': engineer.format(),
            'status': 200,
        })

    @app.route('/new_engineer', methods=['POST'])
    def new_engineer():
        """
        1. get the request
        2. query the database and filter by the username, to check if it has any
        3. if there isn't any, create the engineer, otherwise, return a response stating that there is already one
        4. create a variable with the Engineer class and add your variables
        5. add the variable to the db and commit the changes.
        :return: a JSON object with the response and status
        """

        form = request.get_json(force=True)

        if Engineer.query.filter_by(username=form['username']).first() is not None:
            return jsonify({
                'message': 'Engineer already exists',
                'status': 400,
            })

        try:
            engineer = Engineer(
                name=form['name'],
                username=form['username'],
                email=form['email'],
            )

            roles = [Roles.query.filter_by(name=role['name']).first() for role in form['roles']]
            engineer.roles = roles
            engineer.insert()

        except Exception as error:
            return jsonify({
                'message': 'There was an error creating the engineer',
                'error': str(error),
                'status': 500,
            })

        return jsonify({
            'message': 'Successfully created the engineer',
            'engineer': engineer.format(),
            'status': 200,
        })

    @app.route('/update_engineer/<_id>', methods=['PATCH'])
    def update_engineer(_id):
        """
        1. get the request
        2. query the database and filter by the username, to check if it has any
        3. if there isn't any, create the engineer, otherwise, return a response stating that there is already one
        4. update the values on the engineer
        5. commit the changes
        :param _id: id of the engineer to be updated
        :return: a JSON object with the response and status
        """
        form = request.get_json(force=True)
        engineer = Engineer.query.filter_by(id=_id).first()

        if engineer is None:
            return jsonify({
                'message': 'Engineer not found',
                'status': 404,
            })

        try:
            engineer.name = form['name']
            engineer.username = form['username']
            engineer.email = form['email']

            # delete existing roles:
            roles_delete = RolesSecondary.query.filter_by(engineer_id=_id)
            roles_delete.delete()

            # add new roles:
            roles = [Roles.query.filter_by(name=role['name']).first() for role in form['roles']]
            engineer.roles = roles

            engineer.update()

        except Exception as error:
            return jsonify({
                'message': 'There was an error updating the engineer',
                'error': str(error),
                'status': 500,
            })

        return jsonify({
            'response': 'Successfully updated the engineer',
            'engineer': engineer.format(),
            'status': 200,
        })

    @app.route('/delete_engineer/<_id>', methods=['DELETE'])
    def delete_engineer(_id):
        """
        1. get the request
        2. query the database and filter by the username, to check if it has any
        3. if there isn't any, create the engineer, otherwise, return a response stating that there is already one
        4. delete the engineer and commit the changes
        :param _id: id of the engineer to be deleted
        :return: a JSON object with the response and status
        """
        engineer = Engineer.query.filter_by(id=_id).first()

        if engineer is None:
            return jsonify({
                'message': 'Engineer not found',
                'status': 404,
            })

        deleted_engineer = engineer.format()
        engineer.delete()

        return jsonify({
            'engineer': deleted_engineer,
            'response': 'Successfully deleted the engineer',
            'status': 200,
        })

    """
    Locations Routes
    """

    @app.route('/locations', methods=['GET'])
    def get_locations():
        locations = Location.query.all()

        if len(locations) == 0:
            return jsonify({
                'message': 'No locations found',
                'status': 404
            })

        # using list comprehensions:
        data = [location.format() for location in locations]

        return jsonify({
            'locations': data,
            'message': 'Successfully fetched locations',
            'status': 200
        })

    @app.route('/location/<int:_id>', methods=['GET'])
    def get_location(_id):
        location = Location.query.filter_by(id=_id).first()

        if location is None:
            return jsonify({
                'message': 'Could not find that Location',
                'status': 404
            })

        return jsonify({
            'message': 'Successfully fetched location',
            'engineer': location.format(),
            'status': 200,
        })

    @app.route('/new_location', methods=['POST'])
    def new_location():
        form = request.get_json(force=True)

        if Location.query.filter_by(name=form['name']).first() is not None:
            return jsonify({
                'message': 'Location already exists',
                'status': 400,
            })

        try:
            engineer = Engineer.query.filter_by(username=form['engineer_id']['username']).first()

            if engineer is None:
                return jsonify({
                    'message': 'A location must have a valid engineer',
                    'status': 400,
                })

            location = Location(
                name=form['name'],
                country=form['country'],
                team=form['team'],
                engineer_id=engineer.id,
            )

            location.insert()

        except Exception as error:
            return jsonify({
                'message': 'There was an error creating the location',
                'error': str(error),
                'status': 500,
            })

        return jsonify({
            'message': 'Successfully created the location',
            'engineer': location.format(),
            'status': 200,
        })

    @app.route('/update_location/<int:_id>', methods=['PATCH'])
    def update_location(_id):
        form = request.get_json(force=True)
        location = Location.query.filter_by(id=_id).first()

        if location is None:
            return jsonify({
                'message': 'Location not found',
                'status': 404,
            })

        try:
            engineer = Engineer.query.filter_by(username=form['engineer_id']['username']).first()

            location.name = form['name']
            location.country = form['country']
            location.team = form['team']
            location.engineer_id = engineer.id

            location.update()

        except Exception as error:
            return jsonify({
                'message': 'There was an error updating the location',
                'error': str(error),
                'status': 500,
            })

        return jsonify({
            'response': 'Successfully updated the location',
            'engineer': location.format(),
            'status': 200,
        })

    @app.route('/delete_location', methods=['DELETE'])
    def delete_location(_id):
        location = Location.query.filter_by(id=_id).first()

        if location is None:
            return jsonify({
                'message': 'Engineer not found',
                'status': 404,
            })

        deleted_location = location.format()
        location.delete()

        return jsonify({
            'location': deleted_location,
            'response': 'Successfully deleted the location',
            'status': 200,
        })

    """
    Roles Routes
    """

    @app.route('/roles', methods=['GET'])
    def get_roles():
        roles = Roles.query.all()

        if len(roles) == 0:
            return jsonify({
                'message': 'No roles found',
                'status': 404
            })

        data = [role.format() for role in roles]

        return jsonify({
            'engineers': data,
            'message': 'Successfully fetched roles',
            'status': 200
        })

    @app.route('/role/<int:_id>', methods=['GET'])
    def get_role(_id):
        role = Roles.query.filter_by(id=_id).first()

        if role is None:
            return jsonify({
                'message': 'Could not find that Role',
                'status': 404
            })

        return jsonify({
            'message': 'Successfully fetched role',
            'engineer': role.format(),
            'status': 200,
        })

    @app.route('/new_role', methods=['POST'])
    def new_role():
        form = request.get_json(force=True)

        if Roles.query.filter_by(name=form['name']).first() is not None:
            return jsonify({
                'message': 'Role already exists',
                'status': 400,
            })

        try:
            role = Roles(
                name=form['name'],
                description=form['description'],
            )
            role.insert()

        except Exception as error:
            return jsonify({
                'message': 'There was an error creating the role',
                'error': str(error),
                'status': 500,
            })

        return jsonify({
            'message': 'Successfully created the role',
            'role': role.format(),
            'status': 200,
        })

    @app.route('/update_role/<int:_id>', methods=['PATCH'])
    def update_role(_id):
        form = request.get_json(force=True)
        role = Roles.query.filter_by(id=_id).first()

        if role is None:
            return jsonify({
                'message': 'Role not found',
                'status': 404,
            })

        try:
            role.name = form['name']
            role.description = form['description']
            role.update()

        except Exception as error:
            return jsonify({
                'message': 'There was an error updating the role',
                'error': str(error),
                'status': 500,
            })

        return jsonify({
            'response': 'Successfully updated the role',
            'role': role.format(),
            'status': 200,
        })

    @app.route('/delete_role/<int:_id>', methods=['DELETE'])
    def delete_role(_id):
        role = Roles.query.filter_by(id=_id).first()

        if role is None:
            return jsonify({
                'message': 'Role not found',
                'status': 404,
            })

        deleted_role = role.format()
        role.delete()

        return jsonify({
            'role': deleted_role,
            'response': 'Successfully deleted the role',
            'status': 200,
        })

    # This will allow for us to create the database on app start:
    with app.app_context():
        print('Flask starting...')
        db.create_all()

        # Create predefined roles:
        default_roles = ['Admin', 'NS', 'DS', 'GRMS']
        for default_role in default_roles:
            if Roles.query.filter_by(name=default_role).first() is None:
                current_role = Roles(name=default_role, description=default_role)
                current_role.insert()

    return app
