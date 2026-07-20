---
layout: section
---

# 第0章 導入：Riemann 積分から Lebesgue 積分へ

Riemann 積分の限界から測度論へ進む動機を見る

---
layout: default
---

# 目的

本発表の流れは, まず集合に"大きさ"を与える理論を整え, そのうえで函数を積分し, 最後に極限操作との整合性を扱うことである.

$$
\text{集合の"大きさ"}
\quad\longrightarrow\quad
\text{函数の積分}
\quad\longrightarrow\quad
\text{極限操作との整合性}
$$

Riemann 積分ではどこに限界があるのかを具体的に確認し, Lebesgue 積分と測度論が必要になる問題意識を明確にする.

---
layout: two-cols
---

# Riemann 積分の考え方

Riemann 積分では, 定義域 $[a,b]$ を

$$
\Delta:a=x_0<x_1<\cdots<x_n=b
$$

のように分割し, 小区間 $\Delta_i=[x_{i-1},x_i]$ の幅と代表値 $f(\xi_i)$ から Riemann 和を作り, その極限として積分を考える.

$$
\int_a^b f(x)\,dx
=
\lim_{\|\Delta\|\to0}\sum_{i=1}^n f(\xi_i)(x_i-x_{i-1})
$$

::right::

![Riemann 積分で中央の短冊と代表点を見る図](../figures/measure/static/riemann_local_tagged_partition.png)

---
layout: two-cols
---

# Lebesgue 積分の考え方

Lebesgue 積分では, まず値域 $[\alpha,\beta]$ を

$$
\Theta:\alpha=y_1<y_2<\cdots<y_{m+1}=\beta
$$

のように分割する. 値域区間を

$$
\Theta_k:=[y_k,y_{k+1})
$$

とおき, その逆像

$$
E_k:=f^{-1}(\Theta_k)
=\{x\in[a,b]\mid y_k\le f(x)<y_{k+1}\}
$$

を考え, その"大きさ" $\mu(E_k)$ と区間の代表値 $y_k$ の積の和分の極限として積分を考える.

$$
\int_a^b f(x)\,dx
=
\lim_{\|\Theta\|\to0}\sum_k y_k\mu(E_k)
$$

::right::

![Lebesgue 積分で値域の一層と逆像区間を見る図](../figures/measure/static/lebesgue_local_value_band.png)

---
layout: two-cols
---

# Riemann 積分と Lebesgue 積分の比較

| 観点 | Riemann | Lebesgue |
| --- | --- | --- |
| 分割対象 | 定義域 | 値域 |
| 各項 | $f(\xi_i)\|\Delta_i\|$ | $y_k\mu(E_k)$ |
| 集める情報 | 小区間の代表値 | 各層に入る点集合の大きさ |
| 極限 | $\|\Delta\|\to0$ | $\|\Theta\|\to0$ |
| 表現 | 「縦に切る」 | 「横に切る」 |

::right::

![Riemann 和と分割の細分](../figures/measure/animations/riemann_refinement/gif/riemann_refinement.gif)

![Lebesgue 積分の層による近似](../figures/measure/animations/lebesgue_layers/gif/lebesgue_layers.gif)

---
layout: two-cols
---

# Riemann 積分可能性

Riemann 積分可能性は, 上 Darboux 和と下 Darboux 和で記述できる.

$$
M_i:=\sup_{x\in[x_{i-1},x_i]}f(x),\qquad
m_i:=\inf_{x\in[x_{i-1},x_i]}f(x)
$$

$$
S^*(f,\Delta):=\sum_i M_i|\Delta_i|,
\quad
S_*(f,\Delta):=\sum_i m_i|\Delta_i|
$$

$f$ が Riemann 積分可能であるとは, 任意の $\varepsilon>0$ に対して, ある (十分細かな) 分割 $\Delta$ が存在して

$$
S^*(f,\Delta)-S_*(f,\Delta)<\varepsilon
$$

となることである.


::right::

![Darboux 和の局所拡大](../figures/measure/animations/darboux_local_zoom/gif/darboux_local_zoom.gif)

![Darboux 和の収束](../figures/measure/animations/riemann_area_convergence/gif/riemann_area_convergence.gif)

---
layout: two-cols
---

# Dirichlet 函数が示す限界

Dirichlet 函数

$$
D(x):=\mathbf{1}_{\mathbb{Q}\cap[0,1]}(x) = \begin{cases}
1 & (x\in\mathbb{Q}\cap[0,1]), \\
0 & (x\notin\mathbb{Q}\cap[0,1])
\end{cases}
$$

では, 任意の小区間に有理数と無理数が入る.

したがって各小区間で

$$
\sup D=1,\qquad \inf D=0
$$

であり, どの分割 $\Delta$ を取っても

$$
S^*(D,\Delta)=1,\qquad S_*(D,\Delta)=0
$$

となり, 上和と下和の差は小さくならない.

::right::

![Dirichlet 函数の Darboux 和](../figures/measure/animations/dirichlet_darboux_local_zoom/gif/dirichlet_darboux_local_zoom.gif)

---
layout: default
---

# 「ほとんど至る所」0 という見方

Dirichlet 函数は Riemann 積分可能ではないが, 値 $1$ を取るのは

$$
\mathbb{Q}\cap[0,1]
$$

の上だけであり, それ以外のほとんどの領域では $0$ を取る.

この直観は

$$
D(x)=0 \quad (\text{ほとんど至る所で})
$$

という形で表したい.

すなわち, $0$ と異なる値を取る点の集合の"大きさ"が $0$ である, という意味である.

$$
\int_0^1 D(x)\,dx
=
1\cdot(\text{値 }1\text{ を取る部分の"大きさ"})
+
0\cdot(\text{値 }0\text{ を取る部分の"大きさ"})
=0
$$

---
layout: two-rows
---

# 測度論はなぜ必要か

Lebesgue 積分では, 値域ごとの逆像として集合が自然に現れる.

$$
E_k:=\{x\in[a,b]\mid f(x)\in\Theta_k\}
$$

そのため, 区間や図形だけでなく, より一般の集合にも破綻なく"大きさ"を与える必要がある.

このような集合の"大きさ"を扱う理論が測度論であり, Lebesgue 積分はその上に構成される.

::right::

![Lebesgue 積分で値域の一層と逆像区間を見る図](../figures/measure/static/lebesgue_local_value_band.png)

---
layout: two-rows
---

# 積分の収束

函数列 $f_n$ が函数 $f$ に収束するとき, 積分と極限の順序を交換できるかどうかが問題になる.

$$
f_n \to f \quad
\overset{?}{\Rightarrow}\quad
\int_X f_n d\mu \to \int_X f d\mu
$$

Riemann 積分では, たとえば一様収束なら交換できるが, これは強い条件である.

Lebesgue 積分論では, 単調収束定理や優収束定理により, 一様収束より広い状況でこの交換が可能になる.

::figure::

![函数列の収束と積分の関係を表す可換図式](../figures/measure/static/concepts/integral_commutative_diagram.png)

---
layout: two-rows
---

# 函数列の極限として見る

有理数を $q_1,q_2,\ldots \in \mathbb{Q}\cap[0,1]$ と並べ,

$$
g_n(x):=
\begin{cases}
1 & x\in\{q_1,\ldots,q_n\} \subset \mathbb{Q}\cap[0,1],\\
0 & \text{otherwise}
\end{cases}
$$

とおくと, 各 $g_n$ は Riemann 積分可能であるが, $g_n$ の単調増加極限は Dirichlet 函数 $D$ になり, Riemann 積分可能性は単調増加極限に対して閉じていないことがわかる. 一方, Lebesgue 積分では単調収束定理で扱える.

::right::

![Dirichlet 函数の極限近似](../figures/measure/animations/dirichlet_function_limit_top/gif/dirichlet_function_limit_top.gif)

---
layout: default
---

# Fourier 解析への接続

Fourier 解析では, 例えば

$$
\hat f(\xi):=\int_{\mathbb{R}} f(x)e^{-2\pi i x\xi}\,dx
$$

のような積分が現れる.

函数を点ごとに見るだけではなく, 測度・積分・極限を組み合わせて扱う枠組みが必要になる.

---
layout: end
---

# この章の中心メッセージ

- Riemann 積分は小区間での振動を制御する理論であり, 零集合上の変更や各点極限には弱い.
- Lebesgue 積分では, 値を取る点集合の"大きさ"を測ることで Dirichlet 函数のような例を扱える.
- 以後は測度, 可測函数, Lebesgue 積分, 収束定理の順に枠組みを作る.
