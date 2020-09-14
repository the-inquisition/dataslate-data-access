from flask import Flask, Response, json, request, Blueprint
from main import DataslateDBContext

campaign = Blueprint('campaign', __name__)

context = DataslateDBContext("campaign")


@campaign.route('/<string:name>/<string:owner>', methods=['GET'])
def get_campaign(name, owner):
    filters = {
        "name": name,
        "owner": owner
    }
    response = context.read(filters)
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')
