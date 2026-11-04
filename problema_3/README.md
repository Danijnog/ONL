# Preços ótimos pelo critério minimax

Escolha dos preços `p1` e `p2` de dois produtos que minimizam o pior desvio da receita em relação a uma meta, considerando 4 cenários de mercado.

### Problema

```
min_{p1,p2}  max_i | R_i(p1, p2) - R_alvo |,      R_i(p1, p2) = a1_i / p1 + a2_i / p2,      R_alvo = 10000
```

| Cenário | Descrição | a1,i | a2,i |
|---|---|---|---|
| 1 | Mercado Normal | 100000 | 80000 |
| 2 | Recessão Econômica | 70000 | 56000 |
| 3 | Alta Demanda | 130000 | 104000 |
| 4 | Pressão Competitiva | 90000 | 90000 |

### Características da função objetivo

- Diferenciabilidade: não é diferenciável em todo o domínio. O máximo e o valor absoluto criam quinas, e o ótimo está justamente em uma região onde vários cenários empatam como pior caso.
- Convexidade: não é convexa em (p1, p2). Com `u = 1/p1` e `v = 1/p2` cada `R_i` fica linear e o problema vira um PL (usado só como referência para conferir o resultado).
- Modalidade: o valor ótimo é único (`f* = 3000`), mas o minimizador não é único. Os cenários 1, 2 e 3 dependem de `p1` e `p2` só por `1/p1 + 0,8/p2`, então todo ponto da curva `1/p1 + 0,8/p2 = 0,1` (com `p1, p2 > 0`) é ótimo.
- Continuidade: contínua para `p1, p2 > 0`.

### Método escolhido para resolver o problema

Nelder-Mead (simplex). Como a função não é diferenciável nos pontos de interesse, métodos baseados em gradiente (gradiente, CG, Newton, BFGS) usam uma informação que não existe no ótimo. Com apenas 2 variáveis e avaliação barata da função, um método de busca direta (sem derivadas) é a escolha natural. Para manter `p > 0`, `f` devolve um valor muito alto quando algum preço é não positivo.

Para comparação foram rodados também o método de Powell (busca direta) e o BFGS do scipy com gradiente numérico.

### Como executar

Requisitos: Python 3, `numpy`, `scipy`, `matplotlib`.

```bash
python3 main.py
```

O script imprime a comparação entre os métodos, as receitas por cenário no ponto encontrado, os resultados a partir de vários pontos iniciais e salva `resultado.png`.

### Resultado obtido

Partindo de `p0 = [10, 10]` (`f(p0) = 13400`):

| Método | p1 | p2 | f(p*) | Iterações | Avaliações de f | Convergiu |
|---|---|---|---|---|---|---|
| Nelder-Mead | 26,47179 | 12,85679 | 3000,00000000 | 111 | 234 | Sim |
| Powell | 50,31190 | 9,98453 | 3000,00000000 | 2 | 132 | Sim |
| BFGS (grad. numérico) | 17,02072 | 19,39484 | 3000,00000145 | 7 | 255 | Não (perda de precisão) |

Receitas por cenário no ponto do Nelder-Mead:

| Cenário | R_i(p*) | \|R_i − R_alvo\| |
|---|---|---|
| Mercado Normal | 10000,00 | 0,00 |
| Recessão Econômica | 7000,00 | 3000,00 |
| Alta Demanda | 13000,00 | 3000,00 |
| Pressão Competitiva | 10400,04 | 400,04 |

Os cenários 2 e 3 empatam como pior caso (desvio de 3000), característica típica de soluções minimax. O valor de referência obtido pelo PL em `(1/p1, 1/p2)` também é 3000.

Como o minimizador não é único, pontos iniciais diferentes levam a preços diferentes sobre a curva `1/p1 + 0,8/p2 = 0,1`, todos com `f = 3000`:

| p0 | p1* | p2* | f(p*) |
|---|---|---|---|
| (10, 10) | 26,47 | 12,86 | 3000 |
| (20, 15) | 20,01 | 15,99 | 3000 |
| (15, 30) | 13,40 | 31,50 | 3000 |
| (40, 12) | 41,33 | 10,55 | 3000 |
| (12, 60) | 11,51 | 60,88 | 3000 |

Do ponto de vista de negócio, qualquer um desses pares garante a mesma robustez; a escolha entre eles pode usar outros critérios (por exemplo, a receita no cenário normal ou a competitividade dos preços).

### Como ler a saída

| Coluna | Significado |
|---|---|
| `p1`, `p2` | Preços encontrados |
| `f(p*)` | Pior desvio absoluto de receita no ponto encontrado |
| `iter` | Número de iterações do método |
| `aval.` | Número de avaliações da função objetivo |
| `1/p1 + 0.8/p2` | Deve valer 0,1 em todo ponto ótimo |
