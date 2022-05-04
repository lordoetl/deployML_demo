# Load libraries

import pandas as pd
import tensorflow as tf
import keras
from keras.models import load_model
import json
from json import JSONEncoder
import numpy
from flask import Flask, request, jsonify

#This function is used to convert the NN prediction to JSON
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

# instantiate flask 
app = Flask(__name__)



# define a predict function as an endpoint 
@app.route("/predict", methods=["GET","POST"])
def predict():

    #get the message from the POST (Could put test here to verify 
    # incoming data is correct format i.e. the right number of arguments)
    params = request.json
    
    print(f"prams are: {params}")
    out='no params detected'
    if (params != None):
        #create dataframe from data
        x=pd.DataFrame.from_dict(params)
        #One Hot Encode
        x=pd.get_dummies(x)
        #This was put here to handle extra get-dummies columns
        # Doing better prework would allow you to skip these next 2 lines
        model_columns = ['Age', 'Embarked_C', 'Embarked_Q', 'Embarked_S', 
        'Sex_male'] 
        # This line will fill any missing column with a 0.  Care should be taken that
        # won't affect your output
        x= x.reindex(columns=model_columns, fill_value=0)

        # print ('Model columns loaded')
        
        data=model.predict(x)

    # return a response in json format 
        out=json.dumps(data, cls=NumpyArrayEncoder)
        # out="no params sent"
    return jsonify(out)  

    # The output will be numeric (floats), you may need to build,
    # a translating function here to make that output meaningful.
    # for answer in out:
    #   if answer > .5:
    #       return ("True")    
    #   else:
    #      return("False")

# start the flask app, allow remote connections 
if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 12345 # If you don't provide any port the port will be set to 12345

    model = load_model('example2.h5')
    print ('Model loaded')


    app.run(port=port, debug=True)