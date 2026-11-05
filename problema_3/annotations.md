Deseja-se minimizar o pior desvio da receita em relação à meta entre os cenários:
min_{p1,p2} max_i |R_i(p1,p2) - R_alvo|, com R_i = a1_i/p1 + a2_i/p2 e R_alvo = 10000

Algumas propriedades:
- Diferenciabilidade: NÃO é diferenciável em todo o domínio. O máximo de funções e o valor absoluto introduzem "quinas" (pontos onde dois ou mais desvios empatam, ou onde R_i = R_alvo). Fora dessas quinas a função é suave. O gradiente, portanto, não existe exatamente nos pontos onde o ótimo está (no ótimo vários cenários empatam como pior caso).
- Convexidade: Não é convexa em (p1, p2). Cada R_i é convexa e decrescente em p (soma de termos 1/p), mas o desvio absoluto |R_i - R_alvo| e o máximo quebram a convexidade. Com a troca de variáveis u = 1/p1 e v = 1/p2 cada R_i passa a ser linear em (u, v), e o problema vira convexo (e até um PL). Isso foi usado só para conferir o resultado.
- Modalidade: o valor ótimo é único (f* = 3000), mas o minimizador NÃO é único: os cenários 1, 2 e 3 têm a2/a1 = 0,8 e dependem de p1 e p2 só pela combinação s = 1/p1 + 0,8/p2. O pior desvio entre eles é mínimo em s = 0,1 (cenários 2 e 3 empatam com desvio de 3000). O cenário 4 fica dentro dessa folga. Assim, todo ponto da curva 1/p1 + 0,8/p2 = 0,1 (com p1, p2 > 0) é ótimo.
- Continuidade: contínua em p1, p2 > 0. Em p = 0 (ou p < 0) a receita deixa de fazer sentido (domínio é p1, p2 > 0).

Método Escolhido:
Nelder-Mead (simplex). A função é não-diferenciável nos pontos de interesse, então métodos que dependem de gradiente (gradiente, gradientes conjugados, Newton, BFGS) usam uma informação que não existe no ótimo e tendem a travar nas quinas ou terminar por perda de precisão. O problema tem só 2 variáveis, a avaliação da função é muito barata e não é necessário usar derivadas, o que torna o método de busca direta (sem derivadas) bastante adequado. Para garantir p > 0, f retorna um valor muito alto quando algum preço é não positivo.

Outras possibilidades consideradas:
- Powell (busca direta com buscas lineares): também funciona (encontrou f = 3000 com poucas iterações), mas faz mais avaliações da função.
- BFGS com gradiente numérico: chega perto de 3000, mas o scipy termina com "success = False" (perda de precisão na busca linear) por causa da quina.
- Suavização (por exemplo, log-sum-exp) + BFGS ou reformulação epigráfica (min t s.t. |R_i - R_alvo| <= t) com SLSQP: seriam alternativas válidas, mas exigem ou aproximar o problema ou introduzir restrições, o que foge de "otimização sem restrições".

Resultado: f* = 3000 (pior desvio de R$ 3000). Como o minimizador não é único, o Nelder-Mead termina em pontos diferentes da curva 1/p1 + 0,8/p2 = 0,1 dependendo do ponto inicial, sempre com o mesmo valor de f.
