import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.linalg import eigh

K = np.array([[2., -1., 0.], [-1., 2., -1.], [0., -1., 1.]]) # Dado no exercício
M = np.eye(3) # Matriz identidade 3x3

def R(x):
    """ Função objetivo: R(x) = (x^T K x) / (x^T M x)."""

    return (x @ K @ x) / (x @ M @ x)

def grad(x):
    """Calcula o gradiente de R(x) = (x^T K x) / (x^T M x)."""

    r = R(x)
    return 2.0 * (K @ x - r * (M @ x)) / (x @ M @ x)

def line_search_exact(x, d):
    """Calcula a busca linear exata para o passo do gradiente conjugado."""

    V = np.column_stack([x, d])
    Kr, Mr = V.T @ K @ V, V.T @ M @ V # Projeção de K e M no subespaço gerado 2x2
    w, U = eigh(Kr, Mr)
    c = U[:, 0]
    y = V @ c
    # o sinal do autovetor 2x2 e arbitrario: fixa orientacao y.x > 0
    # para manter x_new consistente com d (grad(-x) = -grad(x))
    if y @ x < 0:
        y = -y
    return y

def cg(x0, variant="PR", tol=1e-12, maxit=50):
    """Gradientes conjugados."""

    x = x0 / np.linalg.norm(x0)
    g = grad(x)
    d = -g
    hist = [dict(k=0, R=R(x), gn=np.linalg.norm(g), x=x.copy())]
    
    for k in range(1, maxit + 1):
        if np.linalg.norm(g) < tol:
            break
        y = line_search_exact(x, d)
        x_new = y / np.linalg.norm(y)
        g_new = grad(x_new)
        if variant == "FR": # Fletcher-Reeves para calcular o beta
            beta = (g_new @ g_new) / (g @ g)

        else:  # Polak-Ribiere para calcular o beta
            beta = max(0.0, g_new @ (g_new - g) / (g @ g))
        d = -g_new + beta * d

        # garante direcao de descida
        if d @ g_new >= 0:
            d = -g_new
        x, g = x_new, g_new
        hist.append(dict(k=k, R=R(x), gn=np.linalg.norm(g), x=x.copy()))
    return x, hist

lam, V = eigh(K, M)
lam1, v1 = lam[0], V[:, 0]
if v1[-1] < 0:
    v1 = -v1

x0 = np.array([1., 1., 1.])
print("Autovalores de K:", lam)
print("x0 =", x0, " R(x0) =", R(x0))

res = {}
for var in ("PR", "FR"):
    x, h = cg(x0, var)

    res[var] = (x, h)
    if x[-1] < 0:
        x = -x

    print(f"\n=== Gradientes conjugados ({var}) ===")
    print(f"{'k':>2} {'R(x_k)':>16} {'R-lam1':>12} {'||grad||':>12}  x_k")
    for r in h:
        print(f"{r['k']:>2} {r['R']:16.12f} {r['R']-lam1:12.3e} {r['gn']:12.3e}  {np.round(r['x'],6)}")
    print("x* =", x, " R(x*) =", R(x), " omega1 =", np.sqrt(R(x)))
    print("erro vs v1 (exato):", np.linalg.norm(x - v1))

print(f"\nSolucao exata: Frequência natural do sistema = {np.sqrt(lam1):.3f},  Vetor de deslocamento das massas = {[f'{v:.3f}' for v in v1]}")

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for var, (x, h) in res.items():
    ks = [r['k'] for r in h]
    ax[0].semilogy(ks, [max(r['R'] - lam1, 1e-17) for r in h], 'o-', label=var)
    ax[1].semilogy(ks, [max(r['gn'], 1e-17) for r in h], 'o-', label=var)
ax[0].set_title(r"$R(x_k)-\lambda_1$"); ax[1].set_title(r"$\|\nabla R(x_k)\|$")

for a in ax:
    a.set_xlabel("# Iterações"); a.grid(True, which="both", alpha=.3); a.legend()
plt.tight_layout(); plt.savefig("convergencia_cg.png", dpi=150)