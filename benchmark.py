import random
import time
from metodos import insercao, intercalacao, rapida, hibrida, contagem, base
from adaptativo import escolher, ordenar


def medir_tempo_ms(func, dados, repeticoes):
    t0 = time.perf_counter()
    for _ in range(repeticoes):
        func(dados)
    t1 = time.perf_counter()
    return ((t1 - t0) / repeticoes) * 1000.0


def executar_benchmarks():
    random.seed(42)
    N = 10_000

    
    c_minuscula = [random.randint(0, 1000) for _ in range(16)]

    c_quase_ord = list(range(N))
    for _ in range(20):  # 20 trocas locais (0,2% de perturbação)
        idx = random.randint(0, N - 2)
        c_quase_ord[idx], c_quase_ord[idx + 1] = c_quase_ord[idx + 1], c_quase_ord[idx]

    c_faixa_estreita = [random.randint(0, 100) for _ in range(N)]
    c_chaves_grandes = [random.randint(0, 5_000_000) for _ in range(N)]

    cenarios = [
        ("Lista minúscula (n=16)", c_minuscula, 1000),
        ("Quase ordenado (n=10.000)", c_quase_ord, 20),
        ("Faixa estreita (n=10.000, k=101)", c_faixa_estreita, 20),
        ("Chaves grandes (n=10.000, k=5M)", c_chaves_grandes, 10),
    ]

    metodos = [
        ("Inserção", insercao),
        ("Intercalação", intercalacao),
        ("Rápida (Pivô Aleatório)", rapida),
        ("Híbrida (Quick+Ins)", hibrida),
        ("Contagem", contagem),
        ("Base (Radix)", base),
        ("ordenar(v) [Adaptativo]", ordenar),
    ]

    print("=" * 80)
    print("RESULTADOS DOS 4 CENÁRIOS (Tempo médio por execução em ms)")
    print("=" * 80)

    for nome_cen, dados, reps in cenarios:
        escolha = escolher(dados).__name__
        custo_escolher = medir_tempo_ms(escolher, dados, max(reps * 20, 1000))
        print(f"\n>>> {nome_cen} | escolher(v) -> {escolha} (custo: {custo_escolher:.4f} ms)")
        for nome_met, fn in metodos:
            r = 2 if (fn is insercao and len(dados) == N and "Quase" not in nome_cen) else reps
            if fn is contagem and "Chaves grandes" in nome_cen:
                r = 2
            tempo = medir_tempo_ms(fn, dados, r)
            print(f"  - {nome_met:25s}: {tempo:9.4f} ms")

   
    print("\n" + "=" * 80)
    print("CENÁRIO ARMADILHA: Vetor Ordenado Rotacionado (n=10.000)")
    print("=" * 80)
    armadilha = [x * 1000 for x in (list(range(5000, 10000)) + list(range(0, 5000)))]
    metodo_enganado = escolher(armadilha).__name__
    t_ordenar = medir_tempo_ms(ordenar, armadilha, 1)
    t_base = medir_tempo_ms(base, armadilha, 5)
    t_hibrida = medir_tempo_ms(hibrida, armadilha, 5)
    print(f"Método escolhido por escolher(v): {metodo_enganado}")
    print(f"Tempo de ordenar(v) [enganado] : {t_ordenar:.2f} ms")
    print(f"Tempo de Base (Radix)          : {t_base:.2f} ms")
    print(f"Tempo de Híbrida (Quick+Ins)   : {t_hibrida:.2f} ms")


if __name__ == "__main__":
    executar_benchmarks()