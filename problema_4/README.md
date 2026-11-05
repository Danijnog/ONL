# Posição de equilíbrio de carrinhos com molas

Determinação da posição de equilíbrio de um sistema de dois carrinhos ligados por três molas lineares minimizando a energia potencial elástica total.

### Problema

```
min_{x1,x2}  U(x1, x2) = 1/2 k2 x1² + 1/2 k3 (x2 − x1)² + 1/2 k1 x2² − P x2
```

com `k1 = 1000 N/m`, `k2 = 1500 N/m`, `k3 = 2000 N/m` e `P = 100 N`. `x1` e `x2` são os deslocamentos dos carrinhos A e B (m).

Reescrevendo como `U(x) = ½ xᵀ H x − bᵀ x`:

```
H = [ k2+k3   −k3 ]  =  [ 3500  −2000 ]        b = [ 0 ]
    [ −k3   k1+k3 ]     [ −2000  3000 ]            [ P ]
```

### Características da função objetivo

- Diferenciabilidade: diferenciável em todo ℝ² (polinômio de grau 2), com `∇U = H x − b`.
- Convexidade: estritamente convexa. A Hessiana é constante e definida positiva (autovalores 1234,4 e 5265,6).
- Modalidade: unimodal, com um único ponto estacionário que é o mínimo global.
- Continuidade: contínua em todo ℝ².

### Método escolhido para resolver o problema

Método de Newton. Como `U` é quadrática, o modelo de segunda ordem do método é exato, e o passo `x − H⁻¹ ∇U(x)` chega ao mínimo em **uma** iteração. Resolver um sistema 2×2 tem custo desprezível, então a desvantagem usual do Newton (calcular e fatorar a Hessiana) não existe aqui.

Para comparação foram rodados também os gradientes conjugados (Fletcher-Reeves, busca linear exata), o gradiente com busca linear exata e o BFGS do scipy.

### Como executar

Requisitos: Python 3, `numpy`, `scipy`, `matplotlib`.

```bash
python3 main.py
```

O script imprime as tabelas de convergência no terminal e salva `resultado.png`.

### Resultado obtido

A partir de `x0 = [0, 0]` (`U(x0) = 0`):

| Grandeza | Valor encontrado |
|---|---|
| x1* | 0,030769 m |
| x2* | 0,053846 m |
| U(x*) | −2,692308 J |

Solução exata: `x1* = k3 P / det(H) = 2000·100 / 6,5·10⁶` e `x2* = (k2+k3) P / det(H)`.

Comparação dos métodos:

| Método | Iterações | Erro vs solução exata |
|---|---|---|
| Newton | 1 | 0 |
| Gradientes conjugados (FR) | 2 | ~7e-18 |
| BFGS (scipy) | 3 | — |
| Gradiente (busca exata) | 48 (para ‖∇U‖ < 1e-8) | ~5e-12 |

O Newton resolve em uma iteração porque a função é quadrática; os gradientes conjugados precisam de no máximo n = 2 iterações; o gradiente simples zigue-zagueia (cond(H) ≈ 4,27) e precisa de dezenas de iterações.

Conferência física: no equilíbrio, `k2 x1 − k3 (x2 − x1) = 0` (carrinho A) e `k1 x2 + k3 (x2 − x1) = 100 N = P` (carrinho B).

### Como ler a saída

| Coluna | Significado |
|---|---|
| `k` | Número da iteração |
| `U(x_k)` | Energia potencial na iteração k (J) |
| `||grad||` | Norma do gradiente na iteração k (critério de parada) |
| `x_k` | Deslocamentos dos carrinhos na iteração k (m) |
