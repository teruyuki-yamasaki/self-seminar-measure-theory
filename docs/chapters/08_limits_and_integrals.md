# 第8章 極限と積分の交換

## 目的

この章の目的は, Lebesgue 積分において函数列の極限と積分の交換を保証する基本定理を述べることである.

点wise 収束だけでは, 一般に

$$
\lim_{n\to\infty}\int f_n\, d\mu
=
\int \lim_{n\to\infty}f_n\, d\mu
$$

は成り立たない.　極限と積分を交換するには, 単調性, 非負性, 支配函数の存在などの追加条件が必要である.

## 点wise 収束だけでは不十分である

$[0, 1]$ 上で

$$
f_n(x)=n\mathbf{1}_{(0, 1/n)}(x)
$$

と定める.

このとき

$$
f_n(x)\to0
$$

が各 $x\in[0, 1]$ について成り立つ.しかし

$$
\int_0^1 f_n\, d\mu=1
$$

であるから

$$
\lim_{n\to\infty}\int_0^1 f_n\, d\mu
=1
\neq
0
=
\int_0^1\lim_{n\to\infty}f_n\, d\mu.
$$

この例では, 函数の質量が $0$ の近くに集中し, 高さが大きくなっている.点ごとの極限だけを見るとこの集中を捉えられない.

![点wise 収束だけでは積分と交換できない例](../../figures/measure/animations/integral_on_subset_monotone_limit/gif/integral_on_subset_monotone_limit.gif)

点ごとの極限だけでは, 集合の上で保たれている積分量を制御できない.極限と積分を交換するには追加の仮定が必要である.

## 単調収束定理

非負可測函数列 $f_n$ が

$$
0\leq f_1\leq f_2\leq\cdots
$$

を満たし,

$$
f(x)=\lim_{n\to\infty}f_n(x)
$$

と定める.このとき $f$ は非負可測函数であり,

$$
\int_X f\, d\mu
=
\lim_{n\to\infty}\int_X f_n\, d\mu
$$

が成り立つ.

同値に,

$$
\int_X \lim_{n\to\infty}f_n\, d\mu
=
\lim_{n\to\infty}\int_X f_n\, d\mu
$$

である.

この定理を単調収束定理という.

単調収束定理では, 各 $f_n$ が非負であり, かつ函数列が単調増加であることが本質的である.この条件のもとでは, 積分値も単調増加し, その極限が極限函数の積分と一致する.

![単調増加する領域上の積分](../../figures/measure/animations/integral_on_subset_monotone_limit_2d/gif/integral_on_subset_monotone_limit_2d.gif)

非負性と単調性がある場合, 近似される領域または函数が増大すると, 積分値もその極限へ増大する.

## Fatou の補題

非負可測函数列 $f_n$ に対して,

$$
\int_X \liminf_{n\to\infty} f_n\, d\mu
\leq
\liminf_{n\to\infty}\int_X f_n\, d\mu
$$

が成り立つ.

これを Fatou の補題という.

Fatou の補題は, 非負可測函数列について常に成り立つ下半連続性の主張である.点wise 極限が存在しない場合でも, 下極限を用いることで積分に関する不等式を得る.

証明の基本方針は

$$
g_n=\inf_{k\geq n}f_k
$$

とおくことである.このとき $g_n$ は単調増加し,

$$
g_n\uparrow \liminf_{n\to\infty}f_n
$$

となる.単調収束定理を $g_n$ に適用し, さらに $g_n\leq f_k$ $(k\geq n)$ を用いる.

## 優収束定理

可測函数列 $f_n$ が

$$
f_n\to f\quad \mu\text{-a.e.}
$$

を満たすとする.

さらに, ある $g\in L^1(\mu)$ が存在して, すべての $n$ について

$$
|f_n|\leq g\quad \mu\text{-a.e.}
$$

が成り立つとする.

このとき $f\in L^1(\mu)$ であり,

$$
\int_X f_n\, d\mu
\to
\int_X f\, d\mu
$$

が成り立つ.

さらに

$$
\int_X |f_n-f|\, d\mu\to0
$$

も成り立つ.

この定理を優収束定理という.

## 優収束定理の意味

優収束定理の条件は二つに分けられる.

第一に, $f_n$ は $f$ に a.e. 収束する.

$$
f_n\to f\quad \mu\text{-a.e.}
$$

第二に, すべての $f_n$ は一つの可積分函数 $g$ によって支配される.

$$
|f_n|\leq g\quad \mu\text{-a.e.}
$$

支配函数 $g$ の存在により, 函数列の質量が狭い領域に集中したり, 高さだけが大きくなったりすることを防ぐ.

第5章の例

$$
f_n(x)=n\mathbf{1}_{(0, 1/n)}(x)
$$

では, 点wise には $0$ に収束するが, 可積分な支配函数 $g$ は存在しない.したがって優収束定理の仮定を満たさない.

## $L^1$ 収束

可測函数列 $f_n$ と可測函数 $f$ について

$$
\int_X |f_n-f|\, d\mu\to0
$$

が成り立つとき, $f_n$ は $f$ に $L^1$ 収束するという.

優収束定理は, a.e. 収束と可積分支配函数の存在から $L^1$ 収束を導く定理である.

$L^1$ 収束が成り立てば,

$$
\left|\int_X f_n\, d\mu-\int_X f\, d\mu\right|
\leq
\int_X |f_n-f|\, d\mu
\to0
$$

であるから, 積分値の収束も従う.

## この章の中心メッセージ

Lebesgue 積分では, 非負性と単調性による単調収束定理, 非負函数列に対する Fatou の補題, 可積分な支配函数による優収束定理によって, 極限と積分の関係を体系的に扱うことができる.優収束定理は, 本発表の到達点である.
