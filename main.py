import training_validation_insersion
import model_building
import predictFromModel
import prediction_validation_insertion
from DataBaseAction import database
from flask import Flask, request, render_template, jsonify
from flask import Response
import flask_monitoringdashboard as dashboard

import os
import json
from flask_cors import CORS, cross_origin
from wsgiref import simple_server


os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
# dashboard.bind(app)
# CORS(app)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods = ['POST'])
@cross_origin()
def predictRouteClient():
    try:

        if request.json is not None:
            # to test with postman application
            path = request.json['filepath']
            pred_val = prediction_validation_insertion.prediction_validation(path) #object initialization
            pred_val.predict_validation() #calling the predict_validation function
            pred = predictFromModel.prediction() #object initialization
            final_predict = pred.predictionFromModel() # Prediction in dataframe
            db_object = database.DB_define() # store the prediction into the database
            folder_path = r'C:\Users\preet\Desktop\DS\Project\Concrete Project\FinalPredictedData'
            db_object.insert_into_db('Results', folder_path = folder_path) # results are stored into the database
            return jsonify("Prediction File created at !!!" + str(folder_path),"top 5 predictions are: " , final_predict.head(5).to_json(orient='records'))

        elif request.form is not None:

            path = request.form['filepath']
            pred_val = prediction_validation_insertion.prediction_validation(path) #object initialization
            pred_val.predict_validation() #calling the predict_validation function
            pred = predictFromModel.prediction() #object initialization
            final_predict = pred.predictionFromModel() # Prediction in dataframe
            db_object = database.DB_define() # store the prediction into the database
            folder_path = r'C:\Users\preet\Desktop\DS\Project\Concrete Project\FinalPredictedData'
            db_object.insert_into_db('Results', folder_path = folder_path) # results are stored into the database
            return jsonify("Prediction File created at !!!" + str(folder_path),"\n top 5 predictions are: " , final_predict.head(5).to_json(orient='records'))

        else:
            print('nothing matched')

    except ValueError:
        return "Error Occurred! {}".format(ValueError)
    except KeyError:
        return "Error Occurred! {}".format(KeyError)
    except Exception as e:
        return "Error Occurred! {}".format(e)



@app.route("/train", methods=['POST'])
@cross_origin()
def trainRouteClient():
    try:
        if request.json['trainFolderPath'] is not None:
            path = request.json['folderPath']  # Accepting the folder path in json format
            train_valObj = training_validation_insersion.train_validation(path)  # object initialization
            train_valObj.train_validation()  # calling the training_validation function
            trainModelObj = model_building.trainModel()  # object initialization
            trainModelObj.trainingModel()  # training the model for the files in the table

    except ValueError:
        return "Error Occurred! {}".format(ValueError)
    except KeyError:
        return "Error Occurred! {}".format(KeyError)
    except Exception as e:
        return "Error Occurred! {}".format(e)
    return "Training successful!!"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()
