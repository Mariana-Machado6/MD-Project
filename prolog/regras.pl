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
