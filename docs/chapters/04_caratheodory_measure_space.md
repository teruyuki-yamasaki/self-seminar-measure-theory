# 第4章 Carathéodory の定理と抽象的測度空間

## 目的

この章の目的は, 前章で得た Lebesgue 測度の構成から, 抽象的な外測度, 可測性, 測度空間の定義を取り出すことである.

前章では, Lebesgue 外測度 $\mu^*$ から Lebesgue 可測集合族 $\mathfrak{M}_{\mu^*}$ を取り出し, その上に Lebesgue 測度 $\mu$ を定めた.
これにより

$$
(\mathbb{R}^N, \mathfrak{M}_{\mu^*}, \mu)
$$

という三つ組が得られた.

この章では, まずこの構成を一般の集合 $X$ 上の外測度に対して見直す. そのうえで, 測度空間

$$
(X, \mathfrak{B}, \mu)
$$

という一般の枠組みを定義する.

## 外測度の抽象化

集合 $X$ に対して, 冪集合 $2^X$ 上の集合函数

$$
\Gamma:2^X\to[0,\infty]
$$

が次を満たすとき, $\Gamma$ を $X$ 上の **外測度** という.

1. （空集合の外測度）$\Gamma(\emptyset)=0$.
2. （単調性）$A\subset B$ ならば

$$
\Gamma(A)\leq\Gamma(B).
$$

3. （可算劣加法性）$A_1,A_2,\ldots\subset X$ ならば

$$
\Gamma\left(\bigcup_{n=1}^{\infty}A_n\right)
\leq
\sum_{n=1}^{\infty}\Gamma(A_n).
$$

第2章で導入した Lebesgue 外測度 $\mu^*$ は, $X=\mathbb{R}^N$ の場合の外測度である.

![Carathéodory の外測度の基本性質](../../figures/measure/animations/caratheodory_outer_measure_axioms/gif/caratheodory_outer_measure_axioms.gif)

また,

$$
\Gamma(N)=0
$$

を満たす集合 $N\subset X$ を, $\Gamma$ に関する **零集合** という.

## Carathéodory 可測性

外測度 $\Gamma$ が $X$ 上に定義されているとする.

集合 $E\subset X$ が, 任意の集合 $A\subset X$ に対して

$$
\Gamma(A)
=
\Gamma(A\cap E)+\Gamma(A\cap E^c)
$$

を満たすとき, $E$ は **Carathéodory 可測** である, または $\Gamma$-**可測**であるという.

$\Gamma$-可測集合全体を

$$
\mathfrak{M}_\Gamma
:=
\{E\subset X \mid
\forall A\subset X,\quad
\Gamma(A)=\Gamma(A\cap E)+\Gamma(A\cap E^c)\}
$$

と書く.

第3章で定義した Lebesgue 可測集合は, この定義で $X=\mathbb{R}^N$, $\Gamma=\mu^*$ とした場合である.

外測度の可算劣加法性から, 任意の $A,E\subset X$ について

$$
\Gamma(A)
\leq
\Gamma(A\cap E)+\Gamma(A\cap E^c)
$$

は常に成り立つ. Carathéodory 可測性は, 逆向きの不等式も含めて等号が成り立つことを要求する.

## 可算加法族

第3章では, Lebesgue 可測集合全体 $\mathfrak{M}_{\mu^*}$ が可算操作に対して閉じていることを述べた.
ここでは, その性質を一般の集合族の定義として取り出す.

空間 $X$ の部分集合族 $\mathfrak{B}$ が次を満たすとき, $\mathfrak{B}$ を**可算加法族**, **完全加法族**, または **$\sigma$-加法族** という. ここで $\sigma$ は可算を意味する.

1. （空集合に対する閉性）$\emptyset\in\mathfrak{B}$.
2. （補集合に対する閉性）$A\in\mathfrak{B}$ ならば $A^c\in\mathfrak{B}$.
3. （可算和に対する閉性）$A_1, A_2, \ldots\in\mathfrak{B}$ ならば

$$
\bigcup_{n=1}^{\infty}A_n\in\mathfrak{B}.
$$

この定義から, $X\in\mathfrak{B}$ である. 実際,

$$
X=\emptyset^c
$$

である.

また, de Morgan の法則により, 可算個の積集合についても

$$
\bigcap_{n=1}^{\infty}A_n
=
\left(\bigcup_{n=1}^{\infty}A_n^c\right)^c
\in\mathfrak{B}
$$

となる.

したがって, 可算加法族は可算回の和・差・積の演算に対して閉じている.

## Carathéodory の定理

Carathéodory の定理は, 外測度から取り出した可測集合全体が, 可算操作に対して安定な集合族になることを主張する.

すなわち, 外測度 $\Gamma$ に対して, $\Gamma$-可測集合全体 $\mathfrak{M}_\Gamma$ は可算加法族である.

さらに, 外測度 $\Gamma$ を可測集合族 $\mathfrak{M}_\Gamma$ 上に制限すると,

$$
\Gamma|_{\mathfrak{M}_\Gamma}:\mathfrak{M}_\Gamma\to[0,\infty]
$$

は可算加法的になる.

つまり, 互いに素な可測集合列

$$
E_1,E_2,\ldots\in\mathfrak{M}_\Gamma
$$

に対して

$$
\Gamma\left(\bigcup_{n=1}^{\infty}E_n\right)
=
\sum_{n=1}^{\infty}\Gamma(E_n)
$$

が成り立つ.

第3章の Lebesgue 測度の構成は, この定理を Lebesgue 外測度 $\mu^*$ に適用したものである.

## 測度

可算加法族 $\mathfrak{B}$ 上の集合函数

$$
\mu:\mathfrak{B}\to\mathbb{R}\cup\{\infty\}
$$

が次を満たすとき, $\mu$ を $\mathfrak{B}$ 上の**測度**という.

1. （非負性）任意の $A\in\mathfrak{B}$ に対して

$$
0\leq \mu(A)\leq \infty.
$$

2. （空集合の測度）$\mu(\emptyset)=0$.
3. （可算加法性）$A_1, A_2, \ldots\in\mathfrak{B}$ が互いに素ならば

$$
\mu\left(\bigcup_{n=1}^{\infty}A_n\right)
=
\sum_{n=1}^{\infty}\mu(A_n).
$$

ここで非負性は, 値域を $[0,\infty]$ に取っていることに対応している.

有限加法性は可算加法性から従う. 実際, 互いに素な $A_1, \ldots, A_N\in\mathfrak{B}$ に対して, $A_n=\emptyset$ $(n>N)$ とおけば

$$
\mu\left(\bigcup_{n=1}^{N}A_n\right)
=
\sum_{n=1}^{N}\mu(A_n)
$$

が得られる.

## 測度の基本性質

測度 $\mu$ は次の性質を満たす.

### 単調性

$A, B\in\mathfrak{B}$ かつ $A\subset B$ ならば,

$$
\mu(A)\leq \mu(B)
$$

である.

実際,

$$
B=A\cup(B-A)
$$

と互いに素な和に分解できるので,

$$
\mu(B)=\mu(A)+\mu(B-A)\geq\mu(A)
$$

となる.

### 可算劣加法性

$A_1, A_2, \ldots\in\mathfrak{B}$ に対して,

$$
\mu\left(\bigcup_{n=1}^{\infty}A_n\right)
\leq
\sum_{n=1}^{\infty}\mu(A_n)
$$

である.

互いに素でない集合列に対しては,

$$
B_1:=A_1, \qquad
B_n:=A_n-\bigcup_{k=1}^{n-1}A_k
$$

とおくと, $B_n$ は互いに素であり

$$
\bigcup_{n=1}^{\infty}A_n
=
\bigcup_{n=1}^{\infty}B_n
$$

である. さらに $B_n\subset A_n$ なので, 単調性から可算劣加法性が従う.

### 下からの連続性

$A_1\subset A_2\subset\cdots$ ならば,

$$
\mu\left(\bigcup_{n=1}^{\infty}A_n\right)
=
\lim_{n\to\infty}\mu(A_n)
$$

が成り立つ.

これは集合列の極限と測度が整合する基本性質である.
集合が下から増大するとき, その合併の測度は各段階の測度の極限として捉えられる. これは測度が可算極限操作と整合することを示す基本性質である.

## 零集合と a.e.

第2章では, 可算集合が Lebesgue 外測度 $0$ の集合であることを見た.
第3章では, Lebesgue 外測度 $0$ の集合が Lebesgue 可測であることを見た.
測度空間では, 同じ考えを一般の測度 $\mu$ に対して次のように表す.

集合 $N\in\mathfrak{B}$ が

$$
\mu(N)=0
$$

を満たすとき, $N$ を零集合という.

集合 $E\in\mathfrak{B}$ 上の点 $x$ に関する命題 $P(x)$ が, ある零集合 $N\subset E$ を除いて成り立つとき, $P(x)$ は $E$ 上で $\mu$ に関して **ほとんど至る所 (almost everywhere, a.e.)** 成り立つという.

記号では

$$
P(x)\quad \mu\text{-a.e. }x\in E
$$

のように書く.

例えば Lebesgue 測度に関して,

$$
\mathbf{1}_{\mathbb{Q}}(x)=0
\quad
\mu\text{-a.e. }x\in\mathbb{R}
$$

である. これは $\mathbb{Q}$ が可算集合であり, Lebesgue 測度 $0$ であるためである.
可算集合が測度 $0$ になることにより, a.e. の議論では可算個の例外点を同時に無視できる.

## 測度空間

空間 $X$, その上の可算加法族 $\mathfrak{B}$, および $\mathfrak{B}$ 上の測度 $\mu$ の組

$$
(X, \mathfrak{B}, \mu)
$$

を**測度空間**という.

前章の構成は, Lebesgue 外測度から一つの測度空間を作る手続きだったと見なせる.

## 測度空間の例

### Lebesgue 測度空間

Lebesgue 測度空間は

$$
(\mathbb{R}^N, \mathfrak{M}_{\mu^*}, \mu)
$$

である.

ここで $\mathfrak{M}_{\mu^*}$ は Lebesgue 可測集合全体であり, $\mu$ は Lebesgue 測度である.

### Borel 測度空間

開集合をすべて含む最小の可算加法族を **Borel 集合族** といい,

$$
\mathfrak{B}(\mathbb{R}^N)
$$

と書く.

すべての Borel 集合は Lebesgue 可測である. したがって,

$$
\mathfrak{B}(\mathbb{R}^N)\subset \mathfrak{M}_{\mu^*}
$$

である.

Lebesgue 測度 $\mu$ を Borel 集合族に制限すると,

$$
(\mathbb{R}^N, \mathfrak{B}(\mathbb{R}^N), \mu|_{\mathfrak{B}(\mathbb{R}^N)})
$$

も測度空間になる.

Lebesgue 可測集合族は Borel 集合族より大きく, Borel 集合に零集合を加えて得られる集合も含む.
発表ではこの包含関係の細部よりも, 開集合, 閉集合, 区間, 可算集合が Lebesgue 可測集合として扱えることが重要である.

### 確率空間

確率空間も測度空間の一種である. 確率空間では

$$
(\Omega, \mathfrak{B}, P)
$$

と書き, 全体空間の測度が

$$
P(\Omega)=1
$$

であることを要求する.

このとき, 事象 $A, B\in\mathfrak{B}$ に対して, 和集合 $A\cup B$, 積集合 $A\cap B$, 差集合 $A-B$, 補集合 $A^c$ も再び $\mathfrak{B}$ に属する.
したがって, これらに対して確率を考えることができる.

特に, 測度の一般論から

$$
P(A^c)=1-P(A)
$$

が成り立ち, また

$$
P(A\cup B)=P(A)+P(B)-P(A\cap B)
$$

である.

さらに, $A\cap B=\emptyset$ ならば

$$
P(A\cup B)=P(A)+P(B)
$$

となり, $A\subset B$ ならば

$$
P(B-A)=P(B)-P(A)
$$

となる.

このように確率空間は, 全体の確率が $1$ に正規化された測度空間であり, 事象の和・積・差に対する関係を測度の言葉で統一的に扱う枠組みになっている.

## この章の中心メッセージ

測度空間 $(X, \mathfrak{B}, \mu)$ は, 集合に大きさを与える理論の抽象的枠組みである. その本質は, 可算集合操作に閉じた集合族 $\mathfrak{B}$ と, その上で可算加法性を満たす測度 $\mu$ にある.
