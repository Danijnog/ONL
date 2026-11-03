Deseja-se minimizar o quociente de Rayleigh R(x):
x = arg_min x^T * K * x / x^T * M * X

Algumas propriedades:
- Diferenciabilidade: diferenciável em todos os pontos do seu domínio, exceto na origem (\(x = 0\)). Para qualquer vetor não-nulo x que deseja-se otimizar, tanto o numerador quanto o denominador são funções polinomiais quadráticas.
- Convexidade: A superfície do quociente de Rayleigh não é convexa globalmente, apresentando múltiplos pontos críticos (máximos, mínimos e pontos de sela).
- Modalidade: Apesar de apresentar múltiplos pontos críticos, é considerada unimodal, pois seus pontos de máximo e mínimo globais estão associados aos seus autovalores: o quociente de Rayleigh atinge seu valor mínimo global no autovetor associado ao menor autovalor, e seu valor máximo global no autovetor associado ao maior autovalor.
Todos os outros autovetores intermediários (com autovalores entre o mínimo e o máximo) comportam-se estritamente como pontos de sela.
- Continuidade: Em x = 0, a função é indefinida. Em  ℝ³ \ {0} a função é contínua.

Método Escolhido:
Método dos gradientes conjugados. O problema possui uma equivalência estrutural com o apresentado no método dos gradientes conjugados, se tratando de um sistema linear. Envolve o cálculo de autovalores do sistema também, e o método é adequado para este fim. Outra possibilidade considerada foi os Métodos de Newton / Quase-Newton, mas envolveria calcular e armazenar a Hessiana $H \in \mathbb{R}^{3\times 3}$. Embora eficientes, adicionam custo computacional desnecessário em comparação às direções conjugadas, enquanto somente o método do gradiente pode possuir uma convergência lenta para o problema analisado.