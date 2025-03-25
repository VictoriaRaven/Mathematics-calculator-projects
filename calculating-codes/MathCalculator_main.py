import tkinter as tk
from tkinter import messagebox

# import these math stuff
import sympy as sp
import numpy as np
import scipy.stats as stats
from math import factorial, sqrt
import statistics
import ctypes
# Enable DPI awareness (for high-DPI displays)
# prevents a Blurry GUI
if ctypes.windll.shcore.SetProcessDpiAwareness:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

#idea in 2024
#updated in 2024 after leaving 1 semester
# included comments and other GUI features during 2025

class MathCalc:
    def __init__(self):
        self.variables = {}

    # Symbolic Algebra Functions
    def define_variable(self, name, value=None):
        if value is not None:
            self.variables[name] = sp.symbols(name)
            return self.variables[name], value
        else:
            self.variables[name] = sp.symbols(name)
            return self.variables[name]

    def simplify_expression(self, expr):
        return sp.simplify(expr)

    def expand_expression(self, expr):
        return sp.expand(expr)

    def factor_expression(self, expr):
        return sp.factor(expr)

    # Combinatorics Functions
    def permutations(self, n, r):
        return factorial(n) // factorial(n - r)

    def combinations(self, n, r):
        return factorial(n) // (factorial(r) * factorial(n - r))

    # Probability Functions
    def binomial_probability(self, n, k, p):
        bcoeff = self.combinations(n, k)
        return bcoeff * (p ** k) * ((1 - p) ** (n - k))

    def poisson_probability(self, k, lam):
        return (lam ** k * np.exp(-lam)) / factorial(k)

    def normal_probability(self, x, mu, sigma):
        return stats.norm.pdf(x, mu, sigma)

    def bayes_theorem(self, prior, likelihood, evidence):
        return (likelihood * prior) / evidence

    # Hypothesis Testing
    def z_test(self, sample_mean, population_mean, population_std, n):
        z_score = (sample_mean - population_mean) / (population_std / sqrt(n))
        p_value = stats.norm.cdf(z_score)
        return z_score, p_value

    def t_test(self, sample_mean, population_mean, sample_std, n):
        t_score = (sample_mean - population_mean) / (sample_std / sqrt(n))
        p_value = stats.t.cdf(t_score, df=n - 1)
        return t_score, p_value

    def chi_square_test(self, observed, expected):
        chi_square_stat, p_value = stats.chisquare(observed, expected)
        return chi_square_stat, p_value

    # Linear Regression and Correlation
    def linear_regression(self, x, y):
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        return slope, intercept, r_value ** 2, p_value


class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Math GUI Calc")

        # Initialize the calculator logic
        self.calc = MathCalc()

        # Add GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Drop-down for selecting type of calculation
        self.operation_label = tk.Label(self.root, text="Select Operation:")
        self.operation_label.grid(row=0, column=0)

        self.operation_var = tk.StringVar(self.root)
        self.operation_var.set("Statistics")
        self.operation_menu = tk.OptionMenu(self.root, self.operation_var,
                                            "Statistics", "Probability",
                                            "Combinatorics", "Hypothesis Testing",
                                            "Linear Regression", "Markov Chains")
        self.operation_menu.grid(row=0, column=1)

        # Entry for the user input (math expression)
        self.input_label = tk.Label(self.root, text="Enter Expression:")
        self.input_label.grid(row=1, column=0)

        self.input_entry = tk.Entry(self.root, width=40)
        self.input_entry.grid(row=1, column=1)

        # Button to calculate result
        self.calculate_button = tk.Button(self.root, text="Calculate", command=self.calculate)
        self.calculate_button.grid(row=2, column=0, columnspan=2)

        # Button to show the search equation for the operation
        self.search_equation_button = tk.Button(self.root, text="Search Equations", command=self.show_equations)
        self.search_equation_button.grid(row=3, column=0, columnspan=2)

        # Label to display the result
        self.result_label = tk.Label(self.root, text="Result:")
        self.result_label.grid(row=4, column=0)

        self.result_value = tk.Label(self.root, text="")
        self.result_value.grid(row=4, column=1)

    def calculate(self):
        global result
        operation = self.operation_var.get()
        user_input = self.input_entry.get()

        try:
            # Handle different operations
            if operation == "Statistics":
                result = self.handle_statistics(user_input)

            elif operation == "Probability":
                result = self.handle_probability(user_input)

            elif operation == "Combinatorics":
                result = self.handle_combinatorics(user_input)

            elif operation == "Hypothesis Testing":
                result = self.handle_hypothesis_testing(user_input)

            elif operation == "Linear Regression":
                result = self.handle_linear_regression(user_input)

            elif operation == "Markov Chains":
                result = self.handle_markov_chains(user_input)

            self.result_value.config(text=result)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def handle_statistics(self, user_input):
        data = list(map(float, user_input.split(",")))
        mean = statistics.mean(data)
        median = statistics.median(data)
        mode = statistics.mode(data)
        variance = statistics.variance(data)
        std_dev = statistics.stdev(data)
        return (f"Mean: {mean}\nMedian: {median}\nMode: {mode}\nVariance: {variance}\n"
                f"Standard Deviation: {std_dev}\n")

    def handle_probability(self, user_input):
        params = user_input.split(",")
        distribution_type = params[0].strip().lower()

        if distribution_type == "binomial":
            n, k, p = map(float, params[1:])
            return f"Binomial Probability: {self.calc.binomial_probability(n, k, p)}"
        elif distribution_type == "poisson":
            k, lam = map(float, params[1:])
            return f"Poisson Probability: {self.calc.poisson_probability(k, lam)}"
        elif distribution_type == "normal":
            x, mu, sigma = map(float, params[1:])
            return f"Normal Probability: {self.calc.normal_probability(x, mu, sigma)}"

    def handle_combinatorics(self, user_input):
        n, r = map(int, user_input.split(","))
        permutations = self.calc.permutations(n, r)
        combinations = self.calc.combinations(n, r)
        return f"Permutations: {permutations}\nCombinations: {combinations}"

    def handle_hypothesis_testing(self, user_input):
        test_type, *params = user_input.split(",")
        if test_type == "z-test":
            sample_mean, population_mean, population_std, n = map(float, params)
            z_score, p_value = self.calc.z_test(sample_mean, population_mean, population_std, n)
            return f"Z-Score: {z_score}\nP-Value: {p_value}"
        elif test_type == "t-test":
            sample_mean, population_mean, sample_std, n = map(float, params)
            t_score, p_value = self.calc.t_test(sample_mean, population_mean, sample_std, n)
            return f"T-Score: {t_score}\nP-Value: {p_value}"
        elif test_type == "chi-square":
            observed = list(map(int, params))
            expected = list(map(int, params))
            chi_square_stat, p_value = self.calc.chi_square_test(observed, expected)
            return f"Chi-Square Stat: {chi_square_stat}\nP-Value: {p_value}"

    def handle_linear_regression(self, user_input):
        x, y = zip(*[map(float, pair.split(",")) for pair in user_input.split(";")])
        slope, intercept, r_squared, p_value = self.calc.linear_regression(x, y)
        return f"Slope: {slope}\nIntercept: {intercept}\nR-squared: {r_squared}\nP-value: {p_value}"

    def show_equations(self):
        operation = self.operation_var.get()

        equations = {
            "Statistics": "1, 2, 3, 4, 5",
            "Probability": "(Only 1 type:) binomial/poisson/normal, 10, 5, 0.5",
            "Combinatorics": "5, 3",
            "Hypothesis Testing": "(Only 1 type:) z-test/t-test/chi-square, 50, 52, 10, 30",
            "Linear Regression": "1, 2; 2, 4; 3, 6; 4, 8",
        }

        messagebox.showinfo("Equations", equations.get(operation, "No equations available"))


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()