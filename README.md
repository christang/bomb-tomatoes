# A tags-based recommender using the MovieLens 1M dataset

This project explores the idea of whether we can express a user's ratings over a set of the movies
they rated as a linear combination of tag-movie relevance scores. That is to say, if we have a movie:

    "When Harry Met Sally" ~ tags {"comedy": 0.9, "drama": 0.1, "romantic": 0.9}
    
is it possible to solve for the vector of weights[u] for each user u such that:

    R[u](m) = weights[u] * tags[m]
    
R[u] is the user u's rating for movie m, and tags[m] is the tags vector for movie m. If so, weights[u]
would give us insight into the user's preferences by tag.

If successful, this would allow us to compute recommendations for a user independent of comparing that
user to other similar users in the database (a nice property). In addition, I wanted to understand the
number of ratings I would need to have in order to obtain reasonable results.

This project was not intended to compete with state-of-the-art methods, but as an opportunity to develop
some ideas I described above.

(*bomb-tomatoes* = *bombfell* + *rotten-tomatoes*)

### Methods

The per-person recommender takes an existing dataset of movie ratings by users, tags in MovieLens, 
and decade the movie was made, and extracts a feature matrix using principal component analysis (e.g.
the demographic set). The recommender then learns a user's individual profile by solving the least
squares problem to extract feature weights using the feature matrix and the user's own ratings.

To test the personalized recommender, I did the following:

1. For each group of users having 20-29 ratings, 30-49 ratings, 50-100 ratings and 100-999 ratings,
do the following:

    1. Split the users into a test set and a demographic training set (k-split, k=12)
    2. Use the demographic training set to extract principal components and select features,
    creating a feature matrix
    3. Split the test set further into a per-person training set and test set (k-fold, k=5)
    4. Apply the per-person training set to the feature matrix and make predictions on the
    training set
    5. Lastly, I scaled the number of features based on the number of existing ratings in their
    per-person set. Thus, the number of features could be different for each person such that
    the rank of the resulting matrix does not exceed the number of ratings. E.g. if Sue only
    rated 15 items, I fit her recommender to 3 components, but if Joaquin rated 80, I fit his to
    16. I capped the number of components to 20.

2. Compute root mean square error (RMSE) and rank correlation (Kendall's tau) between the predicted
scores and ground truth. Rank correlation tells us whether we get the order of the user's preferences
correct, and RMSE tells us how close we are to the real values in absolute points. For our purposes,
rank correlation is more important than RMSE, but useful if in the future we want to display the
predicted score to the user (as in Netflix).

3. Compute RMSE and rank correlation for two hypothetical recommenders: Perfect and Trivial. Perfect
simply returns the user's own recommendation back. Trivial returns the average rating for a movie, as
if we hadn't personalized the ratings at all. This gives us upper and lower bounds on what the metrics
should be, and just an overall sanity check for everything.

### Results

Some guidelines: 

(1) RMSE -- smaller is better, 0.0 is min and perfect;
(2) KendallTauMetric -- larger is better, 1.0 is max and means perfectly correlated, -1.0 is min and means anti-correlated; [number in scientific notation is p-value].

    SPLIT 1
    users.count w/ 20 to 29 ratings : 74
    PerfectRecommender
    Fold 5	RMSEMetric : rmse(f:5)=0.00	KendallTauMetric : tau(f:5)=1.00[8.17e-161]

    TrivialArithMeanRecommender
    Fold 5	RMSEMetric : rmse(f:5)=1.02	KendallTauMetric : tau(f:5)=0.31[6.91e-17]

    BomTomRecommender
    Fold 5	RMSEMetric : rmse(f:5)=1.09	KendallTauMetric : tau(f:5)=0.32[1.70e-17]

    users.count w/ 30 to 49 ratings : 151
    PerfectRecommender
    Fold 5	RMSEMetric : rmse(f:5)=0.00	KendallTauMetric : tau(f:5)=1.00[0.00e+00]

    TrivialArithMeanRecommender
    Fold 5	RMSEMetric : rmse(f:5)=1.06	KendallTauMetric : tau(f:5)=0.31[2.98e-43]

    BomTomRecommender
    Fold 5	RMSEMetric : rmse(f:5)=1.07	KendallTauMetric : tau(f:5)=0.37[1.90e-62]

    users.count w/ 50 to 99 ratings : 129
    PerfectRecommender
    Fold 5	RMSEMetric : rmse(f:5)=0.00	KendallTauMetric : tau(f:5)=1.00[0.00e+00]

    TrivialArithMeanRecommender
    Fold 5	RMSEMetric : rmse(f:5)=1.05	KendallTauMetric : tau(f:5)=0.37[7.33e-124]

    BomTomRecommender
    Fold 5	RMSEMetric : rmse(f:5)=1.00	KendallTauMetric : tau(f:5)=0.45[7.20e-177]

    users.count w/ 100 to 999 ratings : 219
    PerfectRecommender
    Fold 5	RMSEMetric : rmse(f:5)=0.00	KendallTauMetric : tau(f:5)=1.00[0.00e+00]

    TrivialArithMeanRecommender
    Fold 5	RMSEMetric : rmse(f:5)=1.02	KendallTauMetric : tau(f:5)=0.36[0.00e+00]

    BomTomRecommender
    Fold 5	RMSEMetric : rmse(f:5)=0.91	KendallTauMetric : tau(f:5)=0.52[0.00e+00]
    
