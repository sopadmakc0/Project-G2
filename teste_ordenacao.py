import random
import unittest
from metodos import insercao, intercalacao, rapida, hibrida, contagem, base
from adaptativo import escolher, ordenar


class TestOrdenacao(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.metodos = [
            insercao,
            intercalacao,
            rapida,
            hibrida,
            contagem,
            base,
            ordenar,
        ]

    def _verificar_todos(self, entrada: list[int]):
        esperado = sorted(entrada)
        for metodo in self.metodos:
            with self.subTest(metodo=metodo.__name__):
                copia = list(entrada)
                resultado = metodo(copia)
                self.assertEqual(resultado, esperado)
                self.assertEqual(copia, entrada, "A lista original não deve ser modificada.")

    def test_lista_vazia(self):
        self._verificar_todos([])

    def test_um_elemento(self):
        self._verificar_todos([42])

    def test_todos_iguais(self):
        self._verificar_todos([7] * 500)

    def test_ja_ordenada(self):
        self._verificar_todos(list(range(500)))

    def test_invertida(self):
        self._verificar_todos(list(range(500, 0, -1)))

    def test_valores_negativos(self):
        dados = [random.randint(-5000, 5000) for _ in range(500)]
        self._verificar_todos(dados)


if __name__ == "__main__":
    unittest.main(verbosity=2)