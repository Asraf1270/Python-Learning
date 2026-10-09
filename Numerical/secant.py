def f(x):
    return x**3 - 2*x -5

x0 = 2
x1 = 3

f0 = f(x0)
f1 = f(x1)

for i in range(10):
    x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
    f2 = f(x2)
    
    print(f"Iteration {i+1}: x = {x2}, f(x) = {f2}")
    
    if abs(f2) < 1e-6:
        print("Root found:", x2)
        break
    
    x0, f0 = x1, f1
    x1, f1 = x2, f2