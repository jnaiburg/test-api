import requests
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Resource, Api, reqparse

parser = reqparse.RequestParser()

app = Flask(__name__)
api = Api(app)

class Predict(Resource):
    def post(self):
        parser.add_argument('id', type=str)
        parser.add_argument('mriId', type=str)
        parser.add_argument('visit', type=int)
        parser.add_argument('mrDelay', type=int)
        parser.add_argument('gender', type=str)
        parser.add_argument('hand', type=str)
        parser.add_argument('age', type=int)
        parser.add_argument('educ', type=int)
        parser.add_argument('SES', type=int)
        parser.add_argument('MMSE', type=int)
        parser.add_argument('CDR', type=int)
        args = parser.parse_args()

        API_KEY = "yaNBlVmvMmczXo5dUJMPtJ7J0Y_bg4_ml2opIsQQZy-r"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                             API_KEY,
                                                                                         "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]

        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

        # NOTE: manually define and pass the array(s) of values to be scored in the next line
        payload_scoring = {"input_data": [
            {"fields": ["Subject ID", "MRI ID", "Visit", "MR Delay", "M/F", "Hand", "Age", "EDUC", "SES", "MMSE", "CDR"],
             "values": [[args['id'], args['mriId'], args['visit'], args['mrDelay'], args['gender'], args['hand'], args['age'], args['educ'], args['SES'], args['MMSE'], args['CDR']]]}]}

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/deploymenttest/predictions?version=2022-04-21',
            json=payload_scoring,
            headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        response_scoring_object = response_scoring.json()
        value = response_scoring_object['predictions'][0]['values'][0][0]
        return {
            "return_value": value
        }


api.add_resource(Predict, '/')

if __name__ == '__main__':
    app.run(debug=True)