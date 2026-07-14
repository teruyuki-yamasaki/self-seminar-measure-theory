---
layout: section
---

# 第0章 導入：Riemann 積分から Lebesgue 積分へ

Riemann 積分から Lebesgue 積分への動機

---
layout: two-cols
---

# この章の目的

この章の目的は, Riemann 積分ではどこに限界があるのかを具体的に確認し, Lebesgue 積分と測度論が必要になる問題意識を明確にすることである.

$$
\text{集合の``大きさ''}
\;\longrightarrow\;
\text{函数の積分}
\;\longrightarrow\;
\text{極限操作との整合性}
$$

導入では, この流れがなぜ必要になるのかを Riemann 積分の立場から見る.

---
layout: two-cols
---

# Riemann 積分の考え方

Riemann 積分では, 定義域 $[a,b]$ を

$$
\Delta:a=x_0<x_1<\cdots<x_n=b
$$

のように分割し, 各小区間の幅 $\Delta_i=x_i-x_{i-1}$ と代表値 $f(\xi_i)$ から

$$
\sum_{i=1}^n f(\xi_i)\Delta_i
$$

を作る. 分割を細かくするとは
$$
\Vert\Delta\Vert:=\max_i(\Delta_i)\to0
$$
とみなせる.

::right::

<img class="slide-figure" src="../figures/measure/animations/riemann_refinement/gif/riemann_refinement.gif" alt="Riemann 和と分割の細分" />

---
layout: two-cols
---

# Lebesgue 積分の考え方

Lebesgue 積分では, まず値域 $[\alpha,\beta]$ を

$$
\Theta:\alpha=y_1<y_2<\cdots<y_{m+1}=\beta
$$

のように分割する. 各値域区間 $\Theta_k = [y_k, y_{k+1})$ に対して

$$
E_k=f^{-1}(\Theta_k)
$$

を考え, その集合の"大きさ" $\mu(E_k)$ を用いて

$$
\sum_k y_k\mu(E_k)
$$

のような和を作る.

::right::

<img class="slide-figure" src="../figures/measure/animations/lebesgue_layers/gif/lebesgue_layers.gif" alt="Lebesgue 積分の層による近似" />

---

# 2つの積分の比較

| 観点 | Riemann 積分 | Lebesgue 積分 |
| --- | --- | --- |
| 分割するもの | 定義域の分割 $\Delta:a=x_0<\cdots<x_n=b$ | 値域の分割 $\Theta:\alpha=y_1<\cdots<y_{m+1}=\beta$ |
| 各項 | $f(\xi_i)\lvert\Delta_i\rvert$ | $y_k\mu(E_k)$ |
| 集める情報 | 各小区間 $\Delta_i$ での代表値 $f(\xi_i)$ | 各値域区間 $\Theta_k$ に入る点の集合 $E_k$ の"大きさ" |
| 極限 | $\Vert\Delta\Vert\to0$ | $\Vert\Theta\Vert\to0$ |
| 視点 | 小区間の中での振動が直接問題になる | 函数値ごとに現れる集合の"大きさ"が本質的になる |


重要なのは, **何を分割して足し合わせるか**が異なることである.

---
layout: two-cols
---

# Riemann 積分可能性

Riemann 積分可能性は, 上 Darboux 和と下 Darboux 和で記述できる.

$$
M_i=\sup_{x\in[x_{i-1},x_i]}f(x),
\qquad
m_i=\inf_{x\in[x_{i-1},x_i]}f(x)
$$

$$
S^*(f,\Delta)=\sum_i M_i(x_i-x_{i-1}),
\qquad
S_*(f,\Delta)=\sum_i m_i(x_i-x_{i-1})
$$

任意の $\varepsilon>0$ に対して, ある分割 $\Delta$ が存在して

$$
S^*(f,\Delta)-S_*(f,\Delta)<\varepsilon
$$

となることが必要である.

::right::

<img class="slide-figure" src="../figures/measure/animations/riemann_area_convergence/gif/riemann_area_convergence.gif" alt="Darboux 和の収束" />

---
layout: two-cols
---

# Dirichlet 函数

$[0,1]$ 上の函数

$$
D(x):=\mathbf{1}_{\mathbb{Q}\cap[0,1]}(x)
$$

を考える. 任意の小区間には有理数も無理数も含まれるので, どの小区間でも

$$
\sup D=1,\qquad \inf D=0
$$

である. したがって, どの分割を取っても

$$
S^*(D,\Delta)=1,\qquad S_*(D,\Delta)=0
$$

となり, $D$ は Riemann 積分可能ではない.

::right::

<img class="slide-figure" src="../figures/measure/animations/dirichlet_function_limit_top/gif/dirichlet_function_limit_top.gif" alt="Dirichlet 函数の極限近似" />

---
layout: two-cols
---

# 「ほとんど至る所」0

Dirichlet 函数は Riemann 積分可能ではないが, 値 $1$ を取るのは有理点の集合 $\mathbb{Q}\cap[0,1]$ の上だけである.

後で導入する言葉を少し先取りすれば,

$$
D(x)=0 \quad (\text{ほとんど至る所で})
$$

と表したい. つまり, $0$ と異なる値を取る点の集合の"大きさ"が $0$ である, という意味である.

直観的には

$$
\int_0^1 D(x)\,dx
=1\cdot\mu(\mathbb{Q}\cap[0,1])
+0\cdot\mu(\mathbb{Q}^c\cap[0,1])
=0
$$

と考えたくなる.

::right::

<img class="slide-figure" src="../figures/measure/static/concepts/null_set_ae.png" alt="零集合上を除いて等しい函数を見る概念図" />

---
layout: two-cols
---

# 測度論はなぜ必要か

区間の長さ, 平面図形の面積, 立体の体積といった古典的な``大きさ''を, より複雑な集合にも拡張しなければならない.

一般の集合に対して``大きさ''を割り当てる概念を**測度**という.

Lebesgue 積分では, 値域ごとの逆像

$$
E_k=f^{-1}(\Theta_k)
$$

としてそのような集合が自然に現れる. それらにも破綻なく``大きさ''を与える必要がある.

::right::

<img class="slide-figure" src="../figures/measure/static/concepts/measure_space_examples.png" alt="測度空間の例" />

---
layout: two-cols
---

# 極限と積分の交換

Lebesgue 積分を導入しても, 極限と積分が自動に交換できるわけではない.

$$
\lim_{n\to\infty}\int f_n\,d\mu
\overset{?}{=}
\int \lim_{n\to\infty}f_n\,d\mu
$$

積分を定義できることと, 極限操作と積分が整合的に振る舞うことは別の問題である.

個々の函数だけでなく, **函数列の極限を安定に扱う枠組み**が必要になる.

::right::

::example-box{title="この後の問い"}
この交換は, どのような条件のもとで正当化できるのか.
::

---
layout: two-cols
---

# 函数列の極限として見る

各 $n\in\mathbb{N}$ に対して

$$
G_n=\left\{\frac{j}{n!}\mid j=0,1,\ldots,n!\right\},
\qquad
g_n:=\mathbf{1}_{G_n}
$$

とおく. 各 $G_n$ は有限集合なので, $g_n$ は Riemann 積分可能であり,

$$
\int_0^1 g_n(x)\,dx=0
$$

である.

一方で $0\le g_1\le g_2\le\cdots$ かつ
$g_n(x)\to D(x)$ である. つまり Riemann 可積分函数列の単調増加極限として, Riemann 積分可能でない函数が現れる.

::right::

<img class="slide-figure" src="../figures/measure/animations/dirichlet_function_limit_top/gif/dirichlet_function_limit_top.gif" alt="Dirichlet 函数の極限近似" />

---
layout: two-cols
---

# Fourier 解析への接続

$f\in L^1(\mathbb{R})$ の Fourier 変換は

$$
\widehat{f}(\xi)
=
\int_{\mathbb{R}} f(x)e^{-2\pi i x\xi}\,dx
$$

という Lebesgue 積分で定義される.

さらに $L^1$ 函数の Fourier 変換が連続であることは, 後で見る優収束定理から従う.

::right::

::example-box{title="共通する問題意識"}
函数を点ごとに見るだけではなく, 測度・積分・極限を組み合わせて扱う.
::

---

# この章の結論

::example-box{title="中心メッセージ"}
Riemann 可積分性は, 零集合上の変更に対して安定ではない.

Riemann 可積分函数全体は, 各点収束や単調増加極限に対して閉じていない.

Lebesgue 積分論は, 零集合を無視する枠組みと, 極限と積分の関係を保証する収束定理を与える.
::

Lebesgue 積分へ進むには, まず集合に``大きさ''を与える測度論を整え, そのうえで函数の積分と収束定理を構成する必要がある.

---
