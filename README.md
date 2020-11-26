# recommender-matrix

sparse_matrix_from_dataframe.ipynb creates a scipy sparse matrix from a dataframe of ratings of the form (game ID, user, rating given).

svd_with_bias.py: The missing elements of the sparse user-item matrix are first filled-in with the values of item average ratings and then the resulting matrix is additionally normalized by subtracting user average ratings. We compute the truncated SVD of this matrix. There is no need to actually compute the SVD of this dense matrix, LinearOperator from scipy.sparse does the job on the level of sparse matrices (incredibly fast!). 


The dot product between two column vectors of the normalized rating matrix R computes the distance (divide by norms for the adjusted cosine) between two items. 
Given the SVD decomposition R=USV^T, R^T times R = V S^2 V^T. So one can consider rows of the VS matrix as coordinates for items, and take dot products in this space. 

Now, sparse_matrix_from_dataframe.ipynb computes the cosine distance between the pairs of items. kneighbors_graph(n_neighbors=100) give us a 100 closest neighboors for each item. 

