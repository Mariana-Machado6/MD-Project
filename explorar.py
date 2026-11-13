from pathlib import Path
import pandas as pd

pasta = Path(__file__).resolve().parent
arquivo = pasta / "dados" / "dataset.csv"

campos = [
    "track_id",
    "track_name",
    "artists",
    "track_genre",
    "popularity",
    "duration_ms",
    "energy",
    "danceability",
]

df = pd.read_csv(arquivo, usecols=campos)
df = df[campos]

print("Registros originais:", len(df))

df = df.dropna(subset=campos)

df = df.drop_duplicates(subset=["track_id", "track_genre"])

print("Registros após a limpeza:", len(df))
print("Quantidade de gêneros:", df["track_genre"].nunique())
print(df.head())

# Pasta onde ficará a base Prolog.
pasta_prolog = pasta / "prolog"
pasta_prolog.mkdir(exist_ok=True)

arquivo_prolog = pasta_prolog / "musicas.pl"


def texto_prolog(valor):
    """Protege textos para usá-los como átomos Prolog entre aspas."""
    texto = str(valor)
    texto = texto.replace("\\", "\\\\")
    texto = texto.replace("'", "''")
    texto = texto.replace("\r", "\\r")
    texto = texto.replace("\n", "\\n")
    texto = texto.replace("\t", "\\t")
    return f"'{texto}'"


with arquivo_prolog.open("w", encoding="utf-8") as saida:
    saida.write(":- encoding(utf8).\n\n")
    saida.write(
        "% musica(Id, Nome, Artistas, Genero, "
        "Popularidade, DuracaoMs, Energia, Dancabilidade).\n\n"
    )

    for linha in df.itertuples(index=False):
        fato = (
            f"musica("
            f"{texto_prolog(linha.track_id)}, "
            f"{texto_prolog(linha.track_name)}, "
            f"{texto_prolog(linha.artists)}, "
            f"{texto_prolog(linha.track_genre)}, "
            f"{int(linha.popularity)}, "
            f"{int(linha.duration_ms)}, "
            f"{float(linha.energy)}, "
            f"{float(linha.danceability)}"
            f").\n"
        )
        saida.write(fato)

print("Base Prolog criada em:", arquivo_prolog)
print("Quantidade de fatos gerados:", len(df))

# Regras que serão gravadas em prolog/regras.pl.
regras = r"""
:- encoding(utf8).
:- use_module(library(lists)).
:- ensure_loaded('musicas.pl').

% Lista os gêneros sem repetições.
generos(Generos) :-
    findall(G, musica(_, _, _, G, _, _, _, _), Lista),
    sort(Lista, Generos).

% PERGUNTA 1: popularidade média por gênero.

media_popularidade(Genero, Media) :-
    generos(Generos),
    member(Genero, Generos),
    findall(
        P,
        musica(_, _, _, Genero, P, _, _, _),
        Popularidades
    ),
    sum_list(Popularidades, Soma),
    length(Popularidades, Quantidade),
    Quantidade > 0,
    Media is Soma / Quantidade.

ranking_generos(Ranking) :-
    findall(
        Media-Genero,
        media_popularidade(Genero, Media),
        Resultados
    ),
    sort(Resultados, Crescente),
    reverse(Crescente, Ranking).

mostrar_ranking :-
    ranking_generos(Ranking),
    forall(
        member(Media-Genero, Ranking),
        format('~w: ~2f~n', [Genero, Media])
    ).

% PERGUNTA 2: músicas acima da média do próprio gênero.

acima_da_media(Id, Nome, Artistas, Genero, Popularidade, Media) :-
    media_popularidade(Genero, Media),
    musica(Id, Nome, Artistas, Genero, Popularidade, _, _, _),
    Popularidade > Media.

mostrar_acima_da_media(Genero) :-
    forall(
        acima_da_media(
            _, Nome, Artistas, Genero, Popularidade, Media
        ),
        format(
            '~w | ~w | popularidade: ~d | media: ~2f~n',
            [Nome, Artistas, Popularidade, Media]
        )
    ).

% PERGUNTA 3: proporção com energia e dançabilidade >= 0.7.

energia_dancabilidade_alta(Id, Genero) :-
    musica(Id, _, _, Genero, _, _, Energia, Dancabilidade),
    Energia >= 0.7,
    Dancabilidade >= 0.7.

proporcao_genero(Genero, Quantidade, Total, Percentual) :-
    generos(Generos),
    member(Genero, Generos),
    findall(
        Id,
        musica(Id, _, _, Genero, _, _, _, _),
        Todas
    ),
    length(Todas, Total),
    Total > 0,
    findall(
        Id,
        energia_dancabilidade_alta(Id, Genero),
        Selecionadas
    ),
    length(Selecionadas, Quantidade),
    Percentual is 100 * Quantidade / Total.

ranking_energia_dancabilidade(Ranking) :-
    findall(
        Percentual-Genero,
        proporcao_genero(Genero, _, _, Percentual),
        Resultados
    ),
    sort(Resultados, Crescente),
    reverse(Crescente, Ranking).

mostrar_ranking_energia :-
    ranking_energia_dancabilidade(Ranking),
    forall(
        member(Percentual-Genero, Ranking),
        format('~w: ~2f%~n', [Genero, Percentual])
    ).
"""

# Exemplos de consultas: copiar para o console do Prolog.
consultas = r"""
% Carregue regras.pl antes de executar as consultas.

% 1. Quais gêneros têm maior popularidade média?
% mostrar_ranking.

% 2. Quais músicas superam a média do próprio gênero?
% Exemplo para acoustic:
% mostrar_acima_da_media('acoustic').

% Consulta geral:
% acima_da_media(Id, Nome, Artistas, Genero, Popularidade, Media).

% 3. Quais gêneros têm maior proporção de músicas com
% energia e dançabilidade iguais ou superiores a 0.7?
% mostrar_ranking_energia.

% Conferência para acoustic:
% proporcao_genero('acoustic', Quantidade, Total, Percentual).
"""

for nome, conteudo in [
    ("regras.pl", regras),
    ("consultas.pl", consultas),
]:
    destino = pasta_prolog / nome
    destino.write_text(conteudo.lstrip(), encoding="utf-8")
    print("Arquivo gerado:", destino)