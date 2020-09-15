from flask import Flask, Response, json, request, Blueprint
from main import DataslateDBContext

campaign = Blueprint('campaign', __name__)

context = DataslateDBContext("campaign")


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

    return {'available': output, 'status': 404}


@campaign.route('/<string:owner>/<string:name>/players', methods=['GET'])
def get_campaign_players(name, owner):
    filters = dict({
        "owner": owner,
        "name": name
    })
    response = context.read(filters)
    response_status = 200
    players = []
    if not response:
        response = get_available_campaigns(owner)
        response_status = response['status']
        del response['status']
    else:
        for x in response:
            players = x['players']
    return Response(response=json.dumps(players),
                    status=response_status,
                    mimetype='application/json')


@campaign.route('/<string:owner>/<string:name>/players', methods=['POST'])
def add_campaign_players(name, owner):
    filters = dict({
        "owner": owner,
        "name": name
    })
    players_data = request.json
    players = []
    for x in players_data:
        displayname = x['displayname']
        username = x['username']
        players.append("{displayname: '" + displayname + "',username:'" + username + "'}")

    print(players)
    response = context.add_to_array('players', players, filters)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')
