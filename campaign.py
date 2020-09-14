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
    print(output)
    for c in response:
        output.append({'name': c['name']})

    return {'available': output, 'status': 404}
