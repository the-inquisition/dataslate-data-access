from bson import ObjectId
from flask import Flask, Response, json, request, Blueprint
from main import DataslateDBContext
import user

campaign = Blueprint('campaign', __name__)

campaign_collection = DataslateDBContext("campaign")


# Campaign
@campaign.route('/<string:owner>/<string:name>', methods=['GET'])
def get_campaign(name, owner):
    filters = dict({
        "owner": owner,
        "name": name
    })
    response = campaign_collection.read(filters)
    response_status = 200
    if not response:
        response = get_owners_campaigns(owner)
        response_status = response['status']
        del response['status']
    return Response(response=json.dumps(response),
                    status=response_status,
                    mimetype='application/json')


def get_owners_campaigns(owner):
    response = campaign_collection.read({"owner": owner})
    output = []
    for c in response:
        output.append({'name': c['name']})

    return {'available': output, 'status': 204}


@campaign.route('/<string:owner>/<string:name>', methods=['POST'])
def add_campaign(name, owner):
    new_campaign = {
        "owner": owner,
        "name": name
    }
    response = campaign_collection.create(new_campaign)
    return Response(response=json.dumps(response),
                    status=201,
                    mimetype='application/json')


@campaign.route('/<string:username>/campaigns', methods=['GET'])
def get_available_campaigns(username):
    filters = {'$or': [{'owner': username}, {'players.username': username}]}
    response = campaign_collection.read(filters)
    if not response:
        return Response(response=json.dumps({'No available campaigns'}),
                        status=204,
                        mimetype='application/json')
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


# Players
@campaign.route('/<string:owner>/<string:name>/players', methods=['GET'])
def get_campaign_players(name, owner):
    filters = dict({
        "owner": owner,
        "name": name
    })
    response = campaign_collection.read(filters)
    response_status = 200
    if not response:
        response = get_owners_campaigns(owner)
        response_status = response['status']
        del response['status']
    # response is a list, get first (and only, because of owner/name constraint)
    return Response(response=json.dumps(response[0]['players']),
                    status=response_status,
                    mimetype='application/json')


@campaign.route('/<string:owner>/<string:name>/players', methods=['POST'])
def add_campaign_players(name, owner):
    """
    USAGE/DATA/REQUEST FORM

    [{"username":"testerson","displayname":"test"},{"username":"heap","displayname":"jhon"}]

    :param name: name of campaign
    :param owner: name of campaign owner
    :return: insertion affirmation
    """
    filters = dict({
        "owner": owner,
        "name": name
    })

    players = request.json
    players_filter = []
    for p in players:
        players_filter.append(p['username'])
    players_data = user.user_collection.read({'username': {'$in': players_filter}})
    for pd in players_data:
        for p in players:
            if p['username'] == pd['username']:
                pd['displayname'] = p['displayname']
                oid = pd['$oid']
                pd['_id'] = ObjectId(oid)
                del pd['$oid']
                del pd['password']
                del pd['email']
    response = campaign_collection.add_to_array_unique('players', players_data, filters)
    if not response:
        return Response(response=json.dumps({"message": "players already added"}),
                        status=200,
                        mimetype='application/json')
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@campaign.route('/<string:owner>/<string:name>/players', methods=['PUT'])
def update_campaign_players(name, owner):
    filters = dict({
        "owner": owner,
        "name": name
    })


@campaign.route('/<string:owner>/<string:name>/players', methods=['DELETE'])
def remove_campaign_players(name, owner):
    """
    Remove players from a campaign by username

    USAGE (USERNAME ARRAY IN REQUEST BODY):

    ["testerson","heapson"]

    :param name: name of campaign
    :param owner: name of campaign owner
    :return: removal affirmation
    """
    filters = dict({
        "owner": owner,
        "name": name
    })
    players_data = request.json
    response = campaign_collection.remove_from_array('players', 'username', players_data, filters)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')
