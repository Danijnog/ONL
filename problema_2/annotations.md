Recuperações de imagens através de métodos de otimização não-linear:
A minimização da função objetivo envolve um termo quadrático (termo de fidelidade) e um termo de regularização.

f(x) = ∥Ax − b∥^2 +  + λ · TV(x)

Algumas propriedades:
- Diferenciabilidade: É difereciável em todo seu domínio. O termo de fidelidade (quadrático) não possui problemas para calcular sua derivada. Já no termo de regularização, temos uma função irracional (uma raiz quadrada de termos elevados ao quadrado e um ε, mostrado na descrição do exercício.) Como no termo de regularização ε > 0, ele também é diferenciável.
- Convexidade: É convexa. Tanto os termos de fidelidade quanto de regularização são convexos
- Modalidade: Unimodal. Portanto, não há risco da função ficar presa a mínimos ou máximos locais, que não representam a otimização global da função.
- Continuidade: A função é contínua. F é composição e soma de funções contínuas (polinômios e raiz de função estritamente positiva), definida em todo ℝⁿ.

Método Escolhido:
Método BFGS. Como nosso problema envolve funções suaves e contínuas, é possível calcular os gradientes da função sem muitos problemas. Por se tratar de um método Quasi-Newton, o algoritmo aproxima iterativamente a Hessiana (matriz nxn) ao invés de calcula-la diretamente, apresentando uma vantagem nesse sentido.
Memória: O(n²).
Custo por iteração: O(n²).
Convergência: superlinear, em geral com poucas iterações.

A fim de economizar memória para grandes iterações, no código foi utilizado uma variação do método BFGS, conhecido como L-BFGS-B.
A sigla possui duas partes a mais para o algoritmo de BFGS:

L (Limited memory): Em vez de guardar Hₖ inteira, guarda apenas os últimos m pares (sₖ, yₖ), com m tipicamente entre 5 e 20.
Memória: O(m·n).
Custo por iteração: O(m·n).

B (boundary constraints): suporta restrições do problema, mas não é aplicável ao nosso caso no momento.

O foco é economizar memória ao usar o método L-BFGS-B ao invés do BFGS.