import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator
from scipy.sparse.linalg import svds

def svd_bias(A, rank = 3):
    # vector of item averages (excluding zeroes) as a vector and as a column vector
    item_avg = (A.sum(axis = 0) / A.getnnz(axis=0)).A1 
    item_avg_t = item_avg.reshape(-1,1)
    
    
    # vector of user averages
    user_avg = (A.sum(axis = 1).reshape(1,-1) / A.getnnz(axis = 1)).A1
    user_avg_t = user_avg.reshape(-1,1)
    
    
    # minus item averages
    subtracted = A.data - item_avg[A.indices]
    D = csr_matrix((subtracted, A.indices, A.indptr), A.shape)
    
    
    # setting up linear operators. note the correct shapes
    M,N = A.shape
    def matvec(v):
        if v.shape == (N, ):        
            return D.dot(v)  - user_avg*(v.sum()) + item_avg.dot(v)
        else:
            return D.dot(v)  - user_avg_t*(v.sum()) + item_avg.dot(v)

    def rmatvec(v):
        if v.shape == (M, ): 
            return D.T.dot(v) - user_avg.dot(v) + item_avg*(v.sum())
        else:
            return D.T.dot(v) - user_avg.dot(v) + item_avg_t*(v.sum())

    
    
    
    # getting the imputed linear operator
    A_imputed = LinearOperator(A.shape, matvec = matvec, rmatvec = rmatvec)
    
    # SVD of a sparse matrix
    U, S, Vt = svds(A_imputed, k = rank)
    
    
    return U, S, Vt