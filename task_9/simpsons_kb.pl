% -------------------------
% Simpsons Knowledge Base
% -------------------------

% Facts (people)
person(homer).
person(marge).
person(bart).
person(lisa).
person(maggie).
person(ned).
person(maude).
person(milhouse).
person(monty_burns).
person(smithers).
person(krusty).
person(apu).

% Facts (relationships)
parent(homer, bart).
parent(marge, bart).
parent(homer, lisa).
parent(marge, lisa).
parent(homer, maggie).
parent(marge, maggie).

spouse(homer, marge).
spouse(marge, homer).

friend(bart, milhouse).
friend(milhouse, bart).
friend(homer, ned).

works_at(homer, springfield_nuclear_plant).
owns(monty_burns, springfield_nuclear_plant).
assistant(smithers, monty_burns).

job(krusty, comedian).
job(apu, shopkeeper).

% Facts (traits)
smart(lisa).
mischievous(bart).
kind(ned).

% -------------------------
% Rules (5–10)
% -------------------------

% 1) child/2
child(C, P) :- parent(P, C).

% 2) father/2 (simple: father is a parent and male)
male(homer).
male(bart).
male(ned).
male(milhouse).
male(monty_burns).
male(smithers).
male(krusty).
male(apu).

father(F, C) :- parent(F, C), male(F).

% 3) mother/2
female(marge).
female(lisa).
female(maggie).
female(maude).

mother(M, C) :- parent(M, C), female(M).

% 4) sibling/2
sibling(A, B) :-
    parent(P, A),
    parent(P, B),
    A \= B.

% 5) grandparent/2
grandparent(GP, C) :-
    parent(GP, P),
    parent(P, C).

% 6) coworker/2
coworker(A, B) :-
    works_at(A, X),
    works_at(B, X),
    A \= B.

% 7) boss_of/2
boss_of(B, E) :-
    owns(B, X),
    works_at(E, X).

% 8) connected/2 (friends or spouses)
connected(A, B) :- friend(A, B).
connected(A, B) :- spouse(A, B).