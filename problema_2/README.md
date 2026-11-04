# Otimização de imagens borradas para recuperação de nitidez

Minimização de uma dada função objetivo f(x) representando uma imagem borrada e ruidosa, formulando um problema de otimização não linear irrestrito.

### Problema
Seja `x` a imagem nítida achatada (n = N X M) pixels, `b` a imagem borrada e ruidosa e `A` a matriz de convolução que modela o borrão.

Temos a recuperação da imagem minimizando:

f(x) = ‖Ax − b‖₂² + λ · TV(x)
A função objetivo é composta por dois termos:

Termo de fidelidade, ‖Ax − b‖₂² = Σᵢ ((Ax)ᵢ − bᵢ)²: mede o quanto a imagem candidata, depois de borrada, difere da imagem medida. É um termo quadrático.

Termo de regularização, λ · TV(x), com TV dado no enunciado do trabalho.

### Propriedades da função objetivo
Diferenciabilidade: é diferenciável em todo o seu domínio. O termo de fidelidade (quadrático) não apresenta problemas para o cálculo da derivada. O termo de regularização é uma função irracional (raiz quadrada de termos elevados ao quadrado mais um ε). Como ε > 0, o argumento da raiz nunca se anula e esse termo também é diferenciável.
Convexidade: é convexa. Tanto o termo de fidelidade quanto o de regularização são convexos.
Modalidade: unimodal. Não há risco de o algoritmo ficar preso em mínimos locais que não representam o mínimo global da função.
Continuidade: é contínua. f é composição e soma de funções contínuas (polinômios e raiz de função estritamente positiva), definida em todo ℝⁿ.

### Método escolhido
BFGS, na variação L-BFGS-B.

Como o problema envolve funções suaves e contínuas, é possível calcular o gradiente sem grandes dificuldades. O BFGS é um método quase-Newton: em vez de calcular a Hessiana (matriz n × n) diretamente, ele aproxima iterativamente a sua inversa, o que representa uma vantagem em relação ao método de Newton.

BFGS

- Memória: O(n²)
- Custo por iteração: O(n²)
- Convergência: superlinear, em geral com poucas iterações

Para economizar memória em imagens grandes, o código usa a variação L-BFGS-B, cuja sigla acrescenta duas partes ao BFGS:

- L (Limited memory): em vez de guardar a aproximação Hₖ inteira, guarda apenas os últimos m pares (sₖ, yₖ), com m tipicamente entre 5 e 20.
Memória: O(m·n)
- Custo por iteração: O(m·n)
B (Bound constraints): suporta restrições de caixa nas variáveis. Não é aplicável ao nosso caso no momento, pois o problema é irrestrito.

O foco da escolha do L-BFGS-B em vez do BFGS é economizar memória.

### Resultados
Foram plotadas as imagens borradas e reconstruídas considerando 2, 5, 10 e 100 iterações.
Nota-se uma melhora contínua das imagens otimizadas, reduzindo seu ruído.