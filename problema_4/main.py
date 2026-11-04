import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Parâmetros dados no exercício
k1, k2, k3 = 1000., 1500., 2000.  # N/m
P = 100.                          # N

# Hessiana (constante) e termo linear de U(x) = 1/2 x^T H x - b^T x
H = np.array([[k2 + k3, -k3],
              [-k3, k1 + k3]])
b = np.array([0., P])

def U(x):
    """Energia potencial total: U = 1/2 k2 x1^2 + 1/2 k3 (x2 - x1)^2 + 1/2 k1 x2^2 - P x2."""

    return 0.5 * k2 * x[0]**2 + 0.5 * k3 * (x[1] - x[0])**2 + 0.5 * k1 * x[1]**2 - P * x[1]

def grad(x):
    """Gradiente de U (equivale a H x - b)."""

    return np.array([k2 * x[0] - k3 * (x[1] - x[0]),
                     k3 * (x[1] - x[0]) + k1 * x[1] - P])

def newton(x0, tol=1e-12, maxit=50):
    """Método de Newton. Como U é quadrática, a Hessiana é constante e o método converge em 1 iteração."""

    x = x0.copy()
    hist = [dict(k=0, U=U(x), gn=np.linalg.norm(grad(x)), x=x.copy())]
    for k in range(1, maxit + 1):
        g = grad(x)
        if np.linalg.norm(g) < tol:
            break
        x = x - np.linalg.solve(H, g)
        hist.append(dict(k=k, U=U(x), gn=np.linalg.norm(grad(x)), x=x.copy()))
    return x, hist

def steepest_descent(x0, tol=1e-8, maxit=1000):
    """Gradiente com busca linear exata (alpha = g^T g / g^T H g), para comparação."""

    x = x0.copy()
    hist = [dict(k=0, U=U(x), gn=np.linalg.norm(grad(x)), x=x.copy())]
    for k in range(1, maxit + 1):
        g = grad(x)
        if np.linalg.norm(g) < tol:
            break
        x = x - (g @ g) / (g @ H @ g) * g
        hist.append(dict(k=k, U=U(x), gn=np.linalg.norm(grad(x)), x=x.copy()))
    return x, hist

def cg(x0, tol=1e-8):
    """Gradientes conjugados (Fletcher-Reeves) com busca linear exata. Em R^n, converge em no máximo n iterações."""

    x = x0.copy()
    g = grad(x)
    d = -g
    hist = [dict(k=0, U=U(x), gn=np.linalg.norm(g), x=x.copy())]
    for k in range(1, len(x0) + 1):
        if np.linalg.norm(g) < tol:
            break
        x = x + (-(g @ d) / (d @ H @ d)) * d
        g_new = grad(x)
        d = -g_new + (g_new @ g_new) / (g @ g) * d
        g = g_new
        hist.append(dict(k=k, U=U(x), gn=np.linalg.norm(g), x=x.copy()))
    return x, hist

x0 = np.array([0., 0.])
autovalores = np.linalg.eigvalsh(H)
print("Hessiana H =\n", H)
print("Autovalores de H:", autovalores, " -> definida positiva, cond(H) =", autovalores[-1] / autovalores[0])
print("x0 =", x0, " U(x0) =", U(x0))

# Solução analítica: grad U = H x - b = 0
x_exato = np.linalg.solve(H, b)

res = {}
for nome, metodo in (("Newton", newton), ("Gradientes conjugados (FR)", cg), ("Gradiente (busca exata)", steepest_descent)):
    x, h = metodo(x0)
    res[nome] = (x, h)
    print(f"\n=== {nome} ===")
    print(f"{'k':>3} {'U(x_k) [J]':>16} {'||grad||':>12}  x_k [m]")
    for r in h[:8]:
        print(f"{r['k']:>3} {r['U']:16.10f} {r['gn']:12.3e}  {r['x']}")
    if len(h) > 8:
        print(f"... ({len(h) - 1} iterações no total)")
    print(f"x* = {x}  U(x*) = {U(x):.10f}  erro vs exato = {np.linalg.norm(x - x_exato):.2e}")

# Referência: BFGS do scipy, que aproxima a Hessiana sem precisar dela
r = minimize(U, x0, jac=grad, method="BFGS", options={'gtol': 1e-10})
print(f"\n=== BFGS (scipy) ===\nx* = {r.x}  U(x*) = {r.fun:.10f}  iter = {r.nit}  aval. f = {r.nfev}  aval. grad = {r.njev}")

print(f"\nSolução exata (H x = b): x1* = {x_exato[0]:.6f} m, x2* = {x_exato[1]:.6f} m, U* = {U(x_exato):.6f} J")
# Conferência física: equilíbrio de forças nos carrinhos A e B
x1, x2 = x_exato
print(f"Equilíbrio em A: k2 x1 - k3 (x2 - x1) = {k2*x1 - k3*(x2 - x1):.2e} N (esperado 0)")
print(f"Equilíbrio em B: k1 x2 + k3 (x2 - x1) = {k1*x2 + k3*(x2 - x1):.6f} N (esperado P = {P} N)")

# --- Gráficos ---
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))

g1, g2 = np.meshgrid(np.linspace(-0.01, 0.08, 300), np.linspace(-0.01, 0.08, 300))
Z = 0.5 * k2 * g1**2 + 0.5 * k3 * (g2 - g1)**2 + 0.5 * k1 * g2**2 - P * g2
ax[0].contour(g1, g2, Z, levels=25, cmap="viridis")
cores = {"Newton": "r", "Gradientes conjugados (FR)": "b", "Gradiente (busca exata)": "g"}
for nome, (x, h) in res.items():
    caminho = np.array([r['x'] for r in h])
    ax[0].plot(caminho[:, 0], caminho[:, 1], 'o-', color=cores[nome], ms=4, label=nome)
ax[0].plot(*x_exato, 'k*', ms=14, label="Equilíbrio")
ax[0].set_xlabel("$x_1$ [m]"); ax[0].set_ylabel("$x_2$ [m]"); ax[0].set_title("Curvas de nível de $U$ e trajetórias")
ax[0].legend()

for nome, (x, h) in res.items():
    ks = [r['k'] for r in h]
    ax[1].semilogy(ks, [max(r['U'] - U(x_exato), 1e-17) for r in h], 'o-', color=cores[nome], label=nome)
ax[1].set_xlabel("# Iterações"); ax[1].set_title(r"$U(x_k) - U(x^*)$")
ax[1].grid(True, which="both", alpha=.3); ax[1].legend()
plt.tight_layout(); plt.savefig("resultado.png", dpi=150)
