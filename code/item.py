from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from flask import Flask, request
import sqlite3


class ItemData(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @classmethod
    def get_item_by_name(cls, name):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        print(name)
        query = "SELECT * from items WHERE name=?"
        results = cursor.execute(query, (name,))
        result = results.fetchone()
        connection.close()
        if result:
            return cls(*result)
        else:
            return None

    @classmethod
    def get_all_item(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        results = cursor.execute(query)

        items = []
        for result in results:
            item = {'name': result[0], 'price': result[1]}
            items.append(item)
        connection.close()
        return items


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True, help="This filed can not be empty")

    @jwt_required()
    def get(self, name):
        item = ItemData.get_item_by_name(name)
        return {"item": item.__dict__}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        data = Item.parser.parse_args()
        if ItemData.get_item_by_name(name):
            return {"message": "Item already added"}, 400

        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {"message": "Error occured"}, 500

        return item, 201

    @jwt_required()
    def delete(self, name):
        item = ItemData.get_item_by_name(name)
        if item is None:
            return {"message": "No record found"}, 404

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        print(query)
        connection.commit()
        connection.close()
        if result:
            return {"message": "Item deleted successfully"}, 201
        else:
            return {"message": "Failed to add item"}, 400

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemData.get_item_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        print("New PRICE", data['price'])
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "Error occured while inserting"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "Error occured while updating"}, 500

        return updated_item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES(?,?)"

        result = cursor.execute(query, (item['name'], item['price']))
        print(query)
        connection.commit()
        connection.close()
        if result:
            return {"message": "Item added successfully"}, 201
        else:
            return {"message": "Failed to add item"}, 400

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        print("New PRICEssss", item['price'])
        result = cursor.execute(query, (item["price"],item["name"]))
        if result:
            print("SUCCESS")
        else :
            print("FAILURE")
        connection.commit()
        connection.close()


class Items(Resource):
    # @jwt_required
    def get(self):
        items = ItemData.get_all_item()
        return {'items': items}
