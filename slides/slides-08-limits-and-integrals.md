---
layout: section
---

# 第7章 極限と積分の交換

Lebesgue 積分で極限操作を制御する

---
layout: default
---

# 目的

函数列の極限と積分の交換を扱う.

Lebesgue 積分の強みは, 単に積分できる函数の範囲を広げるだけでなく, 極限操作との相性を定理として保証できる点にある.

---
layout: default
---

# まず分けるべき二つの問題

極限と積分を考えるとき, 次の二つを分ける.

$$
\text{(I)}\quad
f_n\in L^1\ \Longrightarrow\ f\in L^1\ ?
$$

$$
\text{(II)}\quad
\lim_{n\to\infty}\int_X f_n\,d\mu
\overset{?}{=}
\int_X \lim_{n\to\infty}f_n\,d\mu
$$

各点収束だけでは, この二つは一般には保証されない.

---
layout: two-cols
---

# 各点収束だけでは積分値は制御できない

函数列が各点で $0$ に収束しても, 面積が移動したり集中したりすると, 積分値は $0$ に近づかないことがある.

例えば $[0,1]$ 上で

$$
f_n(x)=n\mathbf{1}_{(0,1/n]}(x),
\qquad
f_n(x)\to0
$$

だが

$$
\int_0^1 f_n\,d\mu=1
$$

点ごとの収束だけでは, 積分の大きさを制御できない.

::right::

<img class="slide-figure" src="../figures/measure/animations/pointwise_not_enough/gif/pointwise_not_enough.gif" alt="各点収束だけでは積分を制御できない" />

---
layout: default
---

# Riemann 積分での古典的な十分条件

Riemann 積分では, 一様収束があれば極限と積分を交換できる.

$$
\left|\int_a^b f_n-\int_a^b f\right|
\le
(b-a)\|f_n-f\|_\infty
\to0
$$

一様収束は強い条件であり, 点ごとの収束に比べて函数列全体のずれを一様に制御する.

---
layout: default
---

# 一様収束なら安全である

$f_n\to f$ が一様収束し, 各 $f_n$ が Riemann 可積分なら,

$$
\lim_{n\to\infty}\int_a^b f_n(x)\,dx
=
\int_a^b f(x)\,dx
$$

が成り立つ.

しかし Lebesgue 積分では, 一様収束より弱い条件でも積分と極限を交換できる.

---
layout: default
---

# Lebesgue 積分での見取り図

Lebesgue 積分では, 次の代表的な収束定理が現れる.

| 定理 | 主な条件 | 結論 |
| --- | --- | --- |
| Fatou の補題 | 非負函数列 | liminf と積分の不等式 |
| 単調収束定理 | 非負単調増加 | 積分と極限を交換できる |
| 優収束定理 | a.e. 収束と可積分支配 | 積分と極限を交換できる |

---
layout: default
---

# Fatou の補題

非負可測函数列 $f_n$ に対して

$$
\int_X \liminf_{n\to\infty} f_n\,d\mu
\le
\liminf_{n\to\infty}\int_X f_n\,d\mu
$$

が成り立つ.

Fatou の補題は, 非負性だけで得られる基本的な不等式である.

特に $f_n\to f$ a.e. で

$$
\sup_n\int_X f_n\,d\mu<\infty
$$

なら $\int_X f\,d\mu<\infty$ が従う.

---
layout: two-cols
---

# 単調収束定理

非負可測函数列が

$$
0\le f_1\le f_2\le\cdots,\qquad f_n\uparrow f
$$

を満たすなら,

$$
\lim_{n\to\infty}\int_X f_n\,d\mu
=
\int_X f\,d\mu
$$

が成り立つ.

つまり

$$
\int_X f_n\,d\mu
\uparrow
\int_X f\,d\mu
$$

::right::

<img class="slide-figure" src="../figures/measure/animations/integral_on_subset_monotone_limit_2d/gif/integral_on_subset_monotone_limit_2d.gif" alt="単調増加する領域上の積分" />

---
layout: default
---

# 優収束定理

$f_n\to f$ a.e. であり, ある可積分函数 $g$ が存在して

$$
|f_n|\le g
$$

をすべての $n$ で満たすなら,

$$
\lim_{n\to\infty}\int_X f_n\,d\mu
=
\int_X f\,d\mu
$$

が成り立つ.

さらに

$$
\int_X |f_n-f|\,d\mu\to0
$$

---
layout: default
---

# $L^1$ 収束

$L^1$ 収束とは

$$
\int_X |f_n-f|\,d\mu\to0
$$

である.

$L^1$ 収束は, 積分値の収束を直接制御する.

$$
\left|
\int_X f_n\,d\mu-\int_X f\,d\mu
\right|
\le
\int_X |f_n-f|\,d\mu
\to0
$$

---
layout: default
---

# 一様収束との関係

有限測度空間では, 一様収束は $L^1$ 収束を導く.

$$
\mu(X)<\infty,\ f_n\to f\text{ 一様}
\quad\Longrightarrow\quad
\int_X |f_n-f|\,d\mu
\le
\mu(X)\|f_n-f\|_\infty\to0
$$

しかし $L^1$ 収束や優収束定理は, 一様収束より広い状況を扱える.

Lebesgue 積分論では, a.e. 収束や可積分支配を使って極限操作を制御する.

---
layout: default
---

# Egorov の定理との関係

Egorov の定理は, 有限測度空間で a.e. 収束を「小さい例外集合を除けば一様収束」として捉える定理である.

任意の $\varepsilon>0$ に対して

$$
\mu(E)<\varepsilon,\qquad
f_n\to f\quad X\setminus E\text{ 上で一様収束}
$$

となる $E$ を取れる.

a.e. 収束と一様収束の間をつなぐ結果として, Lebesgue 積分の収束定理の背景にある見方を与える.

---
layout: end
---

# この章の中心メッセージ

- 各点収束だけでは積分値は制御できない.
- 単調収束定理と優収束定理は, 極限と積分を交換するための代表的な条件を与える.
- Lebesgue 積分論では, a.e. 収束, 単調性, 可積分支配を組み合わせて極限操作を扱う.
