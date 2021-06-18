def categoryze_sentiment(prediction):
    if prediction < 0.4:
        return 'negative'
    if prediction < 0.6:
        return 'neutral'
    return 'positive'