from flask import Flask, Response, json, request
from flask_cors import CORS, cross_origin
from main import DataslateDBContext
from campaign import campaign
from user import user

app = Flask(__name__)
app.register_blueprint(campaign)
app.register_blueprint(user)
# app.config['CORS-HEADERS'] = 'Content-Type'

CORS(app)


@app.route('/api')
# @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def base():
    return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')


# # GET USAGE
# # {
# #   "database": "dataslate",
# #   "collection": "data_entries"
# # }
# @app.route('/mongodbf', methods=['POST'])
# def mongo_read():
#     data = request.json
#     if data is None or data == {}:
#         return Response(response=json.dumps({"Error": "Please provide connection information"}),
#                         status=400,
#                         mimetype='application/json')
#     obj1 = DataslateDBContext(data)
#     response = obj1.read("asdf")
#     return Response(response=json.dumps(response),
#                     status=200,
#                     mimetype='application/json')
#
#
# # POST USAGE
# # {
# #   "database": "dataslate",
# #   "collection": "data_entries",
# #   "Document": {
# #     "entry": "this is the entry",
# #     "etc": "this is just another entry"
# #   }
# # }
# @app.route('/mongodb', methods=['POST'])
# def mongo_write():
#     data = request.json
#     if data is None or data == {} or 'document' not in data:
#         return Response(response=json.dumps({"Error": "Please provide connection information"}),
#                         status=400,
#                         mimetype='application/json')
#     obj1 = DataslateDBContext(data)
#     response = obj1.write(data)
#     return Response(response=json.dumps(response),
#                     status=200,
#                     mimetype='application/json')
#
#
# # PUT USAGE
# # {
# #   "database": "dataslate",
# #   "collection": "user",
# #   "Filter": {
# #     "username": "huxx"
# #   },
# #   "DataToBeUpdated": {
# #     "email": "eh@example.com",
# #     "Age": 26
# #   }
# # }
# @app.route('/mongodb', methods=['PUT'])
# def mongo_update():
#     data = request.json
#     if data is None or data == {} or 'updates' not in data:
#         return Response(response=json.dumps({"Error": "Please provide connection information"}),
#                         status=400,
#                         mimetype='application/json')
#     obj1 = DataslateDBContext(data)
#     response = obj1.update()
#     return Response(response=json.dumps(response),
#                     status=200,
#                     mimetype='application/json')
#
#
# # DELETE USAGE
# # {
# #     "database": "dataslate",
# #     "collection": "game",
# #     "Filter": {
# #         "name": "terror of tephaine"
# #     }
# # }
# @app.route('/mongodb', methods=['DELETE'])
# def mongo_delete():
#     data = request.json
#     if data is None or data == {} or 'filter' not in data:
#         return Response(response=json.dumps({"Delete_Error": "Filter not valid or no information found"}))
#     obj1 = DataslateDBContext(data)
#     response = obj1.delete()
#     return Response(response=json.dumps(response),
#                     status=200,
#                     mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
