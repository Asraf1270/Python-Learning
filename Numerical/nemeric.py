import math
import os
from datetime import datetime

# ============================================================
# EQUATION HANDLING
# ============================================================

def get_function(equation_str):
    """
    Convert user equation string into a callable function.
    Supported: sin, cos, tan, exp, log, sqrt, pi, e, ^ (as **)
    """
    equation_str = equation_str.replace('^', '**')
    equation_str = equation_str.replace('ln(', 'log(')
    
    def f(x):
        try:
            return eval(equation_str, {
                "x": x,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "exp": math.exp, "log": math.log, "ln": math.log,
                "sqrt": math.sqrt, "pi": math.pi, "e": math.e,
                "abs": abs
            })
        except Exception as ex:
            raise ValueError(f"Error evaluating equation: {ex}")
    return f


def get_derivative(f):
    """Numerical derivative using central difference"""
    def df(x, h=1e-7):
        return (f(x + h) - f(x - h)) / (2 * h)
    return df


# ============================================================
# NUMERICAL METHODS
# ============================================================

def bisection_method(f, a, b, tol, max_iter):
    """Bisection Method"""
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs.")
    
    table = []
    c_old = None
    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)
        error = abs(c - c_old) if c_old is not None else abs(b - a) / 2
        table.append([i, a, b, c, fc, error])
        
        if abs(fc) < tol or error < tol:
            return c, table, i
        if f(a) * fc < 0:
            b = c
        else:
            a = c
        c_old = c
    return c, table, max_iter


def fixed_point_iteration(g, x0, tol, max_iter):
    """Fixed Point Iteration: x = g(x)"""
    table = []
    x = x0
    for i in range(1, max_iter + 1):
        x_new = g(x)
        error = abs(x_new - x)
        table.append([i, x, x_new, error])
        if error < tol or abs(g(x_new) - x_new) < tol:
            return x_new, table, i
        x = x_new
    return x_new, table, max_iter


def newton_raphson(f, df, x0, tol, max_iter):
    """Newton-Raphson Method"""
    table = []
    x = x0
    for i in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise ValueError("Derivative is zero. Method fails.")
        x_new = x - fx / dfx
        error = abs(x_new - x)
        table.append([i, x, fx, dfx, x_new, error])
        if error < tol or abs(f(x_new)) < tol:
            return x_new, table, i
        x = x_new
    return x_new, table, max_iter


def secant_method(f, x0, x1, tol, max_iter):
    """Secant Method"""
    table = []
    for i in range(1, max_iter + 1):
        f0 = f(x0)
        f1 = f(x1)
        if (f1 - f0) == 0:
            raise ValueError("Division by zero in secant formula.")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        error = abs(x2 - x1)
        table.append([i, x0, x1, f0, f1, x2, error])
        if error < tol or abs(f(x2)) < tol:
            return x2, table, i
        x0, x1 = x1, x2
    return x2, table, max_iter


def false_position_method(f, a, b, tol, max_iter):
    """False Position (Regula Falsi) Method"""
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs.")
    
    table = []
    c_old = None
    for i in range(1, max_iter + 1):
        fa, fb = f(a), f(b)
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)
        error = abs(c - c_old) if c_old is not None else abs(b - a)
        table.append([i, a, b, c, fc, error])
        
        if abs(fc) < tol or error < tol:
            return c, table, i
        if fa * fc < 0:
            b = c
        else:
            a = c
        c_old = c
    return c, table, max_iter


# ============================================================
# FILE OUTPUT
# ============================================================

def format_value(v):
    if isinstance(v, float):
        return f"{v:.10f}"
    return str(v)


def save_to_file(method_name, equation, inputs, headers, table, answer, iterations):
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/{method_name.replace(' ', '_')}_{timestamp}.txt"
    
    with open(filename, "w", encoding="utf-8") as file:
        file.write("=" * 70 + "\n")
        file.write(f"  NUMERICAL METHOD REPORT\n")
        file.write("=" * 70 + "\n")
        file.write(f"Method       : {method_name}\n")
        file.write(f"Date & Time  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Equation     : f(x) = {equation}\n")
        file.write("-" * 70 + "\n")
        file.write("INPUT DATA:\n")
        for key, val in inputs.items():
            file.write(f"  {key:<15}: {val}\n")
        file.write("-" * 70 + "\n")
        file.write("ITERATION TABLE:\n")
        file.write("-" * 70 + "\n")
        
        # Header
        header_line = " | ".join(f"{h:^14}" for h in headers)
        file.write(header_line + "\n")
        file.write("-" * len(header_line) + "\n")
        
        for row in table:
            row_line = " | ".join(f"{format_value(v):^14}" for v in row)
            file.write(row_line + "\n")
        
        file.write("-" * 70 + "\n")
        file.write("FINAL RESULT:\n")
        file.write(f"  Root approximation : {answer:.10f}\n")
        file.write(f"  Iterations used    : {iterations}\n")
        file.write("=" * 70 + "\n")
    
    return filename


# ============================================================
# MENU & INPUTS
# ============================================================

def print_menu():
    print("\n" + "=" * 60)
    print("       NUMERICAL METHODS SOLVER")
    print("=" * 60)
    print("  1. Bisection Method")
    print("  2. Fixed Point Iteration")
    print("  3. Newton-Raphson Method")
    print("  4. Secant Method")
    print("  5. False Position Method")
    print("  0. Exit")
    print("=" * 60)


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  [!] Please enter a valid number.")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  [!] Please enter a valid integer.")


def print_table(headers, table):
    header_line = " | ".join(f"{h:^13}" for h in headers)
    print("\n" + "-" * len(header_line))
    print(header_line)
    print("-" * len(header_line))
    for row in table:
        row_line = " | ".join(f"{format_value(v):^13}" for v in row)
        print(row_line)
    print("-" * len(header_line))


# ============================================================
# MAIN
# ============================================================

def main():
    while True:
        print_menu()
        choice = input("Select a method (0-5): ").strip()
        
        if choice == "0":
            print("\nThank you for using Numerical Methods Solver. Goodbye!")
            break
        
        if choice not in ["1", "2", "3", "4", "5"]:
            print("  [!] Invalid choice. Try again.")
            continue
        
        try:
            # ---------- Equation input ----------
            print("\n--- Equation Input ---")
            print("Use 'x' as the variable. Examples: x**3 - x - 2, cos(x) - x, exp(x) - 3*x")
            eq_str = input("Enter f(x) = ").strip()
            f = get_function(eq_str)
            
            # ---------- Common parameters ----------
            tol = get_float("Tolerance (e.g., 0.0001): ")
            max_iter = get_int("Maximum iterations (e.g., 50): ")
            
            # ---------- Method-specific input ----------
            if choice == "1":
                method = "Bisection Method"
                print("\n--- Bisection Inputs ---")
                a = get_float("Lower bound a: ")
                b = get_float("Upper bound b: ")
                root, table, iters = bisection_method(f, a, b, tol, max_iter)
                headers = ["Iter", "a", "b", "c", "f(c)", "Error"]
                inputs = {"f(x)": eq_str, "a": a, "b": b, "Tolerance": tol, "Max iter": max_iter}
            
            elif choice == "2":
                method = "Fixed Point Iteration"
                print("\n--- Fixed Point Iteration ---")
                print("NOTE: Provide g(x) such that x = g(x). Example: (x + 2)**(1/3)")
                g_str = input("Enter g(x) = ").strip()
                g = get_function(g_str)
                x0 = get_float("Initial guess x0: ")
                root, table, iters = fixed_point_iteration(g, x0, tol, max_iter)
                headers = ["Iter", "x", "g(x)", "Error"]
                inputs = {"g(x)": g_str, "x0": x0, "Tolerance": tol, "Max iter": max_iter}
            
            elif choice == "3":
                method = "Newton-Raphson Method"
                print("\n--- Newton-Raphson Inputs ---")
                x0 = get_float("Initial guess x0: ")
                df = get_derivative(f)
                root, table, iters = newton_raphson(f, df, x0, tol, max_iter)
                headers = ["Iter", "x", "f(x)", "f'(x)", "x_new", "Error"]
                inputs = {"f(x)": eq_str, "x0": x0, "Tolerance": tol, "Max iter": max_iter,
                          "Derivative": "numerical (central difference)"}
            
            elif choice == "4":
                method = "Secant Method"
                print("\n--- Secant Inputs ---")
                x0 = get_float("First initial guess x0: ")
                x1 = get_float("Second initial guess x1: ")
                root, table, iters = secant_method(f, x0, x1, tol, max_iter)
                headers = ["Iter", "x0", "x1", "f(x0)", "f(x1)", "x2", "Error"]
                inputs = {"f(x)": eq_str, "x0": x0, "x1": x1, "Tolerance": tol, "Max iter": max_iter}
            
            elif choice == "5":
                method = "False Position Method"
                print("\n--- False Position Inputs ---")
                a = get_float("Lower bound a: ")
                b = get_float("Upper bound b: ")
                root, table, iters = false_position_method(f, a, b, tol, max_iter)
                headers = ["Iter", "a", "b", "c", "f(c)", "Error"]
                inputs = {"f(x)": eq_str, "a": a, "b": b, "Tolerance": tol, "Max iter": max_iter}
            
            # ---------- Display ----------
            print(f"\n\n>>> {method} - Results <<<")
            print_table(headers, table)
            print(f"\n  Approximate Root : {root:.10f}")
            print(f"  Iterations Used  : {iters}")
            print(f"  f(root)          : {f(root):.10e}")
            
            # ---------- Save ----------
            filename = save_to_file(method, eq_str, inputs, headers, table, root, iters)
            print(f"\n  [✓] Full report saved to: {filename}")
        
        except ValueError as e:
            print(f"\n  [!] Error: {e}")
        except Exception as e:
            print(f"\n  [!] Unexpected error: {e}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()