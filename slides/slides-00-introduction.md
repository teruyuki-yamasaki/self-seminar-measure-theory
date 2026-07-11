---
layout: section
---

# 0. 導入

Riemann 積分から Lebesgue 積分への動機

---
layout: two-cols
---

# この章の目的

- Riemann 積分ではどこに限界があるかを確認する
- Lebesgue 積分がどんな見方の転換かを先に掴む
- 測度論と収束定理が必要になる理由を見通す

$$
\text{集合の大きさ}
\;\longrightarrow\;
\text{函数の積分}
\;\longrightarrow\;
\text{極限操作との整合性}
$$

::right::

<img class="slide-figure" src="../figures/measure/animations/riemann_refinement/gif/riemann_refinement.gif" alt="Riemann 和と分割の細分" />

---
layout: two-cols
---

# Riemann と Lebesgue の対比

| 観点 | Riemann 積分 | Lebesgue 積分 |
| --- | --- | --- |
| 分割するもの | 定義域の分割 $\Delta$ | 値域の分割 $\Theta$ |
| 各項 | $f(\xi_i)|\Delta_i|$ | $y_k\mu(E_k)$ |
| 集める情報 | 小区間での代表値 | 値域ごとの逆像の大きさ |
| 極限 | $\|\Delta\|\to0$ | $\|\Theta\|\to0$ |

Lebesgue 積分では, 小区間内の振動そのものよりも,
各値域に入る点全体の集合の大きさを見る.

::right::

<img class="slide-figure" src="../figures/measure/animations/lebesgue_layers/gif/lebesgue_layers.gif" alt="Lebesgue 積分の層による近似" />

---
layout: two-cols
---

# 測度論はなぜ要るか

Lebesgue 積分で基本になるのは

$$
E_k=f^{-1}(\Theta_k)
$$

のような逆像集合の大きさである.

区間なら長さ, 平面図形なら面積, 立体なら体積として理解できるが,
Lebesgue 積分ではもっと複雑な集合にも
破綻なく大きさを与える必要がある.

この「集合に大きさを割り当てる」理論が測度論である.

::right::

<img class="slide-figure" src="../figures/measure/static/concepts/measure_space_examples.png" alt="集合の大きさを扱う測度の概念図" />

---
layout: two-cols
---

# Riemann 積分可能性

Riemann 積分可能性は上 Darboux 和と下 Darboux 和で記述される.

$$
\overline{\mathcal{S}}(f,\Delta)=\sum_i M_i(x_i-x_{i-1}),
\qquad
\underline{\mathcal{S}}(f,\Delta)=\sum_i m_i(x_i-x_{i-1})
$$

分割を細かくしたとき

$$
\overline{\mathcal{S}}(f,\Delta)-\underline{\mathcal{S}}(f,\Delta)\to 0
$$

となることが必要である.

::right::

<img class="slide-figure" src="../figures/measure/animations/riemann_area_convergence/gif/riemann_area_convergence.gif" alt="Darboux 和の収束" />

---
layout: two-cols
---

# Dirichlet 函数が示す限界

$$
D(x)=\mathbf{1}_{\mathbb{Q}\cap[0,1]}(x)
$$

任意の小区間には有理数も無理数も含まれるので

$$
\sup D=1,\qquad \inf D=0
$$

であり, どの分割でも上和と下和は一致しない.

一方で, 値 1 を取るのは可算集合の上だけなので,
「ほとんど至る所 0」と見たい函数でもある.

::right::

<img class="slide-figure" src="../figures/measure/animations/dirichlet_function_limit_top/gif/dirichlet_function_limit_top.gif" alt="Dirichlet 函数の極限近似" />

---
layout: two-cols
---

# 高周波化する函数列

高周波成分を多く含む函数列では,
各小区間の中の振動はどれほど分割を細かくしても残りうる.

そのため Riemann 積分のように
「小区間ごとの振る舞い」を見る見方は不安定になりうる.

Lebesgue 積分では,
各値域に入る点全体の集合の大きさを見ることで,
より安定に面積を捉える見通しが立つ.

::right::

<img class="slide-figure" src="../figures/measure/animations/dirichlet_function_limit_top/gif/dirichlet_function_limit_top.gif" alt="高周波化する函数列の例としての Dirichlet 近似" />

---

# この章の結論

::example-box{title="中心メッセージ"}
Riemann 積分の限界は, 可算集合や零集合の上の振る舞い,
そして極限操作との整合性を十分に扱えないところにある.

Lebesgue 積分へ進むには, まず集合に大きさを与える測度論を整え,
そのうえで函数の積分と収束定理を構成する必要がある.
::

本編の到達点は, 極限と積分の交換を保証する優収束定理である.

---
