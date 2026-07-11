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

## Riemann 積分と Lebesgue 積分の考え方

Riemann 積分と Lebesgue 積分の違いは, 何を分割して足し合わせるかにある.

**Riemann 積分**では, 定義域 $[a,b]$ を分割

$$
\Delta : a=x_0<x_1<\cdots<x_n=b
$$

のように分割し, 各区間 $\Delta_i:=[x_{i-1},x_i]$ の幅


$$
|\Delta_i|:=|x_i-x_{i-1}|
$$

とおく.

にその区間での函数値の代表値 $f(\xi_i)$ をかけて

$$
\sum_{i=1}^n f(\xi_i) |\Delta_i|
$$

を作り, その極限として積分を考える.

ここで $\|\Delta\|:=\max_i |\Delta_i|$ とすれば, 分割を細かくするとは $\|\Delta\|\to0$ とみなせる.

これに対して **Lebesgue 積分**では, まず値域 $[\alpha,\beta]$ を分割

$$
\Theta : \alpha=y_1<y_2<\cdots<y_m<y_{m+1}=\beta
$$

のように分割し, 各区間

$$
\Theta_k:=[y_k,y_{k+1})
$$

の幅

$$
|\Theta_k|:=|y_{k+1}-y_k|
$$

とおく.

に対して, その逆像

$$
E_k:=f^{-1}(\Theta_k)=\{x\in[a,b]\mid f(x)\in \Theta_k\}
$$

を考える. そして, 各値域区間の下限 $y_k$ と, その値を与える点全体の集合 $E_k$ の"大きさ" $\mu(E_k)$ を用いて

$$
\sum_k y_k\mu(E_k)
$$

のような和を作り, 値域分割を細かくした極限として積分を考える.

ここで $\|\Theta\|:=\max_k |\Theta_k|$ とすれば, 値域分割を細かくするとは $\|\Theta\|\to0$ とみなせる.

この違いをまとめると次のようになる.

| 観点 | Riemann 積分 | Lebesgue 積分 |
| --- | --- | --- |
| 分割するもの | 定義域の分割 $\Delta: a=x_0<\cdots<x_n=b$ | 値域の分割 $\Theta: \alpha=y_1<\cdots<y_{m+1}=\beta$ |
| 各項 | $f(\xi_i)\|\Delta_i\|$ | $y_k\mu(E_k)$ |
| 集める情報 | 各小区間 $\Delta_i$ での代表値 $f(\xi_i)$ | 各値域区間 $\Theta_k$ に入る点の集合 $E_k$ の"大きさ" $\mu(E_k)$ |
| 極限 | $\|\Delta\|\to0$ | $\|\Theta\|\to0$ |
| イメージ | ![Riemann 和と分割の細分](../../figures/measure/animations/riemann_refinement/gif/riemann_refinement.gif) | ![Lebesgue 積分の層による近似](../../figures/measure/animations/lebesgue_layers/gif/lebesgue_layers.gif) |

この Lebesgue 積分の見方の利点は, 後で見るような高周波成分を多く含む函数列に対しても, Riemann 積分のように各小区間の中の振動そのものを見るのではなく, 各値域に入る点全体の集合がどれだけの大きさを持つかを見ることで, 面積をより安定に捉えられる見通しが立つことである.

このように, Lebesgue 積分では値域の各層に対応する逆像の集合の"大きさ"が基本になる. したがってその背後では, 定義域の側に現れる集合の"大きさ"を安定に扱う理論が必要になる.


## 測度論はなぜ必要か

ここでいう集合の"大きさ"とは, 区間の長さ, 平面図形の面積, 立体の体積を一般化したものである.

このように, 集合に対して"大きさ"を割り当てる概念を**測度 (measure)** という. Lebesgue 積分では, 値域ごとの逆像として複雑な集合が現れるため, それらにも破綻なく"大きさ"を与える必要がある.

このような「集合の"大きさ"」を扱う理論が**測度論**であり, Lebesgue 積分はその上に構成される.

## Riemann 積分可能性

ここまでで, Riemann 積分と Lebesgue 積分の見取り図を置いた. そのうえで, まず Riemann 積分可能性がどのように記述されるかを確認する.

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

### Riemann 積分の立場で何が起こるか

$[0,1]$ 上の函数

$$
D(x):=\mathbf{1}_{\mathbb{Q}\cap[0,1]}(x) = \begin{cases}
1 & (x\in\mathbb{Q}\cap[0,1]), \\
0 & (x\notin\mathbb{Q}\cap[0,1])
\end{cases}
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

となり, 上和と下和の差は限りなく小さくはならない. よって $D$ は Riemann 積分可能ではない.

### 「ほとんど至る所」0 という見方

しかし, 直観的にはこの函数は **(無限小領域を除いて)「ほとんど至る所」(almost everywhere, a.e.) 0** と見たい. 

$$
D(x)=0 \quad \text{a.e. } x \in[0,1]
$$

実際, 値 1 を取るのは可算集合 $\mathbb{Q}\cap[0,1]$ の上だけであり, それ以外のほとんどの領域 $\mathbb{Q}^c \cap [0,1]$ では値 0 を取るから,

$$
\int_0^1 D(x)\ dx= \int_{\mathbb{Q}\cap[0,1]} 1\ dx + \int_{\mathbb{Q}^c\cap[0,1]} 0\ dx = (無限小領域上での1 \text{の積分}) + (0 \text{の積分}) = 0 + 0 = 0
$$

と考えたいところである.

したがって, Riemann 積分の立場からは「ほとんど至る所」での振る舞いを十分に捉えられないことがわかる.

### 高周波化する函数列と Riemann 積分の限界

この様相を具体的に見やすくするために, 函数列の極限という観点から各 $n\in\mathbb{N}$ に対して

$$
g_n(x)
:=
\lim_{k\to\infty}\cos^{2k}(n!\pi x)
\quad (x\in\mathbb{R})
$$

とおく. 

$$
\lim_{k\to\infty}\cos^{2k}(n!\pi x)
=
\begin{cases}
1 & (n! x \in \mathbb{Z}), \\
0 & (n! x \notin \mathbb{Z})
\end{cases}
$$

であるから, 

$$
G_n :={\{x\in[0,1]\mid n!x\in\mathbb{Z}\}}=\{0,1/n!,2/n!,\ldots,(n-1)!/n!,1\}
$$
とおくと, 各 $g_n$ は有限集合 $G_n$ の定義函数

$$
g_n(x)=\mathbf{1}_{G_n}(x)=\mathbf{1}_{\{0,1/n!,2/n!,\ldots,1\}}(x)
$$

となる. したがって, $g_n$ が 値 1 を取る点は離散的な有限個の点だけである.

一方, $x\in\mathbb{Q}\cap[0,1]$ ならば十分大きい $n$ で $n!x\in\mathbb{Z}$ となるから $g_n(x)\to1$ であり, $x\notin\mathbb{Q}$ ならばどの $n$ についても $n!x\notin\mathbb{Z}$ なので $g_n(x)=0$ である. したがって, **各点 $x\in[0,1]$ について $g_n(x)$ の極限は Dirichlet 函数 $D(x)$ に収束する**:

$$
g_n(x)\to D(x)
\qquad (x\in[0,1])
$$


![Dirichlet 函数の極限近似](../../figures/measure/animations/dirichlet_function_limit_top/gif/dirichlet_function_limit_top.gif)

この函数列を見ると, どれほど細かい分割 $\Delta$ を取っても, 十分大きい $n$ に対して各小区間の中に $g_n=1$ となる点と $g_n=0$ となる点が共存してしまう様子がよくわかる.

したがって, 極限的に見ると, **どんなに細かい分割でも小区間内の振動は消えない**. この例は, **Riemann 的な有限分割による近似が, 高周波成分を次々に含む函数列に対して不安定になりうる**ことを示している.

実用的な例として, Fourier 解析では, 

$$
f(x)=\sum_{n=1}^{\infty}a_n\cos(2\pi nx)+b_n\sin(2\pi nx)
$$

のように, 高周波成分を含む函数列を考える場面が自然に現れる. 

そこでは, 周波数が上がるにつれて函数の局所的な振動はますます細かくなり, 固定した有限分割ではその振る舞いを安定に捉えにくくなる.

したがってこの例は, Dirichlet 函数という特異な一例にとどまらず, 有限分割だけに基づく Riemann 積分が一般に, 高周波化する函数列の極限や細かい局所振動をうまく扱えないことを示している.

## 本発表の到達点

Lebesgue 積分を導入しても, 極限と積分が自動に交換できるわけではない. 本編で最終的に目指すのは, どのような条件のもとで

$$
\lim_{n\to\infty}\int f_n\,d\mu
=
\int \lim_{n\to\infty}f_n\,d\mu
$$

が成り立つかを明確にすることである.

その到達点が優収束定理である.

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

この定理は, Lebesgue 積分が適切な仮定のもとで極限操作と整合的に振る舞うことを保証する中心的定理である.

## この章の中心メッセージ

Riemann 積分の限界は, 可算集合や零集合の上の振る舞い, そして極限操作との整合性を十分に扱えないところにある. Lebesgue 積分へ進むには, まず集合に大きさを与える測度論を整え, そのうえで函数の積分と収束定理を構成する必要がある.
