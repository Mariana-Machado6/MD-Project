# Knowledge Engine - Músicas

Projeto de Lógica e Matemática Discreta onde construimos um mecanismo de busca utilizando Lógica de Primeira Ordem.

## Dados e preparação

Fonte: [Spotify Tracks Dataset — Maharshi Pandya](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset).

Usei uma única tabela, `dataset.csv`, com oito campos:

`track_id`: Identificador da faixa\
`track_name`: Nome\
`artists`: Artistas\
`track_genre`: Gênero\
`popularity`: Popularidade\
`duration_ms`: Duração em milissegundos\
`energy`: Energia\
`danceability`: Dançabilidade

O script seleciona esses campos, remove um registro com dados ausentes e 450 repetições do par música–gênero. A base passa de 114.000 para 113.549 registros, mantendo 114 gêneros.

```prolog
musica(Id, Nome, Artistas, Genero, Popularidade, DuracaoMs, Energia, Dancabilidade).
```

## Arquivos

`explorar.py`: prepara os dados e gera os três arquivos Prolog.\
`dados/dataset.csv`: tabela original.\
`prolog/musicas.pl`: fatos gerados.\
`prolog/regras.pl`: regras que calculam as respostas.\
`prolog/consultas.pl`: exemplos de consultas em comentários.\
`requirements.txt`: dependência Python (`pandas`).

## Como executar

Requisitos: Python 3, pandas e SWI-Prolog. As consultas foram executadas no SWI-Prolog 10.0.2.

No terminal, dentro da raiz do projeto:

```bash
python3 -m pip install -r requirements.txt
python3 explorar.py
swipl -s prolog/regras.pl
```

Se usar o aplicativo SWI-Prolog, carregue as regras no console, substituindo o caminho:

```prolog
consult('/caminho/MD-Project/prolog/regras.pl').
```

Para alterar as regras permanentemente, edite os textos em `explorar.py` e execute novamente. Em uma sessão Prolog já aberta, use `make.` para recarregar.

## Perguntas e consultas

Digite as consultas no console Prolog, incluindo o ponto final.

**1. Quais gêneros têm maior popularidade média?**

Agrupa as músicas por gênero, calcula médias e ordena os resultados.

```prolog
mostrar_ranking.
```

Resultado observado: `pop-film` lidera com média 59,28, seguido de `k-pop`, com 56,96.

**2. Quais músicas têm popularidade acima da média do próprio gênero?**

Combina a regra de média com a comparação da popularidade de cada música. Exemplo para `acoustic`:

```prolog
mostrar_acima_da_media('acoustic').
```

Consulta geral:

```prolog
acima_da_media(Id, Nome, Artistas, Genero, Popularidade, Media).
```

Conferência: `Comedy`, de Gen Hoshino, tem popularidade 73, acima da média 42,483 de `acoustic`.

**3. Quais gêneros têm maior proporção de músicas com energia e dançabilidade >= 0,7?**

Combina duas condições, conta os registros e ordena os percentuais. O limite de 0,7 foi definido para esta análise.

```prolog
mostrar_ranking_energia.
```

Conferência:

```prolog
proporcao_genero('acoustic', Quantidade, Total, Percentual).
```

Resultado: 15 de 1.000 músicas, ou 1,5%. No ranking, `reggaeton` lidera com 48,90%. Cada percentual usa o total do próprio gênero como denominador.
