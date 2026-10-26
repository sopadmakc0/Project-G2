# Relatório Técnico: Ordenação Adaptativa (`escolher` e `ordenar`)

## 1. Tabela Comparativa: Quatro Cenários vs. Seis Métodos Fixos e `ordenar(v)`

As medições abaixo foram obtidas com `N = 10.000` elementos para os cenários de grande porte e `n = 16` para a lista minúscula (`random.seed(42)`). Os tempos estão expressos em **milissegundos (ms)**.

| Método | Lista Minúscula (`n=16`) | Quase Ordenado (`n=10.000`) | Faixa Estreita (`n=10.000, k=101`) | Aleatório Chaves Grandes (`n=10.000, k=5M`) | Tempo Acumulado (Soma dos 4) | Média Geométrica | Slowdown Médio vs. Ótimo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Inserção** | **0,0169 ms** | **2,7420 ms** | 5.872,4613 ms | 5.666,4009 ms | 11.541,6211 ms | 35,2387 ms | 950,73x |
| **Intercalação** | 0,0476 ms | 41,4920 ms | 57,7955 ms | 64,1491 ms | 163,4842 ms | 9,2505 ms | 14,04x |
| **Rápida (Pivô Aleatório)** | 0,0498 ms | 43,7587 ms | 45,8750 ms | 50,9471 ms | 140,6306 ms | 8,4479 ms | 12,31x |
| **Híbrida (Quick+Ins)** | 0,0243 ms | 18,8072 ms | 21,7908 ms | 31,8946 ms | 72,5169 ms | 4,2216 ms | 5,87x |
| **Contagem** | 0,0946 ms | 5,4757 ms | **1,8082 ms** | 483,5959 ms | 490,9744 ms | 4,6133 ms | 13,95x |
| **Base (Radix LSD)** | 0,1193 ms | 6,8028 ms | 4,6277 ms | **10,2422 ms** | 21,7920 ms | 2,4904 ms | 3,27x |
| **`ordenar(v)` [Adaptativo]** | **0,0161 ms** | **4,2652 ms** | **2,2568 ms** | **10,9120 ms** | **17,4501 ms** | **1,1404 ms** | **1,21x** |

*Nota: Os valores de `ordenar(v)` já incluem o tempo gasto dentro de `escolher(v)`.*

---

## 2. Qual método venceu cada cenário e por quê?

1. **Lista Minúscula (`n = 16`) → Vencedor: Inserção (`0,0169 ms`)**
   - **Por quê:** Embora seja assintoticamente $O(n^2)$, para $n = 16$ o número máximo de comparações é 120. A Inserção opera *in-place* com um único laço sequencial, sem chamadas recursivas (que penalizam `Intercalação` e `Rápida`) e sem alocações de vetores de frequência ou *buckets* (que tornam `Contagem` e `Base` até **7x mais lentas** em listas minúsculas).

2. **Quase Ordenado (`n = 10.000`, 20 trocas locais) → Vencedor: Inserção (`2,7420 ms`)**
   - **Por quê:** A complexidade exata do Insertion Sort é $O(n + d)$, onde $d$ é o número de inversões na lista. Quando $d$ é pequeno, o laço interno `while` falha na primeira comparação em quase todas as iterações, reduzindo o algoritmo a uma varredura linear com constante mínima. Métodos como `Intercalação` (`41,49 ms`) e `Rápida` (`43,76 ms`) são cegos à ordenação prévia e continuam executando todas as divisões $\Theta(n \log n)$.

3. **Faixa Estreita (`n = 10.000, k = 101`) → Vencedor: Contagem (`1,8082 ms`)**
   - **Por quê:** Quando o universo de chaves $k = \max(v) - \min(v) + 1$ é muito menor que $n$ ($k = 101 \ll 10.000$), o Counting Sort aloca um vetor minúsculo de 101 posições, contabiliza as ocorrências em uma única passada e reconstrói a lista imediatamente em $\Theta(n + k)$. Ele bate até o Radix Sort (`4,63 ms`), pois não precisa distribuir elementos em listas de *buckets*, e supera algoritmos baseados em comparação (`Híbrida` levou `21,79 ms`) ao contornar o limite inferior de $\Omega(n \log n)$.

4. **Aleatório com Chaves Grandes (`n = 10.000, k = 5.000.000`) → Vencedor: Base / Radix Sort (`10,2422 ms`)**
   - **Por quê:** Com $k = 5 \times 10^6$ ($k = 500n$), o `Contagem` degrada severamente (`483,60 ms`), pois gasta quase todo o tempo alocando e percorrendo 5 milhões de posições majoritariamente vazias. Já o `Base` (LSD Radix Sort em base 256) processa 8 bits por vez: como $5.000.000 < 2^{24}$, ele resolve a ordenação em apenas **3 passes lineares** de tamanho 256, superando a `Híbrida` (`31,89 ms`), a `Rápida` (`50,95 ms`) e a `Intercalação` (`64,15 ms`).

---

## 3. Regras do `escolher(v)` e de onde vieram

A função `escolher(v)` aplica uma árvore de decisão sequencial calibrada por limites teóricos e empíricos:

1. **Regra 1 (`n <= 32` $\rightarrow$ `insercao`):**
   - **Origem:** Em análises empíricas de algoritmos híbridos (Quick-Insertion), o ponto de cruzamento (*crossover point*) entre a sobrecarga de particionamento recursivo e a varredura quadrática ocorre na faixa de $16 \le n \le 32$. A verificação `len(v) <= 32` custa $\Theta(1)$.
2. **Regra 2 (`quebras <= n // 100` com *early-exit* $\rightarrow$ `insercao`):**
   - **Origem:** Uma lista quase ordenada apresenta pouquíssimas quedas entre vizinhos adjacentes ($v[i] < v[i-1]$). Estabelecemos o limiar de até **1% de quebras adjacentes**. Para não gastar tempo varrendo listas aleatórias inteiras, implementamos **parada antecipada (*early-exit*)**: assim que o contador ultrapassa $0,01n$ (o que ocorre por volta do índice 200 em listas aleatórias de 10.000 itens), o laço é abortado imediatamente.
3. **Regra 3 (`faixa <= 2 * n` $\rightarrow$ `contagem`):**
   - **Origem:** O Counting Sort tem custo $\Theta(n + k)$. Enquanto $k \le 2n$, o vetor de contagem tem no máximo o dobro do tamanho da entrada e densidade média $\ge 0,5$ elemento por posição, mantendo o custo estritamente abaixo dos 2 a 4 passes exigidos pelo Radix Sort.
4. **Regra 4 (`faixa <= 2**30` $\rightarrow$ `base`, caso contrário $\rightarrow$ `hibrida`):**
   - **Origem:** Em base 256 (1 byte por passe), uma faixa de até $2^{30}$ exige no máximo 4 passes pelos *buckets*, onde o Radix Sort vence com folga. Se as chaves tiverem amplitude astronômica (ex.: inteiros de 64 bits ou $k > 2^{30}$), o número de passes do Radix aumenta para 8 ou mais, momento em que a `hibrida` (Quick-Insertion) passa a ser mais vantajosa.

---

## 4. Quanto custa rodar o `escolher(v)`? Ele compensa?

### Custo medido de `escolher(v)` isoladamente:
- **Lista Minúscula (`n = 16`):** `0,0003 ms` ($0,3\ \mu\text{s}$) — apenas um `len(v) <= 32` em $\Theta(1)$.
- **Faixa Estreita (`n = 10.000`):** `0,4381 ms` — aborta a checagem de quebras logo nos primeiros ~200 elementos (*early-exit*) e calcula `max(v) - min(v)` via funções nativas.
- **Chaves Grandes (`n = 10.000`):** `0,4461 ms` — mesmo comportamento de *early-exit* + `min`/`max`.
- **Quase Ordenado (`n = 10.000`):** `1,3463 ms` — único caso que percorre os 10.000 elementos no laço de verificação de quebras, mas economiza mais de **37 ms** frente ao Merge/Quicksort.

### Veredito: Compensa?
**Sim, compensa com folga.**
- Na soma dos 4 cenários, `ordenar(v)` (já somado o custo de `escolher(v)`) leva **17,45 ms**, vencendo **todos os 6 métodos fixos**, inclusive o segundo colocado geral (`Base`, com **21,79 ms**) e a `Híbrida` (**72,52 ms**).
- Na **média geométrica** dos 4 cenários, `ordenar(v)` atinge **1,14 ms**, menos da metade do melhor método fixo (`Base` com **2,49 ms**).
- O **slowdown médio** de `ordenar(v)` em relação ao melhor algoritmo possível de cada cenário é de apenas **1,21x**, contra **3,27x** do `Base`, **5,87x** da `Híbrida` e **950,73x** da `Inserção`.

---

## 5. Um cenário em que o `escolher(v)` erra a decisão

### O Cenário Armadilha: Vetor Ordenado Rotacionado
Considere um vetor de $n = 10.000$ elementos formado por duas metades ordenadas concatenadas em ordem trocada (uma rotação de lista ordenada com chaves espaçadas):

$$v = [5.000.000,\ 5.001.000,\ \dots,\ 9.999.000,\ 0,\ 1.000,\ 2.000,\ \dots,\ 4.999.000]$$

### Por que o `escolher(v)` é enganado?
Para ser barato ($O(n)$), `escolher(v)` mede o grau de desordem contando apenas **quebras adjacentes** ($v[i] < v[i-1]$). Nesse vetor rotacionado, existe **apenas 1 quebra adjacente** em 10.000 elementos (exatamente na fronteira entre `9.999.000` e `0`).
- Como $1 \le 100$ (limite de 1%), `escolher(v)` conclui erroneamente que a lista está "quase ordenada" e devolve **`insercao`**.
- Porém, embora haja apenas 1 quebra *local*, cada um dos 5.000 elementos da segunda metade é menor que todos os 5.000 elementos da primeira metade, totalizando $5.000 \times 5.000 = 25.000.000$ de **inversões globais**!

### Resultado Empírico do Erro:
| Método | Tempo no Vetor Rotacionado (`n = 10.000`) |
| :--- | :---: |
| **`ordenar(v)` (enganado → escolheu `insercao`)** | **5.322,85 ms** |
| **`Base` (Radix Sort — escolha ótima real)** | **14,98 ms** |
| **`Híbrida` (Quick-Insertion)** | **20,98 ms** |

Para evitar esse erro sem falsos positivos, `escolher(v)` precisaria estimar inversões globais (ou a distância de deslocamento de cada elemento até sua posição final), o que no caso geral exige $\Theta(n \log n)$ — exatamente o custo de ordenar a lista inteira, destruindo a premissa de que `escolher(v)` deve ser barato.
