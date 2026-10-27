# Ordenação Adaptativa (`escolher` e `ordenar`)

Projeto prático de Análise e Projeto de Algoritmos / Estruturas de Dados que reúne seis métodos de ordenação clássicos (`insercao`, `intercalacao`, `rapida`, `hibrida`, `contagem` e `base`) e implementa um seletor adaptativo (`escolher(v)` e `ordenar(v)`) capaz de superar qualquer escolha fixa ao longo de diferentes perfis de entrada.

## Pré-requisitos

- **Python 3.10+** (não requer instalação de bibliotecas externas; utiliza apenas a biblioteca padrão).

## Estrutura do Projeto

- `src/metodos.py`: Implementação dos 6 algoritmos de ordenação do semestre.
- `src/adaptativo.py`: Implementação de `escolher(v)` e `ordenar(v)`.
- `tests/test_ordenacao.py`: Testes automatizados para casos de borda (lista vazia, 1 elemento, todos iguais, já ordenada, invertida e valores negativos).
- `benchmark.py`: Script que reproduz as medições dos 4 cenários, mede o overhead de `escolher(v)` e demonstra o cenário armadilha onde o seletor erra.
- `RELATORIO.md`: Relatório técnico completo com tabelas comparativas e análise dos resultados.

## Como Executar os Testes

Na raiz do repositório, execute:

```bash
python3 -m unittest discover -s tests -v

- `Observação`: dependendo da versão instalada do seu python, no terminal pode ser usado py ou python ou python3, por favor verifique os Pré-requisitos se batem de acordo!
