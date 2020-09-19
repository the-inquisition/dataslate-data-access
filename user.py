from bson import ObjectId
from flask import Flask, Response, json, request, Blueprint
from main import DataslateDBContext

user = Blueprint('user', __name__)

user_collection = DataslateDBContext("user")


@user.route('/<string:username>', methods=['GET'])
def get_user(username):
    user_filter = {'username': username}
    response = user_collection.read(user_filter)
    if not response:
        return Response(response=json.dumps('User not found'),
                        status=204,
                        mimetype='application/json')
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@user.route('/<string:username>', methods=['POST'])
def create_user(username):
    new_user = {
        'username': username,
        'email': request.json['email'],
        'password': '_placeholder_'
    }
    response = user_collection.create(new_user)
    return Response(response=json.dumps(response),
                    status=201,
                    mimetype='application/json')

# @user.route('/<string:username>', methods=['PUT'])
# def update_user(username):
#     update_user ={
#         'username':username
#     }
#     updated_email =
#     if
#     updates={
#         'email':request.json['email']
#     }
#
# @user.route('/<string:username>', methods=['DELETE'])
# def delete_user()