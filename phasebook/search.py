from flask import Blueprint, jsonify, request
from typing import List
import json

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")

class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(CustomJSONEncoder, self).__init__(*args, **kwargs)
        self.sort_keys = False

bp.json_encoder = CustomJSONEncoder


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!
    if not args:
        return USERS

    results = []

    id = args.get('id', None)
    name = args.get('name', None)
    age = args.get('age', None)
    occupation = args.get('occupation', None)

    [results.append(user) if id and str(user["id"]) == id else None for user in USERS]
    [results.append(user) if name and name.lower() in user["name"].lower() else None for user in USERS]
    [results.append(user) if age and age.isdigit() and abs(int(user["age"]) - int(age)) <= 1 else None for user in USERS]
    [results.append(user) if occupation and occupation.lower() in user["occupation"].lower() else None for user in USERS]

    # Remove duplicate users
    results = list({user["id"]: user for user in results}.values())

    return results
