# Project Prerequisites & Concept Check

Welcome to the implementation phase! Before you dive into the Python code, you must ensure you have a solid grasp of the theory covered in Week 1 and the specific coding tools we will be using.

---

## Part 1: Week 1 Concept Check (Theory)
*Based on `kalman_intro.pdf` and `unscented.pdf`*

You should have read the provided PDFs. Before proceeding, verify you can answer **"Yes"** to the following questions. If not, please revisit the readings.

### From `kalman_intro.pdf` (The Basics)
- [ ] **The Cycle:** Do you understand the two-step cycle of **Prediction** (Time Update) and **Correction** (Measurement Update)?
- [ ] **The Matrices:** Do you know what $x$ (State), $P$ (Covariance), $Q$ (Process Noise), and $R$ (Measurement Noise) represent physically?
- [ ] **The Goal:** Do you understand that the filter is trying to fuse a *noisy prediction* with a *noisy measurement* to find the optimal estimate?

### From `unscented.pdf` (The UKF Innovation)
- [ ] **The "Why":** Do you understand why we can't use a standard Kalman Filter for nonlinear problems? (i.e., Linear functions of Gaussians are Gaussian, but nonlinear functions are not).
- [ ] **EKF vs. UKF:** Do you understand that the Extended Kalman Filter (EKF) linearizes the function (using Jacobians/Taylor Series), whereas the UKF approximates the *probability distribution* instead?
- [ ] **Sigma Points:** Do you understand that we choose specific deterministic points, push them through the nonlinear function, and then recalculate the mean and covariance from the result?
- [ ] **The Unscented Transform:** Do you understand that the "Weights" ($W_m$, $W_c$) are used to reconstruct the Gaussian distribution after the points are transformed?

---

## Part 2: Python & Library Prerequisites
*Focus: The specific tools used in our `ukf.py` template.*

You do not need to be a Python expert, but you must be comfortable with the following specific concepts.

### 1. Python Class Structure
The UKF is implemented as a class to maintain state (`self.x`, `self.p`) over time.
* **`__init__`**: Review how to initialize object attributes.
* **Functions as Arguments**: The UKF takes a physics function (`iterate_function`) as an input. You need to know how to call a function stored in a variable.
    ```python
    # Example of what happens inside the class
    self.iterate = iterate_function
    next_state = self.iterate(current_state, dt)
    ```

### 2. NumPy (Linear Algebra)
*Critical: 90% of UKF errors are due to Matrix Dimension mismatches.*

You must strictly distinguish between **Arrays**, **Vectors**, and **Matrices**.

* **Matrix Multiplication (`@` or `np.dot`)**:
    * **Do not use `*`**: This is element-wise multiplication (like `[1, 2] * [1, 2] = [1, 4]`).
    * **Use `@`**: This is matrix multiplication (row times column).
* **Transposing (`.T`)**: Flipping rows and columns.
* **Outer Product**: used for Covariance calculation.
    * Formula: $\text{diff} \cdot \text{diff}^T$
    * Code: `np.dot(diff, diff.T)`
* **Handling 1D Arrays**:
    * NumPy often defaults to "flat" arrays `(3,)` which behave unexpectedly in linear algebra.
    * **Key Function:** `np.atleast_2d(array)` helps ensure your vectors are shaped `(N, 1)` or `(1, N)` so matrix math works correctly.

### 3. SciPy (The "Unscented" Math)
To generate Sigma points, we need the "square root" of the Covariance matrix ($P$).
* **`scipy.linalg.sqrtm`**: Calculates the matrix square root.
    * *Warning:* Due to tiny floating-point errors, this may return Complex numbers (e.g., `1.0 + 0j`).
    * *Fix:* Always access the real component: `scipy.linalg.sqrtm(P).real`.

### 4. Threading & Locking
*Focus: Data Safety*

In robotics, sensor data arrives asynchronously. We use locks to prevent the **Predict** step and **Update** step from modifying `self.x` at the exact same moment.

* **The Concept:** Only one thread can hold the "key" (lock) to the data at a time.
* **`try...finally` Block**: We use this pattern to ensure the lock is *always* released, even if your code crashes with an error.
    ```python
    self.lock.acquire()
    try:
        # Complex math that might fail
        pass
    finally:
        self.lock.release() # This runs no matter what
    ```

---

## Part 3: Ready to Start?

If you have checked off the boxes in Part 1 and reviewed the syntax in Part 2, you are ready start the implementation.

**Tip:** Keep `unscented.pdf` open on one screen and your code on the other. You will be directly translating the equations from the PDF into NumPy code.