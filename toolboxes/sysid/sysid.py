import numpy as np
class Era():
    def __init__(self):
        pass

    def Hankel_free(self, Y, r, s):
        q, k, p = np.shape(Y)
        H = np.zeros((r * p, q * s))
        H_star = np.zeros_like(H)

        for rows in range(0, r):
            for cols in range(0, s):
                for _q in range(0, q):
                    H[rows * p:(rows + 1) * p, cols * q + _q] = Y[_q][rows + cols, :]
                    H_star[rows * p:(rows + 1) * p, cols * q + _q] = Y[_q][rows + cols + 1, :]
        return H, H_star

    def Free_response_experiment(self, t, y, r, s, epsilon=1e-4):
        # y deve ter shape o formato a = [q][k,p]
        # indice q representa a experimentacao q;
        # indice k representa o instante discreto da amostra;
        # indica p representa o numero de sensores;

        p, q = np.shape(y)[2], np.shape(y)[0]
        H, H_star = self.Hankel_free(y, r, s)

        input_number = q
        output_number = p

        P, D_vector, Qh = np.linalg.svd(H, full_matrices=False)
        D = np.diag(D_vector)
        Q = Qh.conj().T

        P_d = P @ D
        n_orders = [D_vector >= epsilon][0]

        P_tilde = P[:, n_orders]
        D_tilde = np.diag(D[n_orders])
        Q_tilde = Q[:, n_orders]
        P_d_tilde = P_d[:, n_orders]

        D_tilde_half_neg = np.diag(D_vector[n_orders] ** -0.5)
        D_tilde_half_pos = np.diag(D_vector[n_orders] ** 0.5)

        A_id = (D_tilde_half_neg @ P_tilde.T) @ H_star @ (Q_tilde @ D_tilde_half_neg)

        E_m = (np.eye(input_number, M=np.shape(Q_tilde)[0])).T
        E_p = np.eye(output_number, M=np.shape(P_tilde)[0]).T

        B_id = D_tilde_half_pos @ Q_tilde.T @ E_m
        C_id = E_p.T @ P_tilde @ D_tilde_half_pos

        Matrice_acumulada = np.eye(N=np.shape(A_id)[0], M=np.shape(A_id)[1])

        Reconstructed_states = np.zeros((q, len(t), p))

        lambdas, psi = np.linalg.eig(A_id)
        A_d = np.diag(lambdas)
        B_d = np.linalg.inv(psi) @ B_id
        C_d = C_id @ psi

        k = np.arange(0, len(t))
        for _k in k:

            for _q in range(0, q):
                (Reconstructed_states[_q][_k, :]) = ((C_id @ Matrice_acumulada @ B_id)[:, _q])

            Matrice_acumulada = Matrice_acumulada @ A_id

        return {'A_id': A_id,
                'B_id': B_id,
                'C_id': C_id,
                'Reconstructed_states': Reconstructed_states,
                'A_d': A_d,
                'B_d': B_d,
                'C_d': C_d,
                'phi': psi,
                'lambda_i': lambdas,
                'P': P,
                'D': D,
                'Qh': Qh,
                }

    def modal_parameters(self, lambda_i, dt):
        f_i = 1/(2*np.pi*dt)*((np.log(lambda_i*lambda_i.conj())/2)**2 +
                              (np.arccos((lambda_i + lambda_i.conj())/(2*(lambda_i*lambda_i.conj())**0.5)))**2)**0.5

        return f_i

class O3KID():
    # TODO ainda nao apresenta resultados bons
    """
    VERSÃO = 1

    STATUS = Em desenvolvimento

    Referência: https://www.semanticscholar.org/paper/Extension-of-OKID-to-Output-Only-System-Vicario-Phan/85c03fea65a340f335d4763cd379756fe9d51722

    """
    def __init__(self):
        pass
    def setData(self, data):
        """
        Importante que esteja no formato [q, N]
        onde q: é o número de sensores e
        N: tamanho da medição
        """
        self.data = data
        self.data_shape = data.shape

        self.q = self.data_shape[0]
        self.N = self.data_shape[1]
        self.N_markov = 200
        self.p = 200
        H, H_star = self.assemblyHankel(r=self.N_markov//2, s=self.N_markov//2)

        self.stateSpaceId(H, H_star)

    def stateSpaceId(self, H, H_star, epsilon=1e-10):
        # Extrair A, C & K

        P, D_vector, Qh = np.linalg.svd(H, full_matrices=False)
        D = np.diag(D_vector)
        Q = Qh.conj().T

        P_d = P @ D
        n_orders = [D_vector >= epsilon][0]
        print(D_vector)
        print(n_orders)

        P_tilde = P[:, n_orders]
        D_tilde = np.diag(D[n_orders])
        Q_tilde = Q[:, n_orders]
        P_d_tilde = P_d[:, n_orders]

        D_tilde_half_neg = np.diag(D_vector[n_orders] ** -0.5)
        D_tilde_half_pos = np.diag(D_vector[n_orders] ** 0.5)
        A_id = (D_tilde_half_neg @ P_tilde.T) @ H_star @ (Q_tilde @ D_tilde_half_neg)

        E_m = (np.eye(self.q, M=np.shape(Q_tilde)[0])).T
        E_p = np.eye(self.q, M=np.shape(P_tilde)[0]).T

        B_id = D_tilde_half_pos @ Q_tilde.T @ E_m
        C_id = E_p.T @ P_tilde @ D_tilde_half_pos



    def assemblyHankel(self, r=5, s=5):
        ls_results = self.leastSquare()['KalmanFilter']
        markov_parameters = self.computeMarkov(ls_results)['Markov']
        H = np.zeros((self.q*r, self.q*s))
        H_star = np.zeros((self.q * r, self.q * s))
        for rows in range(0, r):
            for cols in range(0, s):
                H[self.q*rows: self.q*(rows+1), self.q*cols: self.q*(cols+1)] = markov_parameters[:, self.q*(rows+cols):self.q*(rows+cols+1)]

                H_star[self.q * rows: self.q * (rows + 1), self.q * cols: self.q * (cols + 1)] = markov_parameters[:,
                                                                                            1+self.q * (
                                                                                                        rows + cols):1+self.q * (
                                                                                                        rows + cols + 1)]
        return H, H_star

    def calc_V(self, index):
        return self.data[:, index : index-self.p:-1].reshape(self.p*self.q)

    def leastSquare(self):
        """
        Resolver o problema Y = PHI@V + E
        """
        k = range(self.p, self.N, 1)
        #Montar as matrizes Y e V
        # Matriz Y
        y = self.data[:, self.p:self.N]
        # Matriz V
        v = np.zeros((self.q*self.p, self.N - self.p))
        for cont, index in enumerate(range(self.p, self.N)):
            v[:, cont] = self.calc_V(index)

        phi_tilde = y@np.linalg.pinv(v)
        y_observed = phi_tilde@v
        residuo = y - y_observed

        return {'E': residuo, 'KalmanFilter': phi_tilde}

    def phi_tilde_j(self, phi_tilde, index):
        #Tamanho de phi_tilde = qxq*p
        if index + 1 > self.p:
            return np.zeros((self.q, self.q))
        else:
            return phi_tilde[:, self.q*index:self.q*index+self.q]

    def calculatePsi(self, psi, index, phi_tilde, funcount = 0):
        # Funcao resursiva para calculo do Psi
        if funcount == index:
            psi[:, index*self.q:(index+1)*self.q] += self.phi_tilde_j(phi_tilde, index)

            return psi
        else:
            psi[:, index*self.q:(index+1)*self.q] += self.phi_tilde_j(phi_tilde, funcount)@psi[:, (index - funcount -1)*self.q:(index - funcount)*self.q]
            funcount += 1
            return self.calculatePsi(psi, index, phi_tilde, funcount)

    def computeMarkov(self, phi_tilde):
        # j > p
        # Vetor para facilitar a montagem das matrizes
        psi = np.zeros((self.q, self.q*self.N_markov))

        for _j in range(0, self.N_markov):
            psi = self.calculatePsi(psi, _j, phi_tilde)

        return {'Markov': psi}

if __name__ =='__main__':
    def run_example1():


        M = np.array([[1, 0], [0, 0.5] ])
        K = np.array([[22.3, -11.5], [-11.5, 22.3-11.5]])
        C = np.array([[0.5, -.02],[-0.2, 0.48]])

        A = np.zeros((4, 4))
        A[0:K.shape[0], K.shape[0]:] = np.identity(K.shape[0])
        A[K.shape[0]:, 0:K.shape[0]] = -np.linalg.inv(M) @ K
        A[K.shape[0]:, K.shape[0]:] = -np.linalg.inv(M) @ C

        natural_frequencys = np.linalg.eigvals(A)
        lambdas = [[(lambdas.real ** 2 + lambdas.imag ** 2) ** 0.5,
                    -lambdas.real / ((lambdas.real ** 2 + lambdas.imag ** 2) ** 0.5)] for lambdas in natural_frequencys[::2]]
        omega_ni = [value[0] for value in lambdas]
        zeta_i = [value[1] for value in lambdas]

        f_ni = [omega_ni / (2 * np.pi) for omega_ni in omega_ni]
        print(f'Frequencias naturais {f_ni} teórica Hz')
        function = lambda x, t: A@x
        t = np.linspace(0, 10, 100)
        y = scipy.integrate.odeint(function, np.array([0, 0., 0.16, 0.0]), t)

        Simulation = Era()
        Sim = Simulation.Free_response_experiment(t, y[None, :, :], 20, 20)
        Reconstructed_states = (Sim['Reconstructed_states'])
        lambda_i = (Sim['lambda_i'])

        fig, ax = plt.subplots()
        ax.plot(t, y)
        ax.plot(t, Reconstructed_states[0], marker='o', markersize=2, linestyle=' ')
        plt.show()

        print(f'Frequencia natural 1 Identificado = {Simulation.modal_parameters(lambda_i[0], t[1] - t[0])} Hz')
        print(f'Frequencia natural 2 Identificado  = {Simulation.modal_parameters(lambda_i[2], t[1] - t[0])} Hz')

    def run_example2():
        Simulation = O3KID()
        datafile = '../data/livre2.txt'
        with open(datafile) as file:
            data = np.loadtxt(file)
        fig, ax = plt.subplots()

        data_id = data.T[2, :]
        data_smooth = movavg(data_id)

        ax.plot(data_smooth)
        plt.show()
        Simulation.setData(data_smooth[None, :])


    def movavg(x, N=10):
        padded_x = np.insert(
            np.insert(np.insert(x, len(x), np.empty(int(N / 2)) * np.nan), 0, np.empty(int(N / 2)) * np.nan), 0, 0)
        n_nan = np.cumsum(np.isnan(padded_x))
        cumsum = np.nancumsum(padded_x)
        window_sum = cumsum[N + 1:] - cumsum[
                                      :-(N + 1)] - x  # subtract value of interest from sum of all values within window
        window_n_nan = n_nan[N + 1:] - n_nan[:-(N + 1)] - np.isnan(x)
        window_n_values = (N - window_n_nan)
        movavg = (window_sum) / (window_n_values)
        return movavg


    import numpy as np
    import scipy.integrate
    import matplotlib.pyplot as plt
    run_example2()