# Prerequisites and Learning Resources

## Python Basics (for those new to the language)

* **Tutorial**: [FreeCodeCamp Tutorial video](https://www.youtube.com/watch?v=rfscVS0vtbw)
* **Reference**: [The Official Python Tutorial](https://docs.python.org/3/tutorial/)
* **Focus on**: Get comfortable with basic syntax. Focus especially on the later parts such as Object Oriented Programming in Python (Classes, `self`, `__init__`).

---

## NumPy - The Core of Scientific Computing

* **Tutorial**: [FreeCodeCamp Tutorial Video](https://www.youtube.com/watch?v=QUT1VHiLmmI)
* **Resource**: [NumPy: The absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
* **Focus on**: 
  * What is a NumPy array? 
  * How do you create arrays? 
  * What is array indexing, slicing, and, most importantly, **vectorization**? 
  * **Critical for UKF**: Understand the difference between `*` (element-wise multiplication) and `@` / `np.dot` (matrix multiplication).

---

## SciPy - Advanced Linear Algebra

* **Documentation**: [SciPy Linear Algebra (linalg) Reference](https://docs.scipy.org/doc/scipy/reference/linalg.html)
* **Specific Function**: [scipy.linalg.sqrtm Documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.sqrtm.html)
* **Focus on**:
  * **Matrix Square Roots**: The UKF relies on calculating the square root of the covariance matrix ($P$).
  * **`sqrtm` vs `sqrt`**: Standard `np.sqrt` calculates the square root of *each number* in the array. We need `scipy.linalg.sqrtm` which calculates the *Matrix* square root.
  * **Complex Returns**: Be aware that `sqrtm` can sometimes return complex numbers (e.g., `1.0 + 0j`) due to floating-point precision errors. You will need to access the `.real` part.

---

## Python Threading & Locking

* **Documentation**: [Python Threading: Locks](https://docs.python.org/3/library/threading.html#lock-objects)
* **Tutorial**: [Real Python: Threading and Locking](https://realpython.com/intro-to-python-threading/#working-with-many-threads)
* **Focus on**:
  * **Data Integrity**: In robotics, sensor data often arrives "asynchronously" (in the background). We must prevent the `predict` and `update` steps from modifying the state at the exact same time.
  * **The `Lock` Object**: How to initialize `self.lock = Lock()`.
  * **Context Managers**: Using the `with self.lock:` syntax to automatically acquire and release locks safely.

---

## Probability and Statistics

Those who want can also explore the below slides for better understanding of the probability and the random variable part.

### Visual Learning
* **Visuals**: [Seeing Theory: Brown University](https://seeing-theory.brown.edu/)
  * An interactive visual introduction to probability and statistics

### Lecture Materials
* **Lecture Slides**: Check out the following slides from Prof. Rajwade for CS215:
  * [Random Variables](https://www.cse.iitb.ac.in/~ajitvr/CS215_Spring2020/Slides/RV.pdf)
  

---

## Notes

* These resources are designed to give you the minimal necessary background for implementing and understanding the Unscented Kalman Filter.
* Don't feel like you need to master everything before starting - you can learn these concepts in parallel with the main project.
* The most important concepts are: basic Python OOP, NumPy array operations (`@` vs `*`), using `sqrtm` from SciPy, and understanding probability distributions.