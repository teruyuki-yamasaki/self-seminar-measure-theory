---
layout: section
---

# 第5章 Lebesgue 積分の見通し

定義域を切る積分から, 値を取る集合を見る積分へ

---
layout: two-cols
---

# Riemann 積分の発想

定義域 $[a,b]$ を細かく分割し, 小区間ごとに函数をほぼ定数と見なす.

$$
\sum_i f(\xi_i)\Delta x_i
$$

Darboux 和では小区間ごとの上限・下限を用いて

$$
L(f,P),\qquad U(f,P)
$$

で挟む.

::right::

<img class="slide-figure" src="../figures/measure/animations/riemann_refinement/gif/riemann_refinement.gif" alt="Riemann 和と分割の細分" />

---
layout: two-cols
---

# Darboux 和の意味

Riemann 積分は, 小区間内の函数の振動が積分に影響しない程度に制御できる場合に定義される.

::example-box{title="見る対象"}
Riemann 積分は定義域を有限個の小区間に切り, 各区間内の振動を見る.
::

::right::

<img class="slide-figure" src="../figures/measure/animations/riemann_area_convergence/gif/riemann_area_convergence.gif" alt="Darboux 和の収束" />

---
layout: two-cols
---

# Dirichlet 函数

$$
f(x)=\mathbf{1}_{\mathbb{Q}\cap[0,1]}(x)
$$

任意の小区間で

$$
\sup f=1,\qquad \inf f=0
$$

である.

したがって Riemann 積分では上和と下和が一致しない.

::right::

<img class="slide-figure" src="../figures/measure/animations/dirichlet_function_limit/gif/dirichlet_function_limit.gif" alt="Dirichlet 函数と Lebesgue 積分" />

---
layout: two-cols
---

# Lebesgue 積分の出発点

Lebesgue 積分では, まず可測集合 $E$ の定義函数を考える.

$$
\int \mathbf{1}_E\,d\mu=\mu(E)
$$

次に単函数

$$
\varphi=\sum_{k=1}^{n}a_k\mathbf{1}_{E_k}
$$

に対して

$$
\int \varphi\,d\mu
=
\sum_{k=1}^{n}a_k\mu(E_k)
$$

と定める.

::right::

<img class="slide-figure" src="../figures/measure/static/concepts/simple_function_algebra.png" alt="単函数の積分を有限和として見る概念図" />

---
layout: two-cols
---

# 値を取る集合を見る

Riemann 積分は定義域を切る.

Lebesgue 積分は値を取る集合を測る.

::note
これは直観的な説明であり, 厳密には可測集合の定義函数からなる単函数の積分を出発点として構成される.
::

::right::

<img class="slide-figure" src="../figures/measure/animations/lebesgue_layers/gif/lebesgue_layers.gif" alt="Lebesgue 積分の層による近似" />

---

# 第5章の結論

::example-box{title="中心メッセージ"}
Riemann 積分は定義域の有限分割に基づき, 小区間内の振動に敏感である.

Lebesgue 積分は可測集合の定義函数と単函数を基礎にし, 測度 0 の集合を自然に無視する.
::

この違いが, 可測函数, 単函数, 収束定理へ進む動機になる.

---
