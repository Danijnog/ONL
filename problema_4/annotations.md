Deseja-se encontrar a posição de equilíbrio do sistema de dois carrinhos minimizando a energia potencial:
U(x1, x2) = 1/2 k2 x1^2 + 1/2 k3 (x2 - x1)^2 + 1/2 k1 x2^2 - P x2
com k1 = 1000 N/m, k2 = 1500 N/m, k3 = 2000 N/m e P = 100 N.

Reescrevendo, U(x) = 1/2 x^T H x - b^T x, com
H = [[k2 + k3, -k3], [-k3, k1 + k3]] = [[3500, -2000], [-2000, 3000]]  e  b = [0, P]^T.

Algumas propriedades:
- Diferenciabilidade: diferenciável em todo ℝ² (polinômio de grau 2). Gradiente: ∇U = H x - b.
- Convexidade: estritamente convexa. A Hessiana H é constante e definida positiva (autovalores 1234,4 e 5265,6, det = 6,5e6 > 0).
- Modalidade: unimodal. Existe um único ponto estacionário, que é o mínimo global.
- Continuidade: contínua em todo ℝ².

Método Escolhido:
Método de Newton. Como U é quadrática, o modelo de segunda ordem usado pelo método é exato: com a Hessiana constante, o passo de Newton x - H⁻¹ ∇U(x) cai diretamente no mínimo em UMA iteração, a partir de qualquer ponto inicial. O custo de resolver o sistema 2x2 é desprezível, então a desvantagem usual do método (calcular e fatorar a Hessiana) não existe aqui.

Outras possibilidades consideradas:
- Gradientes conjugados: também é exato para quadráticas, mas leva n = 2 iterações (confirmado numericamente).
- Gradiente com busca linear exata: converge, mas bem mais devagar (48 iterações para ||grad|| < 1e-8), pois o condicionamento de H (≈ 4,27) faz as trajetórias zigue-zaguearem.
- BFGS: 3 iterações; não precisaria da Hessiana, mas aqui ela está disponível e é trivial.

Conferência física: no equilíbrio, as forças resultantes em cada carrinho são nulas (k2 x1 - k3 (x2 - x1) = 0 no carrinho A e k1 x2 + k3 (x2 - x1) = P no carrinho B), o que é exatamente ∇U = 0.
