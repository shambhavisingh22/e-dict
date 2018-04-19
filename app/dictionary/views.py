from . import dict
from flask import jsonify,request
from app import es
import uuid
import pytz
from datetime import datetime

def getCurrentTime():             #funtion to add current time and date
  tz = pytz.timezone('Asia/Calcutta')
  return datetime.now(tz)

@dict.route('/', methods=['GET'])
def test():
    return jsonify({"msg" : "welcome to my dictionary"})

@dict.route('/add_word',methods=['POST'])
def add_word():
    requestObject= request.get_json()    #in case of post get_json()
    try:
        if "id" not in requestObject:
            #if id comes from front end then it is update and if not then it is addnew

            requestObject['date_added']=getCurrentTime()
            requestObject['date_modified']=getCurrentTime()
            idn = str(uuid.uuid4()) #this generates a new random id and converts it to string
            es.index(index = "dict_word",doc_type="dictionary",id=idn,body=requestObject)  #create a new entry,it means add
            return jsonify({"response":"success","id":idn})
        else:

            requestObject['date_modified'] = getCurrentTime()
            es.update(index="dict_word",doc_type="dictionary",id=requestObject["id"],body={"doc":requestObject})
            return jsonify({"response":"success","id":requestObject["id"]})
    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})

@dict.route('/get_word',methods=['GET'])
def get_word():
    id= request.args['id']   #in case of get(args[])
    try:
        result=es.get("dict_word", doc_type="dictionary",id=id)
        print result
        if result["found"]=="false":
            return jsonify({"response":"failure"})
        else:
            result = result["_source"]
            return jsonify({"response":"success", "data":result})
    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})


def init_comment_post(app):
   # es.indices.delete("dict_word", ignore=[400, 404])

    body={

        "mappings" :
            {
                "dictionary" :
                    {
                        "properties" :
                            {
                               "word":
                                   {
                                       "type":"text"
                                   },
                                "meaning":
                                    {
                                        "type": "text"
                                    },
                                "synonym":
                                    {
                                        "type": "text"
                                    },
                                "antonym":
                                    {
                                        "type": "text"
                                    },
                                "date":
                                    {
                                        "type": "date"
                                    },
                                "date_added":
                                    {
                                        "type": "date"
                                    },
                                "date_modified":
                                    {
                                        "type": "date"
                                    },
                                "user_fav":
                                    {
                                        "type": "nested",
                                        "properties" :{
                                            "mail_id" :{
                                                "type":"text"
                                            }
                                        }
                                    }
                            }
                    }

            }

    }

    print "joi"

    es.indices.create("dict_word",body=body,ignore=400)

@dict.route('/delete_word',methods=['GET'])
def delete_word():
    idn= request.args['id']   #in case of get(args[])
    try:
        es.delete("dict_word", doc_type="word",id=idn)
        return jsonify({"response":"success"})
    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})


@dict.route('/match_all',methods=['GET'])
def match_all():
    try:
        query ={
            "query": {
                "match_all": {}
            }
        }
        result = es.search(index = "dict_word", doc_type="word",body=query)

        res = result["hits"]["hits"]
        filtered_result =[]
        for i in res :
            filtered_result.append(i["_source"])

        return jsonify({"response":"success", "data":filtered_result})
    except Exception as e:
        print str(e)
        return jsonify({"response":"failure","error":str(e)})