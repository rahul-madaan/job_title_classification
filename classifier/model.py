from joblib import load, dump
def prediction(job_title):
    with open('readme.txt', 'w') as f:
        f.write('Create a new text file!')

    model = load('classifier/model.joblib')
    pred_industry = model.predict([job_title])
    return pred_industry[0]

