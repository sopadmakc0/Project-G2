from typing import Callable
from metodos import insercao, intercalacao, rapida, hibrida, contagem, base


def escolher(v: list[int]) -> Callable[[list[int]], list[int]]:
    """
    Analisa a lista v com custo mínimo e devolve a função de ordenação mais adequada.
    """
    n = len(v)

   
    if n <= 32:
        return insercao

   
    limite_quebras = max(1, n // 100)
    quebras = 0
    for i in range(1, n):
        if v[i] < v[i - 1]:
            quebras += 1
            if quebras > limite_quebras:
                break
    else:
        
        return insercao

   
    faixa = max(v) - min(v) + 1
    if faixa <= 2 * n:
        return contagem

    
    if faixa <= (1 << 30):
        return base

    return hibrida


def ordenar(v: list[int]) -> list[int]:
    
    metodo = escolher(v)
    return metodo(v)