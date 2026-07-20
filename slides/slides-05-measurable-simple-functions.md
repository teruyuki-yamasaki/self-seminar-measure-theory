---
layout: section
---

# 第5章 可測函数と単函数

Lebesgue 積分の対象となる函数を準備する

---
layout: default
---

# 目的

測度空間上で函数を積分するために, 可測函数と単函数を導入する.

Lebesgue 積分では, 函数値そのものだけでなく, 値域の集合を定義域に戻した逆像が可測であることが重要になる.

---
layout: two-cols
---

# 可測函数

測度空間 $(X,\mathfrak{B},\mu)$ 上の函数

$$
f:X\to\mathbb{R}
$$

が可測であるとは, 任意の $\alpha<\beta$ に対して

$$
f^{-1}([\alpha,\beta))
=
\{x\in X\mid \alpha\le f(x)<\beta\}
\in\mathfrak{B}
$$

が成り立つことである.

すなわち, 値域 $\mathbb{R}$ 上の可測集合を定義域 $X$ に戻した逆像が可測集合であることを要求する.

::right::

![可測函数の逆像](../figures/measure/animations/measurable_function_preimage_1d/gif/measurable_function_preimage_1d.gif)

---
layout: two-cols
---

# 2次元の可測函数の逆像

可測性は, 値域側で切った集合を定義域側に戻したときに,
その集合の大きさを測れることを保証する.

平面領域でも同様に,

$$
\{(x,y)\in X\mid \alpha\le f(x,y)<\beta\}
=
f^{-1}([\alpha,\beta))
\in\mathfrak{B}
$$

であることを見る.

Lebesgue 積分では, 値域の層ごとの逆像を測るため, この性質が基本になる.

::right::

![2次元の可測函数の逆像](../figures/measure/animations/measurable_function_preimage_2d/gif/measurable_function_preimage_2d.gif)

---
layout: default
---

# 可測函数の安定性

可測函数は, 四則演算や極限操作に対して安定に振る舞う.

すなわち, 函数 $f,g: X\to\mathbb{R}$ が可測で $c\in\mathbb{R}$ なら

$$
f+g,\quad cf,\quad fg,\quad |f|
$$

も可測である.

また可測函数列 $f_n$ について

$$
\limsup_{n\to\infty}f_n,\qquad
\liminf_{n\to\infty}f_n
$$

も可測である.

Lebesgue 積分論では, この可測性の安定性が収束定理の前提になる.

---
layout: default
---

# 定義函数

集合 $A\in\mathfrak{B}$ に対して, 定義函数を

$$
\mathbf{1}_A(x):=
\begin{cases}
1 & x\in A,\\
0 & x\notin A
\end{cases}
$$

で定める.

可測集合の定義函数は可測函数であり, 逆に

$$
E=\{x\in X\mid \mathbf{1}_E(x)>1/2\}
$$

なので, $\mathbf{1}_E$ が可測なら $E\in\mathfrak{B}$ である.

---
layout: two-cols
---

# 単函数

単函数とは, 有限個の値しか取らない可測函数である.

典型的には, 互いに素な可測集合 $E_1,\ldots,E_n \in \mathfrak{B}$ によって

$$
\varphi(x):=\sum_{k=1}^n a_k\mathbf{1}_{E_k}(x),
\qquad
X=\bigsqcup_{k=1}^n E_k
$$

と書ける.

::right::

![1次元の単函数](../figures/measure/static/simple_function_examples_1d.png)

---
layout: two-cols
---

# 単函数の値と可測集合

単函数は, 定義域を有限個の可測集合に分け, 各部分集合で一定値を取る函数である.

値を $a_1,\ldots,a_n$ とすれば

$$
E_k:=\{x\in X\mid \varphi(x)=a_k\}\in\mathfrak{B}
$$

であり, この $E_k$ が積分で測る対象になる.

Lebesgue 積分では, まず単函数の積分を定義し, そこから一般の非負可測函数へ拡張する.

::right::

![単函数の値と可測集合](../figures/measure/animations/simple_function_examples_2d/gif/simple_function_examples_2d.gif)

---
layout: default
---

# 非負単函数

**非負単函数** は, 係数 $a_i$ がすべて $0$ 以上である単函数である.

$$
\varphi(x)=\sum_{i=1}^n a_i\mathbf{1}_{A_i}(x),
\qquad a_i\ge0
$$

非負単函数の積分は, 各値とその値を取る集合の測度の積の有限和として定義される.

$$
\int_X\varphi(x)\,d\mu(x)
:=
\sum_{i=1}^n a_i\mu(A_i)
$$

---
layout: two-rows
---

# 非負可測函数の単函数近似

非負可測函数 $f: X\to[0,\infty]$ は, 単調増加な非負単函数列 $\varphi_n: X\to[0,\infty)$ で下から近似できる.

$$
\forall x\in X,\quad 0\le\varphi_1(x)\le\varphi_2(x)\le\cdots\le f(x) \quad \wedge \quad \varphi_n(x)\nearrow f(x)
$$

この事実が, 非負可測函数の Lebesgue 積分を定義する土台になる.

::right::

![非負可測函数の単函数近似](../figures/measure/animations/monotone_simple_approximation/gif/monotone_simple_approximation.gif)

---
layout: end
---

# この章の中心メッセージ

- 可測函数は, 値域側で切った集合の逆像を可測集合として扱える函数である.
- 定義函数と単函数は, 可測集合を使って函数を組み立てる基本部品である.
- 非負可測函数は単函数で下から近似でき, Lebesgue 積分の定義につながる.
