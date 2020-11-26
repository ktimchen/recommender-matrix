# recommender-matrix

1) sparse_matrix_from_dataframe.ipynb creates a scipy sparse matrix from a dataframe of ratings of the form (game ID, user, rating given).

2) svd_with_bias.py: The missing elements of the sparse user-item matrix are first filled-in with the values of item average ratings and then the resulting matrix is additionally normalized by subtracting user average ratings. We compute the truncated SVD of this matrix. There is no need to actually compute the SVD of this dense matrix, LinearOperator from scipy.sparse does the job on the level of sparse matrices (incredibly fast!). 


The dot product between two column vectors of the normalized rating matrix R computes the distance (divide by norms for the adjusted cosine) between two items. 
Given the SVD decomposition R=USV^T, R^T times R = V S^2 V^T. So one can consider rows of the VS matrix as coordinates for items, and take dot products in this space. 

3) Now, sparse_matrix_from_dataframe.ipynb computes the cosine distance between the pairs of items. After that, kneighbors_graph(n_neighbors=100) give us a 100 closest neighboors for each item. 

Literature: 
- LinearOperator trick is inspired by this: www.skoltech.ru/app/data/uploads/2018/09/Frolov_Dissertation_Final1.pdf
- Old paper, but gets R^T times R correctly, http://lsa.colorado.edu/papers/JASIS.lsi.90.pdf
- Explains normalizations to counter bias, notes that it is enough to compute cosine similarity, gets  R^T times R wrong https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.104.241&rep=rep1&type=pdf 

