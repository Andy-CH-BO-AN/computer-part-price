from pymongo import MongoClient

client = MongoClient("mongodb+srv://digbick:digbick@cluster0dot0.ym7ee.mongodb.net/?retryWrites=true&w=majority")

id = '_id'


def create_db_collection(db_name, collection_name):
    db_list = client.list_database_names()

    if db_name in db_list:
        print(f"The {db_name} exists")
    else:
        mydb = client[db_name]

        collist = mydb.list_collection_names()
        if "customers" in collist:
            print("The collection exists.")
        else:
            mydb.create_collection(collection_name)
            print(query_db(), find_collection(db_name))


def create_db_collection2(db_name, collection_name, data):
    client[db_name][collection_name].insert_one(data)


def delete_db():
    pass


def query_db():
    dblist = client.list_database_names()
    return dblist


def count_collection(db_name, collection_name):
    # 看看有幾筆資料
    db = client.get_database(db_name)
    records = db[collection_name]
    count_doc = records.count_documents({})
    return f"筆數(count data)：{count_doc}"


def insert_collection(db_name, collection_name, data):
    db = client.get_database(db_name)
    records = db[collection_name]
    data[id] = get_sequence(db_name, collection_name)
    records.insert_one(data)


def insert_collection_multiple_data(db_name, collection_name, data):
    db = client.get_database(db_name)
    records = db[collection_name]
    for i in range(len(data)):
        if i == 0:
            data[i][id] = get_sequence(db_name, collection_name)
        else:
            data[i][id] = data[i - 1][id] + 1

    records.insert_many(data)


def find_collection(db_name, collection_name):
    db = client.get_database(db_name)
    records = db[collection_name]
    return list(records.find())


def find_collection_single(db_name, collection_name, data):
    db = client.get_database(db_name)
    records = db[collection_name]
    return list(records.find(data))


def update_collection(db_name, collection_name, data, updatedata):
    db = client.get_database(db_name)
    records = db[collection_name]
    # records.update_one({id: 10}, {'$set': {'name': 'tiger'}})
    records.update_one(data, {'$set': updatedata})


def delete_collection(db_name, collection_name):
    db = client.get_database(db_name)
    records = db[collection_name]
    records.delete_many({})
    # records.delete_many({'<column_name>': '<what_you_want>'})


def get_sequence(db_name, collection_name):
    if len(find_collection(db_name, collection_name)) > 0:
        return int(find_collection(db_name, collection_name)[-1][id]) + 1
    else:
        return 1


new_cat = {'name': "caracal",
           'dick': "20"}

new_cats = [
    {'name': "lynx",
     'dick': "21"},
    {
        'name': "bobcat",
        'dick': {'dick': "22", "dik": "23"},
    }
]

# print(find_collection_single('test_meow','serval',{id:7}))
# cat_update = {'name': 'tiger'}
# delete_serval_db()


# for i in range(len(query_db())):
#     print(i, query_db()[i])
# db_name = query_db()[int(input('請輸入資料庫號碼:'))]
# print(db_name)
print(find_collection_single('test_meow', 'serval', {'_id': 4}))
# create_db_collection('dbtest2', 'collectiontest')
