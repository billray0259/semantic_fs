from urllib import response
import uuid
import numpy as np
import flask
from lib.encoders import TextEncoderPipeline, QueryPipeline, ExtractiveQAPipeline
from lib.util import ndarray_to_json
import json
import random
import os

from threading import Thread


app = flask.Flask(__name__)

encoder_pipeline = TextEncoderPipeline()
query_pipeline = QueryPipeline()
# qa_pipeline = ExtractiveQAPipeline()


database_file = "database.json"


def update_database(data, batch_id, database_file):
    if not os.path.exists(database_file):
        with open(database_file, "w") as f:
            json.dump({}, f, indent=4)
    
    with open(database_file, "r") as f:
        database = json.load(f)

    embeddings_dict = {}
    
    for sample in data:
        file = sample["file"]
        text = sample["text"]
        text_chunks, embeddings = encoder_pipeline(text)
        file_name_chunks, file_name_embeddings = encoder_pipeline(file)

        text_chunks.extend(file_name_chunks)
        
        if len(embeddings) == 0:
            embeddings = file_name_embeddings
        else:
            embeddings = np.concatenate([embeddings, file_name_embeddings], axis=0)

        for chunk, embedding in zip(text_chunks, embeddings):
            # hash the text to make a key
            key = str(uuid.uuid3(uuid.NAMESPACE_DNS, chunk))
            embeddings_dict[key] = {}
            embeddings_dict[key]["filename"] = file
            embeddings_dict[key]["text"] = chunk
            embeddings_dict[key]["embedding"] = ndarray_to_json(embedding)
        
    database[batch_id] = embeddings_dict

    with open(database_file, "w") as f:
        json.dump(database, f, indent=4)


def get_batch_status(batch_id, database_file):
    with open(database_file, "r") as f:
        database = json.load(f)

    return batch_id in database

'''
{
    "status": "ok",
    "data": [
        {
            "filepath": "pwd/file1",
            "text": "some text",
            "similarity": 22.11,
        },
        {
            "filepath": "pwd/file2",
            "text": "some text2",
            "similarity": 15.11,
        },
    ]
}
'''
def search_database(query, batch_id, database_file):
    with open(database_file, "r") as f:
        database = json.load(f)

    results = query_pipeline.query_embeddings_dict(query, database[batch_id])

    results = [
        {
            "filepath": result[1],
            "text": result[2],
            "similarity": str(result[3]),
        }
        for result in results
    ]

    return results
    
# accept post requests
'''
POST /data_upload/
    {
        "data": [
            {
                "file": "pwd/file1",
                "text": "some text",
            },
            {
                "file": "pwd/file2",
                "text": "some text2",
            },
        ]
    }
'''
@app.route('/data_upload/', methods=['POST', 'GET'])
def data_upload():
    # if the request is a POST request
    if flask.request.method == 'POST':
        string = str(flask.request.get_json())
        print(string[:500], "...", string[-500:])
        data = flask.request.get_json()["data"]
        # 4 digit int
        batch_id = random.randint(1000, 9999)

        # open separate thread to do the heavy lifting
        thread = Thread(target=update_database, args=(data, batch_id, database_file))
        thread.start()

        # return batch id with status 200
        return flask.jsonify({"batch_id": batch_id}), 200
    # if the request is a GET request
    else:
        # get the batch id
        batch_id = flask.request.args.get("batchId")
        # check if the batch id is in the database
        if get_batch_status(batch_id, database_file):
            # return with status 200
            return flask.jsonify({"status": "done"}), 200
        else:
            # return with status 202
            return flask.jsonify({"status": "in progress"}), 202



# search endpoint
'''
GET /search/
    {
        "batchId": "1",
        "query": "some text",
        OPTIONAL:
        "filepath": "pwd/",
    }
Return value:
    {
        "status": "ok",
        "data": [
            {
                "filepath": "pwd/file1",
                "text": "some text",
                "similarity": 22.11,
            },
            {
                "filepath": "pwd/file2",
                "text": "some text2",
                "similarity": 15.11,
            },
        ]
    }
'''
@app.route('/search/', methods=['GET'])
def search():
    data = flask.request.get_json()
    batch_id = data["batchId"]
    query = data["query"]
    filepath = data.get("filepath", None)

    if not get_batch_status(batch_id, database_file):
        # return 404
        return flask.jsonify({"status": "error", "message": "batch id not found"}), 404

    results = search_database(query, batch_id, database_file)

    # return results with status 200
    return flask.jsonify({"status": "ok", "data": results}), 200





# index page says "Semantic Search Server is Online"
@app.route('/')
def index():
    return "Semantic Search Server is Online"

if __name__ == '__main__':
    # run on 0.0.0.0:8000
    app.run(host='0.0.0.0', port=8000)