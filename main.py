from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with

from model import sample_predict
from service import categoryze_sentiment

app = Flask(__name__)
api = Api(app)

sentiment_get_args = reqparse.RequestParser()
sentiment_get_args.add_argument("sentence", type=str, help="The sentence field is required!", required=True)

resource_fields = dict(
    percentage=fields.Float,
    prediction=fields.String,
    sentence=fields.String
)

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


api.add_resource(SentimentResource, '/sentiment-analysis')

if __name__ == "__main__":
    app.run(debug=True)
