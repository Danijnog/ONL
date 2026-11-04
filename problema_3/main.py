import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import minimize, linprog

# Parâmetros dados no exercício (Tabela 1)
R_ALVO = 10000.0
CENARIOS = ["Mercado Normal", "Recessão Econômica", "Alta Demanda", "Pressão Competitiva"]
A1 = np.array([100000., 70000., 130000., 90000.]) # a_{1,i}
A2 = np.array([80000., 56000., 104000., 90000.])  # a_{2,i}

def receitas(p):
    """Receita em cada cenário: R_i(p1, p2) = a_{1,i}/p1 + a_{2,i}/p2."""

    return A1 / p[0] + A2 / p[1]

def f(p):
    """Função objetivo: pior desvio absoluto da receita em relação à meta, max_i |R_i - R_alvo|.
    Como os preços precisam ser positivos (R_i não está definida em p = 0), pontos com p <= 0
    recebem um valor muito alto, o que impede o simplex de sair do domínio.
    """

    if p[0] <= 0 or p[1] <= 0:
        return 1e12
    return np.max(np.abs(receitas(p) - R_ALVO))

def otimiza(metodo, p0):
    """Executa um método do scipy e guarda o histórico de f(p_k) a cada iteração."""

    hist = [f(p0)]
    cb = lambda xk, *args: hist.append(f(xk))
    options = {'xatol': 1e-10, 'fatol': 1e-10, 'maxiter': 2000} if metodo == "Nelder-Mead" else {'maxiter': 2000}
    res = minimize(f, p0, method=metodo, callback=cb, options=options)
    return res, hist

def referencia_lp():
    """Solução de referência: com u = 1/p1 e v = 1/p2 cada R_i é linear em (u, v), então o problema
    minimax vira um PL (min t s.t. -t <= a1_i u + a2_i v - R_alvo <= t). Serve só para conferir o resultado."""

    c = [0, 0, 1]  # variáveis (u, v, t), minimiza t
    A_ub = np.vstack([np.column_stack([ A1,  A2, -np.ones(4)]),
                      np.column_stack([-A1, -A2, -np.ones(4)])])
    b_ub = np.concatenate([np.full(4, R_ALVO), np.full(4, -R_ALVO)])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(1e-9, None), (1e-9, None), (0, None)])
    return res.x[2]

p0 = np.array([10., 10.])
print("p0 =", p0, " f(p0) =", f(p0))
print(f"Valor ótimo de referência (PL em u=1/p1, v=1/p2): {referencia_lp():.6f}")

# --- Comparação de métodos a partir do mesmo ponto inicial ---
res_all = {}
print(f"\n{'Método':<14} {'p1':>10} {'p2':>10} {'f(p*)':>14} {'iter':>5} {'aval.':>6}  convergiu")
for metodo in ("Nelder-Mead", "Powell", "BFGS"):
    res, hist = otimiza(metodo, p0)
    res_all[metodo] = (res, hist)
    print(f"{metodo:<14} {res.x[0]:10.5f} {res.x[1]:10.5f} {res.fun:14.8f} {res.nit:>5} {res.nfev:>6}  {res.success}")

# --- Nelder-Mead (método escolhido): detalhes do resultado ---
x, h = res_all["Nelder-Mead"]
x = x.x
print(f"\n=== Nelder-Mead ===")
print(f"p* = [{x[0]:.5f}, {x[1]:.5f}]   f(p*) = {f(x):.6f}")
print(f"{'Cenário':<22} {'R_i(p*)':>12} {'|R_i - R_alvo|':>16}")
for nome, Ri in zip(CENARIOS, receitas(x)):
    print(f"{nome:<22} {Ri:12.4f} {abs(Ri - R_ALVO):16.4f}")

# --- A solução não é única: Nelder-Mead a partir de vários pontos iniciais ---
print("\n=== Nelder-Mead a partir de vários pontos iniciais ===")
print(f"{'p0':>14} {'p1':>10} {'p2':>10} {'f(p*)':>12} {'1/p1 + 0.8/p2':>15}")
starts = [(10., 10.), (20., 15.), (15., 30.), (40., 12.), (12., 60.)]
paths = {}
for s in starts:
    path = [np.array(s)]
    r = minimize(f, np.array(s), method="Nelder-Mead", callback=lambda xk, *a: path.append(xk.copy()),
                 options={'xatol': 1e-10, 'fatol': 1e-10, 'maxiter': 2000})
    paths[s] = (np.array(path), r.x)
    print(f"{str(s):>14} {r.x[0]:10.4f} {r.x[1]:10.4f} {r.fun:12.6f} {1/r.x[0] + 0.8/r.x[1]:15.8f}")

# --- Gráficos ---
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))

# (a) Curvas de nível de f e caminhos do Nelder-Mead
P1, P2 = np.meshgrid(np.linspace(5, 60, 400), np.linspace(5, 60, 400))
F = np.max(np.abs(A1[:, None, None] / P1 + A2[:, None, None] / P2 - R_ALVO), axis=0)
cs = ax[0].contourf(P1, P2, np.log10(F), levels=30, cmap="viridis")
fig.colorbar(cs, ax=ax[0], label=r"$\log_{10} f(p)$")
p2_curva = np.linspace(8.01, 60, 400)
p1_curva = 1.0 / (0.1 - 0.8 / p2_curva)
ok = (p1_curva > 0) & (p1_curva < 60)
ax[0].plot(p1_curva[ok], p2_curva[ok], 'r--', lw=2, label=r"$1/p_1 + 0{,}8/p_2 = 0{,}1$ (ótimos)")
for s, (path, xf) in paths.items():
    ax[0].plot(path[:, 0], path[:, 1], '.-', color="w", lw=.8, ms=3)
    ax[0].plot(*s, 'ws', ms=5)
    ax[0].plot(*xf, 'r*', ms=10)
ax[0].set_xlim(5, 60); ax[0].set_ylim(5, 60)
ax[0].set_xlabel("$p_1$"); ax[0].set_ylabel("$p_2$"); ax[0].set_title("Superfície de $f(p)$ e trajetórias do Nelder-Mead")
ax[0].legend(loc="upper right")

# (b) Convergência
for metodo, (r, hist) in res_all.items():
    ax[1].semilogy(hist, 'o-', ms=3, label=f"{metodo} ({r.nfev} aval.)")
ax[1].axhline(3000, color="k", ls=":", label="$f^*=3000$")
ax[1].set_xlabel("# Iterações"); ax[1].set_ylabel("$f(p_k)$"); ax[1].set_title("Convergência")
ax[1].grid(True, which="both", alpha=.3); ax[1].legend()
plt.tight_layout(); plt.savefig("resultado.png", dpi=150)
