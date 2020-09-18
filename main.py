import logging as log
import ast
from flask import json
from pymongo import MongoClient
from bson import Binary
from bson.json_util import dumps
from bson.objectid import ObjectId


class DataslateDBContext:
    def __init__(self, collection_name):
        self.client = MongoClient("mongodb://dataslate-data-access:test@huxx-dev-shard-00-00.5n2pg.gcp.mongodb.net"
                                  ":27017,huxx-dev-shard-00-01.5n2pg.gcp.mongodb.net:27017,"
                                  "huxx-dev-shard-00-02.5n2pg.gcp.mongodb.net:27017/dataslate?ssl=true&replicaSet"
                                  "=atlas-n977x7-shard-0&authSource=admin&retryWrites=true&w=majority")

        database = "dataslate"  # data['database']
        collection = collection_name
        cursor = self.client[database]
        self.collection = cursor[collection]
        # self.data = data
        # self.filter = data['filter']

    def create(self, document):
        response = self.collection.insert_one(document)
        output = {'Status': 'Successfully Inserted', 'Document_ID': str(response.inserted_id)}
        return output

    def read(self, filters):
        documents = self.collection.find(filters)
        output = []
        for data in documents:
            data_dict = {}
            for item in data:
                if item == '_id':
                    raw_id_dict = ast.literal_eval(dumps(data[item]))
                    for v in raw_id_dict:
                        data_dict[v] = raw_id_dict[v]
                else:
                    data_dict[item] = data[item]
            output.append(data_dict)
        return output

    def update(self, updates, filters):
        updated_data = {"$set": updates}
        response = self.collection.update_one(filters, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, filters):
        response = self.collection.delete_one(filters)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

    def add_to_array_unique(self, array_name, inserts, filters):
        response = self.collection.update_one(filters, {'$addToSet': {array_name: {'$each': inserts}}})
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def update_array_matching_elements(self, array_name, update, filters):
        mod_count = 0
        # for k,v in update:
        # response = self.collection.update_one(filters, {'$set': {array_name +'.$[i].' + update['field']: array_match['filter']}}, {arrayFilters: [{“i.b”: 0}]})
        #     mod_count = mod_count + response.modified_count
        # output = {'Status': 'Successfully Removed' if mod_count > 0 else "Nothing was removed."}
        # return output

    def remove_from_array(self, array_name, array_field, removes: [], filters):
        response = self.collection.update_one(filters, {'$pull': {array_name: {array_field: {'$in': removes}}}})
        output = {'Status': 'Successfully Removed' if response.modified_count > 0 else "Nothing was removed."}
        return output
