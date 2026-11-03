# Frequência natural fundamental por Gradientes Conjugados

Minimização do quociente de Rayleigh de um sistema massa-mola com 3 graus de
liberdade, usando o método dos gradientes conjugados com busca linear exata.

### Problema

A frequência natural fundamental do sistema é obtida minimizando

```
R(x) = (xᵀ K x) / (xᵀ M x),     ω₁² = min R(x)
```

com

```
M = [1  0  0]        K = [ 2 -1  0]
    [0  1  0]            [-1  2 -1]
    [0  0  1]            [ 0 -1  1]
```

`x = [x1, x2, x3]ᵀ` são os deslocamentos das massas (m), `K` é a rigidez (N/m)
e `M` é a massa (kg).

### Características da função objetivo

- Diferenciabilidade: diferenciável em todos os pontos do seu domínio, exceto na origem (\(x = 0\)). Para qualquer vetor não-nulo x que deseja-se otimizar, tanto o numerador quanto o denominador são funções polinomiais quadráticas.
- Convexidade: A superfície do quociente de Rayleigh não é convexa globalmente, apresentando múltiplos pontos críticos (máximos, mínimos e pontos de sela).
- Modalidade: Apesar de apresentar múltiplos pontos críticos, é considerada unimodal, pois seus pontos de máximo e mínimo globais estão associados aos seus autovalores: o quociente de Rayleigh atinge seu valor mínimo global no autovetor associado ao menor autovalor, e seu valor máximo global no autovetor associado ao maior autovalor.
Todos os outros autovetores intermediários (com autovalores entre o mínimo e o máximo) comportam-se estritamente como pontos de sela.
- Continuidade: Em x = 0, a função é indefinida. Em  ℝ³ \ {0} a função é contínua.
- Gradiente: `∇R(x) = 2 (Kx − R(x)·x) / (xᵀx)` (com M = I).

### Método escolhido para resolver o problema
Método dos gradientes conjugados. O problema possui uma equivalência estrutural com o apresentado no método dos gradientes conjugados, se tratando de um sistema linear. Envolve o cálculo de autovalores do sistema também, e o método é adequado para este fim. Outra possibilidade considerada foi os Métodos de Newton / Quase-Newton, mas envolveria calcular e armazenar a Hessiana $H \in \mathbb{R}^{3\times 3}$. Embora eficientes, adicionam custo computacional desnecessário em comparação às direções conjugadas, enquanto somente o método do gradiente pode possuir uma convergência lenta para o problema analisado.

### Como executar

Requisitos: Python 3, `numpy`, `scipy`, `matplotlib`.

```bash
python3 main.py
```

O script imprime as tabelas de convergência no terminal e salva
`convergencia_cg.png`.


### Resultado obtido

| Grandeza | Valor encontrado
|---|---|---|
| x* (normalizado) | [0,32799; 0,59101; 0,73698]ᵀ 
| ω₁² = R(x*) | 0,198062264195
| ω₁ | 0,445042 rad/s

Os autovalores de K são λ₁ = 0,19806, λ₂ = 1,55496 e λ₃ = 3,24698.

### Como ler a saída

Para cada variante (PR e FR) o script imprime uma tabela com as colunas:

| Coluna | Significado |
|---|---|
| `k` | Número da iteração |
| `R(x_k)` | Valor do quociente de Rayleigh na iteração k (estimativa de ω²) |
| `R-lam1` | Erro em relação ao valor exato: R(x_k) − λ₁ |
| `||grad||` | Norma do gradiente na iteração k (critério de parada) |
| `x_k` | Vetor de deslocamentos na iteração k |

Em seguida imprime a frequência natural do sistema `omega1` e o vetor de deslocamento das massas `x*` final,.