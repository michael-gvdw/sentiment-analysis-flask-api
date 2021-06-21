# Sentiment Analysis Flask REST API

## Project Overview

### Context

For the Open Program (Week 17 - Week 18) I will be investigating Python Flask. Flask is a micro web framework written in Python. It is used to build web applications and REST APIs. 

### Goal

The goal of this project is to create a REST API that hosts the Deep Learning Model for Sentiment Analysis created in the [tensorflow-sentiment-analysis](https://github.com/michael-gvdw/tenserflow-sentiment-analysis.git) repository. Users will be able to query the API by passing a sentence as a parameter and be provided how positive or negative the sentence is.

## Code Explanation

First the necessary imports need to specified in order to achieve the goal. The Flask related packages are imported as well as the Sentiment Analysis model. 

    from flask import Flask 
    from flask_restful import Api, Resource, reqparse, fields, marshal_with

    from model import sample_predict
    from service import categoryze_sentiment

Secondly the app and api are instaciated.

    app = Flask(__name__)
    api = Api(app)

Next we specify the arguments (parameters) that are passed in the request. Also we specify what the response body will look like.

    # arguments
    sentiment_get_args = reqparse.RequestParser()
    sentiment_get_args.add_argument("sentence", type=str, help="The sentence field is required!", required=True)

    # response
    resource_fields = dict(
        percentage=fields.Float,
        prediction=fields.String,
        sentence=fields.String
    )

Most importantly we define our `Resource`. This is a Python class that defines the API methods that will be allowed to be accessed. In the case of this project only the `get` funtion is needed as the user will be requesting information only. 

    class SentimentResource(Resource):
        @marshal_with(resource_fields)
        def get(self):
            sentence = sentiment_get_args.parse_args()["sentence"] # get the sentence from arguments
            prediction = sample_predict(sentence=sentence, pad=True) # make a prediction based on the sentence
            sentiment_category = categoryze_sentiment(prediction) # put the prediction in a category (negative, neutral, positive)

            # create return dictionary
            ret_val = dict(
                percentage=prediction * 100,
                prediction=sentiment_category,
                sentence=sentence
            )

            return ret_val # return value

After defining the `Resource` it is necessary to register the resource to the api so that Flask has knowledge of the existance of the `Resource`. We also specicy the path of the resource, in this case the `Resource` will be accessible at:

* [BASE_URL]/senitment-analysis

    api.add_resource(SentimentResource, '/sentiment-analysis')

Finally, we need to check that the current file is the "main" file and run the file.

    if __name__ == "__main__":
        app.run()

## Conclusion

In summary I have succesfully setup a basic Python Flask REST API which hosts a Deep Learning Model. With the knowledge aqcuired in developing this API I am capable of applying that in bigger and more complex projects.