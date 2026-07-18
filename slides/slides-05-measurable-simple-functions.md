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

::right::

<img class="slide-figure" src="../figures/measure/animations/measurable_function_preimage_1d/gif/measurable_function_preimage_1d.gif" alt="可測函数の逆像" />

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

<img class="slide-figure" src="../figures/measure/animations/measurable_function_preimage_2d/gif/measurable_function_preimage_2d.gif" alt="2次元の可測函数の逆像" />

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

典型的には, 互いに素な可測集合 $E_k$ によって

$$
\varphi(x)=\sum_{k=1}^n a_k\mathbf{1}_{E_k}(x),
\qquad
X=E_1+\cdots+E_n
$$

と書ける.

::right::

<img class="slide-figure" src="../figures/measure/static/simple_function_examples_1d.png" alt="1次元の単函数" />

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

<img class="slide-figure" src="../figures/measure/animations/simple_function_examples_2d/gif/simple_function_examples_2d.gif" alt="単函数の値と可測集合" />

---
layout: default
---

# 非負単函数

非負単函数は, 係数 $a_i$ がすべて $0$ 以上である単函数である.

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
layout: two-cols
---

# 単函数による近似

非負可測函数は, 下から増加する非負単函数列で近似できる.

$$
0\le \varphi_1\le\varphi_2\le\cdots\le f
$$

かつ各点で

$$
\varphi_n(x)\nearrow f(x)
$$

この事実が, 非負可測函数の Lebesgue 積分を定義する土台になる.

::right::

<img class="slide-figure" src="../figures/measure/animations/monotone_simple_approximation/gif/monotone_simple_approximation.gif" alt="非負可測函数の単函数近似" />

---
layout: end
---

# この章の中心メッセージ

- 可測函数は, 値域側で切った集合の逆像を可測集合として扱える函数である.
- 定義函数と単函数は, 可測集合を使って函数を組み立てる基本部品である.
- 非負可測函数は単函数で下から近似でき, Lebesgue 積分の定義につながる.
