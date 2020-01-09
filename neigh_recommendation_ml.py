from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

df_pca = pd.read_csv('raleigh_neighborhoods_pca.csv', index_col = 'Neighborhood')

def get_recommendations(df_pca, neighborhood_name, num_recommendations = 10):
    neighborhood = df_pca[df_pca.index == neighborhood_name]
    if len(neighborhood) != 1:
        return []
    distances = cdist(neighborhood,df_pca)[0]
    return sorted(list(zip(df_pca.index,distances)), key = lambda x:x[1])[1:(num_recommendations+1)]

app = Flask(__name__)

@app.route('/list_all',methods=['POST'])
def get_list():
	return jsonify(df_pca.index.to_list())

@app.route('/recommend',methods=['POST'])
def recommend():
	params = request.get_json(force = True)
	neighborhood_name, num_recommendations = params['neighborhood_name'], params['num_recommendations']
	recommendations = get_recommendations(df_pca, neighborhood_name, num_recommendations)
	return jsonify(recommendations)

if __name__ =='__main__':
	app.run(debug=True)
