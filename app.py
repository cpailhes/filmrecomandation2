# import main Flask class and request object
from flask import Flask, request
import pandas as pd
import numpy as np
import math

# create the Flask app
app = Flask(__name__)


gaussian_filter = lambda x,y,sigma: math.exp(-(x-y)**2/(2*sigma**2))


@app.route('/recommandation' , methods=['GET', 'POST'])

def recommandation():
#reading the original dataset
        
        df_result = pd.read_csv('df_result.csv')

        #reading movie title given by user in the front-end
        Movie =request.args.get('movie')
        sample =request.args.get('sample')
        if not sample :
            sample="yes"
        
                
        def recommend(m ,sample):
            cluster_KMeans=df_result[df_result.movie_title==m].cluster_KMeans.values
                
            if cluster_KMeans.size != 0 :
                dfresult =df_result[df_result['cluster_KMeans']==cluster_KMeans[0]]    
                dfresult =dfresult[df_result['movie_title']!=m]
                if sample == 'yes':
                    dfresult = dfresult.sample(5)
                    dfresult = dfresult.reset_index()
                    return (dfresult[['movie_title']]).to_html()
                else:
                    dfresult['note'] = 0
                    for index, row in dfresult.iterrows():
                        row['note'] = gaussian_filter( row['tsne-2d-one'], row['tsne-2d-two'],10) 
                    dfresult.sort_values('note', ascending=False)
                    dfresult = dfresult.head(5)
                    return (dfresult[['movie_title']]).to_html()
            else :
                print('no movie')
                return 'no movie found for :{}'.format(Movie)
    

   #printing top-10 recommendations
        try:
            output = recommend(Movie ,sample)
            
            return output
        except ValueError as e:
            return e

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)