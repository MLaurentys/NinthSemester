%%%%% Insira aqui os seus predicados.
%%%%% Use quantos predicados auxiliares julgar necess�rio

%
% 1
%
% Uses built-in "member"
to_set([], _, []) .

to_set([H|T], S, C) :-
    member(H, S),
    !,
    to_set(T, S, C).

to_set([H|T], S, [H|C]) :-
    !,
    to_set(T, [H|S], C).

perm([], []).
perm([H|X],Y) :-
    perm(X, Y2),
    select(H, Y, Y2).

lista_para_conjunto(L, C) :- 
    to_set(L, [], C).
%
% 2
%
% Uses function from 1

% mesmo_conjunto_fix([], [], [], []).
% mesmo_conjunto_fix(_, _, [], []).
% mesmo_conjunto_fix(Xb, Yb, [Hx|Tx], []) :-
%     member(Hx, Yb),
%     mesmo_conjunto_fix(Xb, Yb, Tx, []).
    
% mesmo_conjunto_fix(Xb, Yb, [], [Hy|Ty]) :-
%     member(Hy, Xb),
%     mesmo_conjunto_fix(Xb, Yb, [], Ty).

% mesmo_conjunto_fix(Xb, Yb, [Hx|Tx], [Hy|Ty]) :-
%     member(Hx, Yb),
%     member(Hy, Xb),
%     mesmo_conjunto_fix(Xb, Yb, Tx, Ty).

% mesmo_conjunto([], []).

mesmo_conjunto(X, Y) :-
    lista_para_conjunto(X, Xf),
    %mesmo_conjunto_fix(Xf, Yf, Xf, Yf),
    perm(Xf, Y).

%
% 3
%
% Uses function from 1


append_to([], L2, L2).

append_to([H|L1], L2, [H|X]) :-
	append_to(L1, L2, X).
uniao_conjunto(Cs, Ds, Esfp) :-
    lista_para_conjunto(Cs, Csf),
    lista_para_conjunto(Ds, Dsf),
    append_to(Csf, Dsf, Es),
    lista_para_conjunto(Es, Esfp).

%
% 4
%
% Uses function from 1


intersection_(_,_,[],[],[]).
intersection_(_,[],_,_,[]).
intersection_([],_,_,_,[]).
intersection_(L1b, L2b, [], [H|L2], [H|X]) :-
    member(H, L1b),
    !,
    intersection_(L1b, L2b, [], L2, X).
intersection_(L1b, L2b, [], [_|L2], X) :-
    intersection_(L1b, L2b, [], L2, X).
intersection_(L1b, L2b, [H|L1], L2, [H|X]) :-
    member(H, L2b),
    !,
    intersection_(L1b, L2b, L1, L2, X).
intersection_(L1b, L2b, [_|L1], L2, X):-
    intersection_(L1b, L2b, L1, L2, X).

inter_conjunto(Cs, Ds, Esf) :-
    lista_para_conjunto(Cs, Csf),
    lista_para_conjunto(Ds, Dsf),
    intersection_(Csf, Dsf, Csf, Dsf, Es),
    lista_para_conjunto(Es, Esf).

%
% 5
%
% Uses function from 1

set_minus([], _, []).

set_minus([H|L1], L2, X):-
    member(H, L2),
	!,
    set_minus(L1, L2, X).

set_minus([H|L1], L2, [H|X]):-
	!,
    set_minus(L1, L2, X).
    
diferenca_conjunto(Cs, Ds, Esf):-
    lista_para_conjunto(Cs, Csf),
    lista_para_conjunto(Ds, Dsf),
	set_minus(Csf, Dsf, Esf).


%%%%%%%% Fim dos predicados adicionados
%%%%%%%% Os testes come�am aqui.
%%%%%%%% Para executar os testes, use a consulta:   ?- run_tests.

%%%%%%%% Mais informacoes sobre testes podem ser encontradas em:
%%%%%%%%    https://www.swi-prolog.org/pldoc/package/plunit.html

:- begin_tests(conjuntos).
test(lista_para_conjunto, all(Xs=[[1,a,3,4]]) ) :-
    lista_para_conjunto([1,a,3,3,a,1,4], Xs).
test(lista_para_conjunto2,fail) :-
    lista_para_conjunto([1,a,3,3,a,1,4], [a,1,3,4]).

test(mesmo_conjunto, set(Xs=[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    mesmo_conjunto([1,a,3], Xs).
test(uniao_conjunto2,fail) :-
    mesmo_conjunto([1,a,3,4], [1,3,4]).

test(uniao_conjunto, set(Ys==[[1,a,3],[1,3,a],[a,1,3],[a,3,1],[3,a,1],[3,1,a]])) :-
    uniao_conjunto([1,a], [a,3], Xs),
    mesmo_conjunto(Xs,Ys).
test(uniao_conjunto2,fail) :-
    uniao_conjunto([1,a,3,4], [1,2,3,4], [1,1,a,2,3,3,4,4]).

test(inter_conjunto, all(Xs==[[1,3,4]])) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], Xs).
test(inter_conjunto2,fail) :-
    inter_conjunto([1,a,3,4], [1,2,3,4], [1,1,3,3,4,4]).

test(diferenca_conjunto, all(Xs==[[2]])) :-
    diferenca_conjunto([1,2,3], [3,a,1], Xs).
test(diferenca_conjunto2,fail) :-
    diferenca_conjunto([1,3,4], [1,2,3,4], [_|_]).

:- end_tests(conjuntos).
