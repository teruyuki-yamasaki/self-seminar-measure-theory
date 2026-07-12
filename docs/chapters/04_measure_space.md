# 第4章 抽象的測度空間

## 目的

この章の目的は, 前章で得た Lebesgue 測度の構成から, 抽象的な測度空間の定義を取り出すことである.

前章では, Lebesgue 外測度 $\mu^*$ から Lebesgue 可測集合族 $\mathfrak{M}_{\mu^*}$ を取り出し, その上に Lebesgue 測度 $\mu$ を定めた.
これにより

$$
(\mathbb{R}^N, \mathfrak{M}_{\mu^*}, \mu)
$$

という三つ組が得られた.

この章では, この形式だけを取り出して

$$
(X, \mathfrak{B}, \mu)
$$

という一般の枠組みとして扱う.

## 可算加法族

前章では, Carathéodory 可測集合全体 $\mathfrak{M}_\Gamma$ が可算加法族になることを見た.
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
B=A\cup(B\setminus A)
$$

と互いに素な和に分解できるので,

$$
\mu(B)=\mu(A)+\mu(B\setminus A)\geq\mu(A)
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
B_n:=A_n\setminus\bigcup_{k=1}^{n-1}A_k
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
第3章では, 外測度 $0$ の集合が Carathéodory 可測であることを見た.
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

## この章の中心メッセージ

測度空間 $(X, \mathfrak{B}, \mu)$ は, 集合に大きさを与える理論の抽象的枠組みである. その本質は, 可算集合操作に閉じた集合族 $\mathfrak{B}$ と, その上で可算加法性を満たす測度 $\mu$ にある.
