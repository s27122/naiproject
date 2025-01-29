from recomendation_engine import get_data, collaborative_filtering, content_based_filtering, popularity_based_filtering, precision_recall_f1
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split

if __name__ == "__main__":
    df_interactions, df_products = get_data()
    
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df_interactions[['userId', 'productId', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.2)
    
    # Collaborative Filtering
    cf_model = collaborative_filtering(df_interactions)
    cf_predictions = cf_model.test(testset)
    cf_precision, cf_recall, cf_f1 = precision_recall_f1(cf_predictions)
    
    # Content-Based Filtering
    cb_predictions = []
    for _, row in df_interactions.iterrows():
        userId = row['userId']
        productId = row['productId']
        true_rating = row['rating']
        
        print(f"Processing User: {userId}, Product: {productId}")
        
        cb_recommendations = content_based_filtering(df_products, productId)
        est = 1 if productId in cb_recommendations else 0
        cb_predictions.append((userId, productId, true_rating, est, None))
    
    cb_precision, cb_recall, cb_f1 = precision_recall_f1(cb_predictions)
    
    # Popularity-Based Filtering
    pb_predictions = []
    popular_products = popularity_based_filtering(df_interactions)
    for _, row in df_interactions.iterrows():
        userId = row['userId']
        productId = row['productId']
        true_rating = row['rating']
        est = 1 if productId in popular_products else 0
        pb_predictions.append((userId, productId, true_rating, est, None))
    
    pb_precision, pb_recall, pb_f1 = precision_recall_f1(pb_predictions)
    
    print("Collaborative Filtering: Precision: {:.2f}, Recall: {:.2f}, F1: {:.2f}".format(cf_precision, cf_recall, cf_f1))
    print("Content-Based Filtering: Precision: {:.2f}, Recall: {:.2f}, F1: {:.2f}".format(cb_precision, cb_recall, cb_f1))
    print("Popularity-Based Filtering: Precision: {:.2f}, Recall: {:.2f}, F1: {:.2f}".format(pb_precision, pb_recall, pb_f1))