import numpy as np
import scipy.linalg
from copy import deepcopy
from threading import Lock


class UKFException(Exception):
    """Raise for errors in the UKF, usually due to bad inputs"""


class UKF:
    def __init__(self, num_states, process_noise, initial_state, initial_covar, alpha, k, beta, iterate_function):
        """
        Initializes the unscented kalman filter
        :param num_states: int, the size of the state
        :param process_noise: the process noise covariance per unit time, should be num_states x num_states
        :param initial_state: initial values for the states, should be num_states x 1
        :param initial_covar: initial covariance matrix, should be num_states x num_states
        :param alpha: UKF tuning parameter, determines spread of sigma points
        :param k: UKF tuning parameter
        :param beta: UKF tuning parameter
        :param iterate_function: function that predicts the next state
        """
        self.n_dim = int(num_states)
        self.n_sig = 1 + num_states * 2
        self.q = process_noise
        self.x = initial_state
        self.p = initial_covar
        self.beta = beta
        self.alpha = alpha
        self.k = k
        self.iterate = iterate_function

        # ------------------------------------------------------------------
        # TODO: Calculate self.lambd
        # Formula: alpha^2 * (n_dim + k) - n_dim
        # ------------------------------------------------------------------
        self.lambd = 0 # Replace with formula

        self.covar_weights = np.zeros(self.n_sig)
        self.mean_weights = np.zeros(self.n_sig)

        # ------------------------------------------------------------------
        # TODO: Initialize Weights
        # 1. Set self.covar_weights[0] and self.mean_weights[0]
        #    (Remember covar_weights[0] includes the beta term)
        # 2. Use a loop to set weights for the rest of the sigma points (1 to n_sig)
        # ------------------------------------------------------------------
        
        # ------------------------------------------------------------------
        # TODO: Generate Initial Sigmas
        # Call the __get_sigmas helper function and store in self.sigmas
        # ------------------------------------------------------------------
        self.sigmas = None # Replace with call

        self.lock = Lock()

    def __get_sigmas(self):
        """generates sigma points"""
        ret = np.zeros((self.n_sig, self.n_dim))

        # ------------------------------------------------------------------
        # TODO: Generate Sigma Points
        # 1. Calculate the square root matrix of: (n_dim + lambd) * self.p
        #    Hint: Use scipy.linalg.sqrtm
        # 2. Set the first point (ret[0]) to self.x
        # 3. Loop through n_dim to set the remaining points:
        #    - Positive direction: self.x + sqrt_matrix_column
        #    - Negative direction: self.x - sqrt_matrix_column
        # ------------------------------------------------------------------
        
        return ret.T

    def update(self, states, data, r_matrix):
        """
        performs a measurement update
        :param states: list of indices (zero-indexed) of which states were measured
        :param data: list of the data corresponding to the values in states
        :param r_matrix: error matrix for the data
        """

        self.lock.acquire()

        num_states = len(states)

        # ------------------------------------------------------------------
        # TODO: Create Measurement Sigmas (y) and Mean (y_mean)
        # 1. Split self.sigmas to isolate the states being measured.
        # 2. Create 'y' (sigmas of the measured states).
        # 3. Create 'y_mean' (mean of the measured states).
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TODO: Calculate Differences
        # 1. Calculate y_diff: difference between y and y_mean
        # 2. Calculate x_diff: difference between self.sigmas and self.x
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TODO: Calculate Measurement Covariance (p_yy)
        # 1. Initialize p_yy (num_states x num_states).
        # 2. Sum the weighted outer products of y_diff.
        # 3. CRITICAL: Add the measurement noise (r_matrix) to p_yy.
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TODO: Calculate Cross Covariance (p_xy)
        # 1. Initialize p_xy (n_dim x num_states).
        # 2. Sum the weighted products of x_diff and y_diff.
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TODO: Kalman Gain and Update
        # 1. Calculate K = p_xy * inv(p_yy)
        # 2. Update self.x using K and residual (data - y_mean)
        # 3. Update self.p using K and p_yy
        # 4. Recalculate self.sigmas using __get_sigmas()
        # ------------------------------------------------------------------

        self.lock.release()

    def predict(self, timestep, inputs=[]):
        """
        performs a prediction step
        :param timestep: float, amount of time since last prediction
        """

        self.lock.acquire()

        # ------------------------------------------------------------------
        # TODO: Propagate Sigma Points
        # 1. Pass each column of self.sigmas through self.iterate() function.
        #    (Pass timestep and inputs to iterate).
        # 2. Store result in sigmas_out.
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TODO: Calculate Predicted Mean (x_out)
        # Calculate the weighted sum of sigmas_out using self.mean_weights.
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TODO: Calculate Predicted Covariance (p_out)
        # 1. Loop through sigma points.
        # 2. Calculate diff = sigma_point - x_out.
        # 3. p_out += weight * (diff dot diff.T).
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TODO: Add Process Noise
        # Add (timestep * self.q) to p_out.
        # ------------------------------------------------------------------

        # ------------------------------------------------------------------
        # TODO: Update State
        # Set self.sigmas, self.x, and self.p to the new values.
        # ------------------------------------------------------------------

        self.lock.release()

    def get_state(self, index=-1):
        """
        returns the current state (n_dim x 1), or a particular state variable (float)
        :param index: optional, if provided, the index of the returned variable
        :return:
        """
        if index >= 0:
            return self.x[index]
        else:
            return self.x

    def get_covar(self):
        """
        :return: current state covariance (n_dim x n_dim)
        """
        return self.p

    def set_state(self, value, index=-1):
        """
        Overrides the filter by setting one variable of the state or the whole state
        :param value: the value to put into the state (1 x 1 or n_dim x 1)
        :param index: the index at which to override the state (-1 for whole state)
        """
        with self.lock:
            if index != -1:
                self.x[index] = value
            else:
                self.x = value

    def reset(self, state, covar):
        """
        Restarts the UKF at the given state and covariance
        :param state: n_dim x 1
        :param covar: n_dim x n_dim
        """

        with self.lock:
            self.x = state
            self.p = covar