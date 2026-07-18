# 第7章 極限と積分の交換

## 目的

本章では, 極限と積分を交換できるための条件を考える.

函数列が収束しても, 積分値が極限函数の積分へ収束するとは限らない.

![函数列の収束と積分の交換を問う図式](../../figures/measure/static/concepts/integral_commutative_diagram.png)

## この章で考える問題

函数列 $f_n$ が $f$ に収束しているとする. 問題は, 点ごとの収束だけで

$$
\int_X f_n\,d\mu
\longrightarrow
\int_X f\,d\mu
$$

が成り立つかである.

これは

$$
\lim_{n\to\infty}\int f_n\, d\mu
\overset{?}{=}
\int \lim_{n\to\infty} f_n\, d\mu
$$

という, 極限と積分の交換の問題である. 答えは一般には否である. 各点収束に加えて, 函数列の積分量を制御する条件が必要になる.

## 各点収束だけでは積分値は制御できない

$[0,1]$ 上で

$$
f_n(x):=n\mathbf{1}_{(0,1/n]}(x)
$$

とおく.

このとき各 $x\in[0,1]$ に対して

$$
f_n(x)\to 0
$$

であるが,

$$
\int_0^1 f_n(x)\, dx = 1
$$

なので

$$
1=\lim_{n\to\infty}\int_0^1 f_n(x)\, dx
\neq
\int_0^1 \lim_{n\to\infty} f_n(x)\, dx
=0
$$

である.

![各点収束だけでは積分を制御できない](../../figures/measure/animations/pointwise_not_enough/gif/pointwise_not_enough.gif)

この例では, 台 $(0,1/n]$ は縮んでいくが, 高さ $n$ が大きくなるため, 面積は常に $1$ のままである. 各点収束だけでは, 質量が狭い領域に集中する現象を見抜けない.

この失敗は Riemann 積分でも Lebesgue 積分でも共通である. Lebesgue 積分の収束定理は, まさにこの種の質量集中を防ぐ条件を与えるものだと見てよい.

## Riemann 積分での古典的な十分条件

Riemann 積分においては, 一様収束が古典的な安全条件になっている.

### 一様収束なら安全である

有界閉区間 $[a,b]$ 上の Riemann 積分可能函数列 $f_n$ が函数 $f$ に一様収束するとする. このとき $f$ も Riemann 積分可能であり, Riemann 積分でも, 一様収束のもとでは極限と積分を交換できる.

![一様収束のもとで Riemann 積分と極限を交換できる図式](../../figures/measure/static/concepts/integral_commutative_diagram_uniform_riemann.png)

![一様収束で函数列が同じ epsilon 帯に入る様子](../../figures/measure/animations/uniform_convergence_band/gif/uniform_convergence_band.gif)

実際,

$$
\left|
\int_a^b f_n(x)\, dx
-
\int_a^b f(x)\, dx
\right|
\leq
\int_a^b |f_n-f|
\leq
(b-a)\|f_n-f\|_\infty
\to 0
$$

である.

したがって, Riemann 積分における基本的な十分条件は

$$
\boxed{
\text{Riemann 可積分函数列の一様極限は再び Riemann 可積分であり, 積分も収束する}
}
$$

という形になる. 問題は, より弱い収束条件のもとで交換を正当化できるかである.

## Lebesgue 積分での見取り図

Lebesgue 可積分とは通常

$$
\int_X |f|\, d\mu < \infty
$$

を意味する.

Lebesgue 積分では, 各点収束だけでなく, 函数列の積分量が集中したり逃げたりしないことを保証する条件を加える.

ここで現れる代表的な状況をまとめると, 次のようになる.

| 条件 | 極限 $f$ の可積分性 | 積分と極限の交換 |
| --- | --- | --- |
| a.e. 収束だけ | 一般には保証されない | 一般には保証されない |
| 非負 + $\sup_n\int f_n\, d\mu<\infty$ | 保証される | 一般には保証されない |
| 非負単調増加 $f_n\nearrow f$ | $\sup_n\int f_n<\infty$ なら保証される | 成り立つ |
| a.e. 収束 + 可積分支配函数 $|f_n|\le g\in L^1$ | 保証される | 成り立つ |
| $L^1$ 収束 | 保証される | 成り立つ |

以下では, それぞれの定理がこの表のどこに対応するかを見る.

## 単調収束定理

非負可測函数列 $f_n$ が

$$
0\leq f_1\leq f_2\leq \cdots,
\qquad
f_n\nearrow f
$$

を満たすとする. このとき

$$
\int_X f_n\, d\mu
\nearrow
\int_X f\, d\mu
$$

が成り立つ.

これを単調収束定理という.

単調収束定理は, 極限と積分を交換できる最初の代表的条件である. ただし, 右辺は $+\infty$ でもよい.

したがって

$$
\boxed{
f\in L^1
\iff
\sup_n \int_X f_n\, d\mu < \infty
}
$$

である.

![単調増加する領域上の積分](../../figures/measure/animations/integral_on_subset_monotone_limit_2d/gif/integral_on_subset_monotone_limit_2d.gif)

例えば $(0,1]$ 上で

$$
f_n(x)=\frac{1}{x}\mathbf{1}_{[1/n,1]}(x)
$$

とすると, 各 $f_n$ は可積分であり,

$$
f_n(x)\nearrow \frac{1}{x}
$$

である. しかし

$$
\int_0^1 f_n(x)\, dx = \log n \to \infty
$$

なので, 極限函数 $1/x$ は Lebesgue 可積分ではない.

この例は, 各 $f_n$ が可積分であっても, 極限函数の可積分性は自動ではなく, 積分値の有界性が別途必要であることを示している.

## Fatou の補題

非負可測函数列 $f_n\ge 0$ に対して

$$
\int_X \liminf_{n\to\infty} f_n\, d\mu
\leq
\liminf_{n\to\infty}\int_X f_n\, d\mu
$$

が成り立つ.

これを Fatou の補題という.

Fatou の補題は, 完全な交換ではなく一方向の評価を与える定理である.

特に, $f_n\to f$ a.e.（ほとんど至る所）で

$$
\sup_n \int_X f_n\, d\mu < \infty
$$

なら,

$$
\int_X f\, d\mu
\leq
\liminf_{n\to\infty}\int_X f_n\, d\mu
<
\infty
$$

となるので, 極限 $f$ は可積分である.

ただし, 積分値の収束までは保証しない. 先ほどの例

$$
f_n(x):=n\mathbf{1}_{(0,1/n]}(x)
$$

では

$$
f_n\to 0,
\qquad
\int_0^1 f_n\, d\mu = 1
$$

であるから, 極限函数 $0$ は可積分だが, 積分値は $0$ に収束しない.

## 優収束定理

可測函数列 $f_n$ が

$$
f_n\to f\quad \mu\text{-a.e.}
$$

を満たし, さらにある $g\in L^1(\mu)$ が存在して

$$
|f_n|\leq g\quad \mu\text{-a.e.}
$$

がすべての $n$ について成り立つとする.

このとき $f\in L^1(\mu)$ であり, 可積分函数による支配のもとでは, 極限と積分を交換できる.

![優収束定理により極限と積分を交換できる図式](../../figures/measure/static/concepts/integral_commutative_diagram_dominated_convergence.png)

さらに実際には

$$
\int_X |f_n-f|\, d\mu \to 0
$$

も従う.

これを優収束定理という.

優収束定理は,

$$
\boxed{
\text{a.e. 収束}
+
\text{共通の可積分な支配函数}
\Longrightarrow
\text{極限と積分の交換}
}
$$

という形で, 極限と積分の交換を正当化する.

支配函数 $g$ は, 函数列の質量が狭い領域に集中したり, 高さだけが大きくなったりすることを防ぐ役割を持つ.

スパイク列

$$
f_n(x):=n\mathbf{1}_{(0,1/n]}(x)
$$

では, 各点では $0$ に収束するが, 可積分な支配函数 $g$ は存在しない. したがって優収束定理の仮定を満たさない.

## $L^1$ 収束

可測函数列 $f_n$ と可測函数 $f$ について

$$
\int_X |f_n-f|\, d\mu \to 0
$$

が成り立つとき, $f_n$ は $f$ に $L^1$ 収束するという.

$L^1$ 収束は, 積分との整合性という意味で最も直接的な収束概念である. 実際,

$$
\left|
\int_X f_n\, d\mu
-
\int_X f\, d\mu
\right|
\leq
\int_X |f_n-f|\, d\mu
\to 0
$$

であるから, 積分値の収束は直ちに従う.

また, $f_n\in L^1$ で $f_n\to f$ が $L^1$ 収束なら, 極限 $f$ も $L^1$ に属する.

## 一様収束との関係

Riemann 積分では一様収束が基本的な十分条件だった. Lebesgue 積分でも, 測度空間が有限測度なら一様収束はやはり十分条件である.

実際, $\mu(X)<\infty$ で, 各 $f_n\in L^1(\mu)$ が $f$ に一様収束するなら

$$
\int_X |f_n-f|\, d\mu
\leq
\mu(X)\|f_n-f\|_\infty
\to 0
$$

であるから, $f_n\to f$ は $L^1$ 収束であり, 特に

$$
f\in L^1,
\qquad
\int_X f_n\, d\mu \to \int_X f\, d\mu
$$

が成り立つ.

一方, $\mu(X)=\infty$ では一様収束だけでは不十分である. 例えば $\mathbb{R}$ 上で

$$
f_n(x)=\frac{1}{n}\mathbf{1}_{[0,n]}(x)
$$

とすると,

$$
\|f_n\|_\infty=\frac{1}{n}\to 0
$$

なので $f_n\to 0$ は一様収束するが,

$$
\int_{\mathbb{R}} f_n(x)\, d\mu(x)=1
$$

であり, 積分は $0$ に収束しない.

したがって, Lebesgue 積分では一様収束そのものより, 空間の測度や質量の分布まで含めて見る必要がある.

## Egorov の定理との関係

有限測度空間では, a.e. 収束する函数列は, 任意に小さな測度の集合を除けば一様収束する. これが Egorov の定理である.

しかし, それだけでは積分の収束は出ない.

スパイク列

$$
f_n(x):=n\mathbf{1}_{(0,1/n]}
$$

は, 例えば $(0,1/n]$ を除けば恒等的に $0$ であり, 小さい集合を除いた一様収束は見えている. それでもその小さい集合上に積分量 $1$ が集中しているため,

$$
\int_0^1 f_n\, d\mu \not\to 0
$$

である.

したがって,

$$
\boxed{
\text{集合の測度が小さい}
\not\Rightarrow
\text{その上での積分が小さい}
}
$$

のであり, 積分の収束には優収束や $L^1$ 収束のような, 量そのものを制御する条件が必要である.

## この章のまとめ

- 函数列が収束しても, 一般には極限と積分を交換できない.
- Riemann 積分でも, 一様収束のもとでは交換できる.
- Lebesgue 積分では, 単調性や可積分函数による支配など, より柔軟な条件によって交換を正当化できる.
- 単調収束定理, Fatou の補題, 優収束定理は, 極限操作に対する積分の振る舞いを段階的に制御する.

本章の要点は

$$
\boxed{
\text{極限と積分の交換を, 条件ごとに見極める}
}
$$

ということである.
