from flask import Flask, Response, json, request, Blueprint
from main import DataslateDBContext

campaign = Blueprint('campaign', __name__)

context = DataslateDBContext("campaign")


# Campaign
@campaign.route('/<string:owner>/<string:name>', methods=['GET'])
def get_campaign(name, owner):
    filters = dict({
        "owner": owner,
        "name": name
    })
    response = context.read(filters)
    response_status = 200
    if not response:
        response = get_available_campaigns(owner)
        response_status = response['status']
        del response['status']
    return Response(response=json.dumps(response),
                    status=response_status,
                    mimetype='application/json')


def get_available_campaigns(owner):
    response = context.read({"owner": owner})
    output = []
    for c in response:
        output.append({'name': c['name']})

    return {'available': output, 'status': 204}


@campaign.route('/<string:owner>/<string:name>', methods=['POST'])
def add_campaign(name, owner):
    addition = {
        "owner": owner,
        "name": name
    }
    response = context.create(addition)
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
    response = context.read(filters)
    response_status = 200
    if not response:
        response = get_available_campaigns(owner)
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
    players_data = request.json
    response = context.add_to_array_unique('players', players_data, filters)
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
    response = context.remove_from_array('players', 'username', players_data, filters)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')
