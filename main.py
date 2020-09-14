import logging as log

from flask import json
from pymongo import MongoClient


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

    def read(self, filters):
        documents = self.collection.find(filters)
        output = [{item: data[item] for item in data} for data in documents]
        print(output)
        return output

    def write(self, document):
        response = self.collection.insert_one(document)
        output = {'Status': 'Successfully Inserted', 'Document_ID': str(response.inserted_id)}
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
