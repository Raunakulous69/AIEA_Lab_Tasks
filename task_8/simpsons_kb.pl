% ============================================================
% Simpsons Knowledge Base
% 20 facts, 8 rules
% ============================================================

% --- Gender facts (10) ---
male(homer).
male(bart).
male(abe).
male(herb).
female(marge).
female(lisa).
female(maggie).
female(mona).
female(patty).
female(selma).

% --- Parent facts (9) ---
parent(homer, bart).
parent(homer, lisa).
parent(homer, maggie).
parent(marge, bart).
parent(marge, lisa).
parent(marge, maggie).
parent(abe, homer).
parent(abe, herb).
parent(mona, homer).

% --- Sibling facts (1) ---
sibling(selma, marge).

% ============================================================
% Rules
% ============================================================

% mother(X, Y): X is the mother of Y
mother(X, Y) :- parent(X, Y), female(X).

% father(X, Y): X is the father of Y
father(X, Y) :- parent(X, Y), male(X).

% grandparent(X, Y): X is a grandparent of Y
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

% grandmother(X, Y): X is the grandmother of Y
grandmother(X, Y) :- grandparent(X, Y), female(X).

% grandfather(X, Y): X is the grandfather of Y
grandfather(X, Y) :- grandparent(X, Y), male(X).

% ancestor(X, Y): X is an ancestor of Y (recursive)
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% aunt(X, Y): X is an aunt of Y
aunt(X, Y) :- sibling(X, P), parent(P, Y), female(X).

% related(X, Y): X and Y share a common ancestor
related(X, Y) :- ancestor(Z, X), ancestor(Z, Y), X \= Y.