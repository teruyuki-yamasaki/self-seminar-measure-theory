---
layout: section
---

# 6. 可測函数と単函数

Lebesgue 積分の対象と基本単位

---
layout: two-cols
---

# 可測函数

測度空間 $(X,\mathfrak{B},\mu)$ 上の函数 $f:X\to\mathbb{R}$ が可測であるとは, 任意の実数 $a$ に対して

$$
\{x\in X\mid f(x)>a\}\in\mathfrak{B}
$$

が成り立つこと.

::note
函数の値によって定まる集合が測度で扱えることを要求している.
::

::right::

<img class="slide-figure" src="../figures/measure/animations/measurable_function_preimage_2d/gif/measurable_function_preimage_2d.gif" alt="可測函数が値域の集合を定義域の可測集合へ戻す概念図" />

---
layout: two-cols
---

# 逆像として見る

値域側の区間を切り出したとき, その逆像が定義域側で可測集合になる.

$$
f^{-1}([\alpha,\beta))\in\mathfrak{B}
$$

この条件により

$$
\mu\left(\{x\mid \alpha\le f(x)<\beta\}\right)
$$

が定義できる.

::right::

<img class="slide-figure" src="../figures/measure/animations/measurable_function_preimage_1d/gif/measurable_function_preimage_1d.gif" alt="可測函数の逆像" />

---
layout: two-cols
---

# 定義函数

集合 $E\subset X$ の定義函数は

$$
\mathbf{1}_E(x)=
\begin{cases}
1 & (x\in E),\\
0 & (x\notin E)
\end{cases}
$$

である.

$E\in\mathfrak{B}$ であるとき, $\mathbf{1}_E$ は可測函数である.

::note
集合 $E$ が可測であることと, その定義函数 $\mathbf{1}_E$ が可測であることは同値である.
::

::right::

<img class="slide-figure" src="../figures/measure/static/concepts/indicator_function_set.png" alt="集合を 0 と 1 の定義函数として見る概念図" />

---
layout: two-cols
---

# 単函数

単函数とは

$$
\varphi=\sum_{k=1}^{n}a_k\mathbf{1}_{E_k}
$$

の形で表される可測函数である.

::example-box{title="基本単位"}
単函数は, 有限個の可測集合上で定数値を取る函数である.
::

::right::

<img class="slide-figure" src="../figures/measure/static/simple_function_examples_1d.png" alt="1次元の単函数" />

---
layout: two-cols
---

# 単函数による近似

非負可測函数は, 非負単函数列によって下から単調に近似できる.

$$
0\le\varphi_1\le\varphi_2\le\cdots\le f,
\qquad
\varphi_n(x)\uparrow f(x)
$$

::note
この事実が Lebesgue 積分の定義を支えている.
::

::right::

<img class="slide-figure" src="../figures/measure/animations/monotone_simple_approximation/gif/monotone_simple_approximation.gif" alt="非負可測函数の単函数近似" />

---
layout: two-cols
---

# 第6章の結論

::example-box{title="中心メッセージ"}
可測函数とは, 値によって定まる集合が測度で扱える函数である.

単函数は可測集合の定義函数の有限線形結合であり, Lebesgue 積分を構成する基本単位である.
::

::right::

<img class="slide-figure" src="../figures/measure/static/concepts/simple_function_algebra.png" alt="単函数を定義函数の有限線形結合として見る概念図" />

---
