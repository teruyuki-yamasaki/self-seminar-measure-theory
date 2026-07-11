# 第0章 導入：Riemann 積分から Lebesgue 積分へ

## 目的

この章の目的は, Riemann 積分ではどこに限界があるのかを具体的に確認し, Lebesgue 積分と測度論が必要になる問題意識を明確にすることである.

本発表の流れは, 単に新しい積分公式を与えることではない. まず集合に大きさを与える理論を整え, そのうえで函数を積分し, 最後に極限操作との整合性を扱う. したがって全体の見取り図は

$$
\text{集合の大きさ}
\quad\longrightarrow\quad
\text{函数の積分}
\quad\longrightarrow\quad
\text{極限操作との整合性}
$$

である. 導入では, この流れがなぜ必要になるのかを Riemann 積分の立場から見る.

## Riemann 積分の考え方

有界閉区間 $[a, b]$ 上の有界函数 $f$ を考える.

分割

$$
\Delta:\quad a=x_0<x_1<\cdots<x_n=b
$$

を取り, 各小区間 $[x_{i-1}, x_i]$ から代表点 $\xi_i$ を選ぶ. このとき Riemann 和は

$$
\sum_{i=1}^{n}f(\xi_i)(x_i-x_{i-1})
$$

で与えられる.

これは, 定義域を有限個の小区間に分け, 各小区間上で函数をほぼ定数とみなして面積を近似する方法である.

![Riemann 和と分割の細分](../../figures/measure/animations/riemann_refinement/gif/riemann_refinement.gif)

Riemann 積分では, 分割を細かくすることで近似を改善していく.

## Darboux 和

Riemann 積分可能性は, 上 Darboux 和と下 Darboux 和で記述できる.

分割 $\Delta$ に対して

$$
M_i=\sup\{f(x)\mid x\in[x_{i-1},x_i]\},
$$

$$
m_i=\inf\{f(x)\mid x\in[x_{i-1},x_i]\}
$$

とおく.

上 Darboux 和と下 Darboux 和を

$$
\overline{\mathcal{S}}(f,\Delta)=\sum_{i=1}^{n}M_i(x_i-x_{i-1}),
$$

$$
\underline{\mathcal{S}}(f,\Delta)=\sum_{i=1}^{n}m_i(x_i-x_{i-1})
$$

で定める.

$f$ が Riemann 積分可能であるとは, 任意の $\varepsilon>0$ に対して, 分割を十分細かく取れば

$$
\overline{\mathcal{S}}(f,\Delta)-\underline{\mathcal{S}}(f,\Delta)<\varepsilon
$$

となることである.

このとき, Riemann 積分は
$$
\int_a^b f(x)\,dx=\lim_{\|\Delta\|\to 0}\sum_{i=1}^{n}f(\xi_i)(x_i-x_{i-1})=\lim_{\|\Delta\|\to 0}\overline{\mathcal{S}}(f,\Delta)=\lim_{\|\Delta\|\to 0}\underline{\mathcal{S}}(f,\Delta)
$$
で与えられる.

つまり Riemann 積分では, **小区間ごとの振動が積分に影響しない程度に抑えられる**ことが必要になる.

![Darboux 和の収束](../../figures/measure/animations/riemann_area_convergence/gif/riemann_area_convergence.gif)

## Dirichlet 函数が示す限界

$[0,1]$ 上の函数

$$
D(x)=\mathbf{1}_{\mathbb{Q}\cap[0,1]}(x)
$$

を考える.

任意の小区間には有理数も無理数も含まれるので, どの小区間でも

$$
\sup D=1,\qquad \inf D=0
$$

である.

したがって, どの分割を取っても

$$
\overline{\mathcal{S}}(D,\Delta)=1,\qquad
\underline{\mathcal{S}}(D,\Delta)=0
$$

となり, 上和と下和の差は小さくならない. よって $D$ は Riemann 積分可能ではない.

しかし, 直観的にはこの函数は「ほとんど至る所 0」と見たい. 実際, 値 1 を取るのは可算集合 $\mathbb{Q}\cap[0,1]$ の上だけである.

この点を函数列の極限という観点から見るために, 各 $n\in\mathbb{N}$ に対して

$$
g_n(x)
:=
\lim_{k\to\infty}\cos^{2k}(n!\pi x)
=
\mathbf{1}_{\{x\in[0,1]\mid n!x\in\mathbb{Z}\}}(x)
=
\mathbf{1}_{\{0,1/n!,2/n!,\ldots,1\}}(x)
$$

とおく. 各 $g_n$ は有限集合の定義函数なので, 値 1 を取る点は離散的である.

一方, $x\in\mathbb{Q}\cap[0,1]$ ならば十分大きい $n$ で $n!x\in\mathbb{Z}$ となるから $g_n(x)\to1$ であり, $x\notin\mathbb{Q}$ ならばどの $n$ についても $n!x\notin\mathbb{Z}$ なので $g_n(x)=0$ である. したがって

$$
g_n(x)\to D(x)
\qquad (x\in[0,1])
$$

が成り立つ.

ここで重要なのは, 分割をどれほど細かく取っても, 十分大きい $n$ を選べば各小区間の中に $g_n=1$ となる点と $g_n=0$ となる点が同時に現れることである. 実際, 分割 $\Delta$ の最小幅を $\delta>0$ とすると, $1/n!<\delta$ となるように $n$ を十分大きく取れば, 各小区間には格子点 $\{k/n!\}$ が入り, そこで $g_n=1$ となる. しかしその小区間全体が有限集合になることはないので, 同じ小区間内に $g_n=0$ となる点も存在する.

したがって, 極限的に見ると, どんなに細かい分割でも小区間内の振動は消えない. これは Riemann 的な有限分割による近似が, 高周波成分を次々に含む函数列に対して不安定になりうることを示している.

![Dirichlet 函数の極限近似](../../figures/measure/animations/dirichlet_function_limit_top/gif/dirichlet_function_limit_top.gif)

Fourier 解析でも, 高周波成分が加わるにつれて函数の局所的な振動は細かくなる. そのため, 函数列の極限を考えるときには, 各小区間内の振動そのものだけでなく, どの集合の上でどの程度の大きさを持つかを測度を通して捉える視点が重要になる.

この例は, 有限分割だけに基づく Riemann 積分では, 可算集合や零集合の上の振る舞いだけでなく, 高周波化する函数列の極限をもうまく処理できないことを示している.

## 測度論で扱いたい問題

ここで必要になるのは, 単に「積分の定義を変える」ことではない. 少なくとも次の問題を同時に扱う必要がある.

- 複雑な集合に大きさを与えること
- 可算個の集合の和に対して大きさが安定に振る舞うこと
- 測度 $0$ の集合を自然に扱えること
- 函数列の極限と積分の交換を扱えること

Lebesgue 積分は, こうした要求を満たすために, まず集合に対する大きさの理論として測度論を整えるところから始まる.

## Lebesgue 積分は何を変えるのか

Lebesgue 積分では, 函数をその定義域の有限分割だけで見るのではなく, 函数の値と, その値を取る集合の大きさとを組み合わせて積分を考える.

たとえば可測集合 $E$ の定義函数

$$
\mathbf{1}_E(x)=
\begin{cases}
1 & (x\in E), \\
0 & (x\notin E)
\end{cases}
$$

に対しては,

$$
\int \mathbf{1}_E\,d\mu=\mu(E)
$$

と定めるのが自然である.

さらに, こうした定義函数の有限和から出発して一般の函数へ進む. したがって Lebesgue 積分の背後には, まず集合の大きさを安定に与える測度の理論が必要になる.

![Lebesgue 積分の層による近似](../../figures/measure/animations/lebesgue_layers/gif/lebesgue_layers.gif)

## 点wise 収束だけでは不十分である

Lebesgue 積分のもう一つの重要な動機は, 極限操作との整合性にある.

$[0,1]$ 上で

$$
f_n(x)=n\mathbf{1}_{(0,1/n)}(x)
$$

とおくと, 各点 $x\in[0,1]$ について

$$
f_n(x)\to 0
$$

である.

しかし積分は

$$
\int_0^1 f_n(x)\,d\mu(x)=1
$$

なので,

$$
\lim_{n\to\infty}\int_0^1 f_n\,d\mu
\neq
\int_0^1\lim_{n\to\infty}f_n\,d\mu
$$

となる.

この例は, 点wise 収束だけでは極限と積分を交換できないことを示している. 後に扱う収束定理は, こうした失敗を防ぐ条件を与える.

## 本発表の到達点

本編の到達点は優収束定理である.

可測函数列 $f_n$ が

$$
f_n\to f \quad \mu\text{-a.e.}
$$

を満たし, ある $g\in L^1(\mu)$ によって

$$
|f_n|\leq g \quad \mu\text{-a.e.}
$$

と支配されるならば,

$$
\int f_n\, d\mu\to \int f\, d\mu
$$

が成り立つ.

この定理は, Lebesgue 積分が極限操作と整合的に振る舞うことを示す中心的定理である.

## この章の中心メッセージ

Riemann 積分の限界は, 可算集合や零集合の上の振る舞い, そして極限操作との整合性を十分に扱えないところにある. Lebesgue 積分へ進むには, まず集合に大きさを与える測度論を整え, そのうえで函数の積分と収束定理を構成する必要がある.
