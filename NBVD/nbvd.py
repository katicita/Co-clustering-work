import numpy as np
from matplotlib import pyplot as plt

class NBVD(object):
    def nbvd(self, X, U, S, V):
        U = U * (X.dot(V).dot(S.T)) / U.dot(S).dot(V.T).dot(V).dot(S.T)
        V = V * (X.T.dot(U).dot(S)) / V.dot(S.T).dot(U.T).dot(U).dot(S)
        S = S * (U.T.dot(X).dot(V)) / U.T.dot(U).dot(S).dot(V.T).dot(V)
        return U, S, V

    def matrix_factorization_clustering1(self, X, k, l, factorization_func=nbvd, norm=False, num_iters=1000):
        m, n = X.shape
        U = np.random.rand(m,k)
        S = np.random.rand(k,l)
        V = np.random.rand(n,l)
        
        if norm:
            X = Normalizer().fit_transform(X)

        for i in xrange(num_iters):
            U, S, V = self.nbvd(X, U, S, V)
            error = np.sum((X - U.dot(S).dot(V.T)) ** 2)

        rows_ind = np.argmax(U, axis=1)
        cols_ind = np.argmax(V, axis=1)    
        return U, S, V, rows_ind, cols_ind, error
    
    def matrix_factorization_clustering(self, X, k, l, factorization_func=nbvd, norm=False, num_iters=100):
        m, n = X.shape
        U = np.random.rand(m,k)
        S = np.random.rand(k,l)
        V = np.random.rand(n,l)

        if norm:
            X = Normalizer().fit_transform(X)

        error_best = np.inf

        for i in xrange(num_iters):
            U, S, V = self.nbvd(X, U, S, V)
            error = np.sqrt(np.sum((X - U.dot(S).dot(V.T)) ** 2))
            

            if error < error_best:
                U_best = U
                S_best = S
                V_best = V
                error_best = error

        Du = np.diag(np.ones(m).dot(U_best))
        Dv = np.diag(np.ones(n).dot(V_best))

        U_norm = U_best.dot( np.diag(S_best.dot(Dv).dot(np.ones(l))) )
        V_norm = V_best.dot( np.diag(np.ones(k).dot(Du).dot(S_best)) )

        rows_ind = np.argmax(U_norm, axis=1)
        cols_ind = np.argmax(U_norm, axis=1)

        #return U_norm, S_best, V_norm, rows_ind, cols_ind, error_best
        return U_best, S_best, V_best, rows_ind, cols_ind, error_best, U_norm, V_norm