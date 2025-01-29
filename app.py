from flask import Flask, request, render_template
from recomendation_engine import get_data, collaborative_filtering, content_based_filtering, popularity_based_filtering

app = Flask(__name__)

def get_user_recommendations(user_id, df_interactions, df_products, cf_model, popular_products):
    # Collaborative Filtering Recommendations
    try:
        user_inner_id = cf_model.trainset.to_inner_uid(user_id)
        cf_recommendations = cf_model.get_neighbors(user_inner_id, k=5)
        cf_recommended_items = [cf_model.trainset.to_raw_iid(inner_id) for inner_id in cf_recommendations]
    except ValueError:
        cf_recommended_items = []

    # Content-Based Filtering Recommendations
    user_interactions = df_interactions[df_interactions['userId'] == user_id]
    cb_recommended_items = set()
    for _, row in user_interactions.iterrows():
        product_id = row['productId']
        recommendations = content_based_filtering(df_products, product_id)
        cb_recommended_items.update(recommendations)
    cb_recommended_items = list(cb_recommended_items)[:5]  # Top 5 recommendations
    
    # Popularity-Based Filtering Recommendations
    pb_recommended_items = [product for product in popular_products if product not in user_interactions['productId'].tolist()][:5]
    
    return {
        "collaborative": cf_recommended_items,
        "content_based": cb_recommended_items,
        "popularity_based": pb_recommended_items
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id']) 
        except ValueError:
            error_message = "id must be a number"
            return render_template('index.html', error_message=error_message)

        df_interactions, df_products = get_data()
        cf_model = collaborative_filtering(df_interactions)
        popular_products = popularity_based_filtering(df_interactions)
        
        if user_id in df_interactions['userId'].unique():
            recommendations = get_user_recommendations(user_id, df_interactions, df_products, cf_model, popular_products)
            return render_template('index.html', user_id=user_id, recommendations=recommendations)
        else:
            error_message = "User not found"
            return render_template('index.html', error_message=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)