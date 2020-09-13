import logging as log

from pymongo import MongoClient


class MongoAPI:
    def __init__(self, data):
        self.client = MongoClient("mongodb://dataslate-data-access:test@huxx-dev-shard-00-00.5n2pg.gcp.mongodb.net"
                                  ":27017,huxx-dev-shard-00-01.5n2pg.gcp.mongodb.net:27017,"
                                  "huxx-dev-shard-00-02.5n2pg.gcp.mongodb.net:27017/dataslate?ssl=true&replicaSet"
                                  "=atlas-n977x7-shard-0&authSource=admin&retryWrites=true&w=majority")

        database = data['database']
        collection = data['collection']
        cursor = self.client[database]
        self.collection = cursor[collection]
        self.data = data
        self.filter = data['Filter']

    def read(self):
        documents = self.collection.find(self.filter)
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted', 'Document_ID': str(response.inserted_id)}
        return output

    def update(self):
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(self.filter, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self):
        response = self.collection.delete_one(self.filter)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output
