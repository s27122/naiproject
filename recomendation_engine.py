from pymongo import MongoClient
import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import defaultdict

client = MongoClient('*********')
db = client['*******']

def get_data():
    interactions = list(db.user_product_interactions.find())
    df_interactions = pd.DataFrame(interactions)
    products = list(db.products.find())
    df_products = pd.DataFrame(products)
    return df_interactions, df_products

# Collaborative Filtering
def collaborative_filtering(df_interactions):
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df_interactions[['userId', 'productId', 'rating']], reader)
    trainset = data.build_full_trainset()
    model = KNNBasic()
    model.fit(trainset)
    return model

# Content-Based Filtering
def content_based_filtering(df_products, product_id):
    df_products['combined_features'] = df_products['name'] + " " + df_products['category']
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_products['combined_features'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    # Check if product_id exists in the dataframe
    idx_list = df_products.index[df_products['_id'] == product_id].tolist()
    if not idx_list:
        print(f"Warning: Product ID {product_id} not found in products dataframe.")
        return []
    
    idx = idx_list[0]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Top 5 похожих продуктов
    return [df_products.iloc[i[0]]['_id'] for i in sim_scores]

# Popularity-Based Filtering
def popularity_based_filtering(df_interactions):
    product_popularity = df_interactions.groupby('productId').size().reset_index(name='interaction_count')
    top_products = product_popularity.sort_values(by='interaction_count', ascending=False).head(5)
    return list(top_products['productId'])

def precision_recall_f1(predictions, k=5, threshold=3.5):
    user_est_true = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))
    
    precisions, recalls = [], []
    for uid, user_ratings in user_est_true.items():
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        top_k = user_ratings[:k]
        
        relevant = sum((true_r >= threshold) for _, true_r in top_k)
        retrieved = len(top_k)
        relevant_total = sum((true_r >= threshold) for _, true_r in user_ratings)
        
        precision = relevant / retrieved if retrieved else 0
        recall = relevant / relevant_total if relevant_total else 0
        
        precisions.append(precision)
        recalls.append(recall)
    
    avg_precision = sum(precisions) / len(precisions) if precisions else 0
    avg_recall = sum(recalls) / len(recalls) if recalls else 0
    f1 = (2 * avg_precision * avg_recall) / (avg_precision + avg_recall) if avg_precision + avg_recall else 0
    return avg_precision, avg_recall, f1