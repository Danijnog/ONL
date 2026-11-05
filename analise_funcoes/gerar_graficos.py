import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Configurações de estilo para publicação/relatório acadêmico (UFMG)
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 14
})

# ==========================================
# PROBLEMA 1: Quociente de Rayleigh (3D/Slice 2D)
# ==========================================
def gerar_grafico_p1():
    # Matrizes do problema
    K = np.array([[2.0, -1.0, 0.0],
                  [-1.0, 2.0, -1.0],
                  [0.0, -1.0, 1.0]])
    M = np.eye(3)

    # Projetando no plano (x1, x2) mantendo x3 fixo em 1.0 para visualização 2D
    x1 = np.linspace(-3, 3, 300)
    x2 = np.linspace(-3, 3, 300)
    X1, X2 = np.meshgrid(x1, x2)
    x3 = 1.0

    R = np.zeros_like(X1)
    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            x = np.array([X1[i, j], X2[i, j], x3])
            R[i, j] = (x.T @ K @ x) / (x.T @ M @ x)

    fig, ax = plt.subplots(figsize=(7, 5))
    contour = ax.contourf(X1, X2, R, levels=30, cmap='viridis')
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label(r'Quociente de Rayleigh $R(x_1, x_2, x_3=1)$')
    
    ax.set_title(r'Problema 1: Quociente de Rayleigh (Corte $x_3 = 1.0$)')
    ax.set_xlabel(r'$x_1$')
    ax.set_ylabel(r'$x_2$')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('problema1_quociente_rayleigh.pdf', format='pdf', dpi=300)
    plt.close()
    print("Gráfico do Problema 1 salvo com sucesso.")

# ==========================================
# PROBLEMA 2: Regularização Total Variation (TV) + Fidelidade
# ==========================================
def gerar_grafico_p2():
    # Ilustração 2D dos termos para 2 pixels adjacentes (x1, x2) com b = (1.5, 0.5)
    b1, b2 = 1.5, 0.5
    lam = 0.5
    eps = 1e-4

    x1 = np.linspace(-0.5, 2.5, 300)
    x2 = np.linspace(-0.5, 2.5, 300)
    X1, X2 = np.meshgrid(x1, x2)

    # Fidelidade: ||Ax - b||^2 (supondo A = Identidade para representação gráfica)
    fidelidade = (X1 - b1)**2 + (X2 - b2)**2
    # Regularização TV: sqrt((x2 - x1)^2 + eps)
    tv = np.sqrt((X2 - X1)**2 + eps)
    
    Z = fidelidade + lam * tv

    fig, ax = plt.subplots(figsize=(7, 5))
    contour = ax.contourf(X1, X2, Z, levels=30, cmap='magma')
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label(r'$f(x_1, x_2) = ||x - b||_2^2 + \lambda \cdot TV(x)$')
    
    # Ponto observado b
    ax.plot(b1, b2, 'r*', markersize=12, label=r'Dado Medido $b$')
    
    ax.set_title(r'Problema 2: Função Objetivo de Restauração de Imagem (TV)')
    ax.set_xlabel(r'$x_1$ (Pixel 1)')
    ax.set_ylabel(r'$x_2$ (Pixel 2)')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('problema2_regularizacao_tv.pdf', format='pdf', dpi=300)
    plt.close()
    print("Gráfico do Problema 2 salvo com sucesso.")

# ==========================================
# PROBLEMA 3: Minimax da Precificação (Não-Diferenciável)
# ==========================================
def gerar_grafico_p3():
    # Parâmetros da Tabela 1
    cenarios = [
        (100000, 80000),   # Cenário 1
        (70000, 56000),    # Cenário 2
        (130000, 104000),  # Cenário 3
        (90000, 90000)     # Cenário 4
    ]
    R_alvo = 10000

    p1 = np.linspace(2, 20, 300)
    p2 = np.linspace(2, 20, 300)
    P1, P2 = np.meshgrid(p1, p2)

    # Cálculo da função Minimax f(p1, p2) = max_i |R_i(p1, p2) - R_alvo|
    desvios = []
    for a1, a2 in cenarios:
        R_i = (a1 / P1) + (a2 / P2)
        desvios.append(np.abs(R_i - R_alvo))

    Z = np.maximum.reduce(desvios)

    fig, ax = plt.subplots(figsize=(7, 5))
    contour = ax.contourf(P1, P2, Z, levels=30, cmap='plasma')
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label(r'$\max_i |R_i(p_1, p_2) - R_{\mathrm{alvo}}|$')

    ax.set_title(r'Problema 3: Minimax da Precificação (Não-Diferenciável)')
    ax.set_xlabel(r'Preço $p_1$')
    ax.set_ylabel(r'Preço $p_2$')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('problema3_minimax_precificacao.pdf', format='pdf', dpi=300)
    plt.close()
    print("Gráfico do Problema 3 salvo com sucesso.")

# ==========================================
# PROBLEMA 4: Energia Potencial de Carrinhos (Quadrática/Convexa)
# ==========================================
def gerar_grafico_p4():
    # Parâmetros do Problema 4
    k1, k2, k3 = 1000.0, 1500.0, 2000.0
    P = 100.0

    x1 = np.linspace(-0.05, 0.15, 300)
    x2 = np.linspace(-0.05, 0.15, 300)
    X1, X2 = np.meshgrid(x1, x2)

    # U(x1, x2) = 0.5*k2*x1^2 + 0.5*k3*(x2 - x1)^2 + 0.5*k1*x2^2 - P*x2
    U = 0.5 * k2 * X1**2 + 0.5 * k3 * (X2 - X1)**2 + 0.5 * k1 * X2**2 - P * X2

    fig, ax = plt.subplots(figsize=(7, 5))
    contour = ax.contourf(X1, X2, U, levels=30, cmap='coolwarm')
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label(r'Energia Potencial $U(x_1, x_2)$ [J]')

    # Ponto de Mínimo Analítico para destacar
    # grad U = 0 -> [(k2+k3)x1 - k3*x2 = 0], [-k3*x1 + (k1+k3)x2 = P]
    A = np.array([[k2 + k3, -k3], [-k3, k1 + k3]])
    b = np.array([0.0, P])
    x_opt = np.linalg.solve(A, b)
    ax.plot(x_opt[0], x_opt[1], 'r*', markersize=12, label=f'Mínimo Ótimo ({x_opt[0]:.3f}, {x_opt[1]:.3f})')

    ax.set_title(r'Problema 4: Energia Potencial Total (Forma Quadrática Convexa)')
    ax.set_xlabel(r'Deslocamento $x_1$ [m]')
    ax.set_ylabel(r'Deslocamento $x_2$ [m]')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig('problema4_energia_potencial.pdf', format='pdf', dpi=300)
    plt.close()
    print("Gráfico do Problema 4 salvo com sucesso.")

if __name__ == "__main__":
    gerar_grafico_p1()
    gerar_grafico_p2()
    gerar_grafico_p3()
    gerar_grafico_p4()