import random
import sys

sys.setrecursionlimit(50000)


def insercao(v: list[int]) -> list[int]:
    
    arr = list(v)
    for i in range(1, len(arr)):
        chave = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > chave:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = chave
    return arr


def intercalacao(v: list[int]) -> list[int]:
    
    arr = list(v)
    if len(arr) <= 1:
        return arr

    def _merge_sort(a: list[int]) -> list[int]:
        if len(a) <= 1:
            return a
        meio = len(a) // 2
        esq = _merge_sort(a[:meio])
        dir = _merge_sort(a[meio:])
        res = []
        i = j = 0
        while i < len(esq) and j < len(dir):
            if esq[i] <= dir[j]:
                res.append(esq[i])
                i += 1
            else:
                res.append(dir[j])
                j += 1
        res.extend(esq[i:])
        res.extend(dir[j:])
        return res

    return _merge_sort(arr)


def rapida(v: list[int]) -> list[int]:
    
    arr = list(v)

    def _qs(a: list[int], low: int, high: int) -> None:
        while low < high:
            p_idx = random.randint(low, high)
            a[low], a[p_idx] = a[p_idx], a[low]
            pivo = a[low]

            # Particionamento de Hoare (evita degradação O(n^2) em elementos iguais)
            i = low - 1
            j = high + 1
            while True:
                i += 1
                while a[i] < pivo:
                    i += 1
                j -= 1
                while a[j] > pivo:
                    j -= 1
                if i >= j:
                    break
                a[i], a[j] = a[j], a[i]

            # Eliminação de recursão de cauda no lado maior
            if j - low < high - j:
                _qs(a, low, j)
                low = j + 1
            else:
                _qs(a, j + 1, high)
                high = j

    if len(arr) > 1:
        _qs(arr, 0, len(arr) - 1)
    return arr


def hibrida(v: list[int], limite: int = 24) -> list[int]:
    
    arr = list(v)

    def _qs_parcial(a: list[int], low: int, high: int) -> None:
        while high - low + 1 > limite:
            p_idx = random.randint(low, high)
            a[low], a[p_idx] = a[p_idx], a[low]
            pivo = a[low]

            i = low - 1
            j = high + 1
            while True:
                i += 1
                while a[i] < pivo:
                    i += 1
                j -= 1
                while a[j] > pivo:
                    j -= 1
                if i >= j:
                    break
                a[i], a[j] = a[j], a[i]

            if j - low < high - j:
                _qs_parcial(a, low, j)
                low = j + 1
            else:
                _qs_parcial(a, j + 1, high)
                high = j

    if len(arr) > 1:
        _qs_parcial(arr, 0, len(arr) - 1)
        for i in range(1, len(arr)):
            chave = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > chave:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = chave
    return arr


def contagem(v: list[int]) -> list[int]:
    
    if len(v) <= 1:
        return list(v)
    min_val = min(v)
    max_val = max(v)
    faixa = max_val - min_val + 1
    if faixa > 20_000_000:
        raise MemoryError(f"Faixa k={faixa} excede o limite seguro para Counting Sort.")

    cont = [0] * faixa
    for x in v:
        cont[x - min_val] += 1

    res = []
    for offset, freq in enumerate(cont):
        if freq > 0:
            res.extend([offset + min_val] * freq)
    return res


def base(v: list[int]) -> list[int]:
   
    if len(v) <= 1:
        return list(v)
    min_val = min(v)
    arr = [x - min_val for x in v]
    max_shifted = max(arr)

    shift = 0
    while (max_shifted >> shift) > 0:
        buckets = [[] for _ in range(256)]
        for x in arr:
            buckets[(x >> shift) & 0xFF].append(x)
        arr = [x for b in buckets for x in b]
        shift += 8

    return [x + min_val for x in arr]