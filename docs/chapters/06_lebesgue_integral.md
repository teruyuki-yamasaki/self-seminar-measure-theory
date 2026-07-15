# 第6章 Lebesgue 積分

## 目的

この章の目的は, 単函数の積分から出発し, 非負可測函数, さらに一般の可積分函数の Lebesgue 積分を定義することである.

Lebesgue 積分は, 次の順に構成される.

1. 非負単函数の積分を定義する.
2. 非負可測函数の積分を, 下から近似する単函数の積分の上限として定義する.
3. 一般の可測函数を正部分と負部分に分けて積分する.

## 非負単函数の積分

測度空間 $(X, \mathfrak{B}, \mu)$ を固定する.

非負単函数

$$
\varphi (x) = \sum_{k=1}^{n}a_k\mathbf{1}_{E_k}(x)
$$

を考える. ここで

$$
a_k\geq0, \qquad E_k\in\mathfrak{B}
$$

であり, $E_1, \ldots, E_n$ は互いに素であるとする.

このとき, $\varphi$ の積分を

$$
\int_X \varphi(x)\, d\mu(x)
:=
\sum_{k=1}^{n}a_k\mu(E_k)
= a_1 \mu(E_1) + \cdots + a_n \mu(E_n)
$$

と定める.

この定義は, 表示の仕方によらない. 異なる単函数表示がある場合でも, 可測集合を共通細分すれば, 同じ値が得られる.

![単函数の積分](../../figures/measure/animations/simple_function_examples_2d/gif/simple_function_examples_2d.gif)

単函数の積分は, 各値とその値を取る可測集合の測度の積を足し合わせることで定義される.

## 非負単函数の基本性質

非負単函数 $\varphi, \psi$ と $c\geq0$ に対して, 次が成り立つ.

### 線形性

$$
\int_X(\varphi+\psi)\, d\mu
=
\int_X\varphi\, d\mu+\int_X\psi\, d\mu
$$

および

$$
\int_X c\varphi\, d\mu
=
c\int_X\varphi\, d\mu
$$

が成り立つ.

### 単調性

$$
0\leq\varphi\leq\psi
$$

ならば

$$
\int_X\varphi\, d\mu
\leq
\int_X\psi\, d\mu
$$

である.

これらの性質は, 測度の有限加法性および単調性から従う.

## 非負可測函数の積分

非負可測函数

$$
f:X\to[0, \infty]
$$

に対して, Lebesgue 積分を

$$
\int_X f(x)\, d\mu(x)
:=
\sup\left\{
\int_X \varphi(x)\, d\mu(x)
\ \middle|\
0\leq\varphi\leq f, \ \varphi\text{ は非負単函数}
\right\}
$$

と定める.

この値は $[0, \infty]$ に属する. つまり, 非負可測函数の積分では値 $\infty$ を許す.

この定義は, 非負可測函数を下から単函数で近似するという考えに基づいている.

![下からの単函数近似](../../figures/measure/animations/monotone_simple_approximation/gif/monotone_simple_approximation.gif)

非負可測函数の積分は, $0\leq\varphi\leq f$ を満たす単函数の積分の上限として定義される.

## 非負可測函数の積分の意味

非負可測函数 $f$ に対して, 単函数 $\varphi$ が

$$
0\leq\varphi\leq f
$$

を満たすとき, $\varphi$ は $f$ の下側近似である.

Lebesgue 積分

$$
\int_X f\, d\mu
$$

は, そのような下側近似の積分の上限である.

したがって, Lebesgue 積分は, 単函数の積分を非負可測函数へ拡張したものである.

![Lebesgue 積分値の収束](../../figures/measure/animations/lebesgue_area_convergence/gif/lebesgue_area_convergence.gif)

値の分割を細かくすると, 下からの単函数近似の積分は極限として非負可測函数の積分に近づく.

## 可測函数の安定性

Lebesgue 積分を一般の函数へ拡張するためには, 可測函数が基本的な演算と極限操作で閉じていることが必要である.

$f, g$ が可測函数であり, $c\in\mathbb{R}$ とする. このとき

$$
f+g, \qquad cf, \qquad fg, \qquad |f|
$$

も可測函数である. また, 可測函数列 $f_n$ に対して

$$
\sup_n f_n, \qquad \inf_n f_n, \qquad
\limsup_{n\to\infty}f_n, \qquad
\liminf_{n\to\infty}f_n
$$

も可測である.

特に, 可測函数列 $f_n$ が各 $x\in X$ で極限を持ち

$$
f(x)=\lim_{n\to\infty}f_n(x)
$$

と定まるならば, $f$ も可測である.

この性質により, 可測函数の範囲は, 正部分・負部分への分解や単函数近似の極限を扱っても保たれる.

## 一般の可測函数の積分

実数値可測函数 $f$ に対して, 正部分と負部分を

$$
f^+=\max\{f, 0\},
$$

$$
f^-=\max\{-f, 0\}
$$

と定める.

このとき

$$
f=f^+-f^-,
\qquad
|f|=f^++f^-
$$

である.

可測函数の安定性より, $f^+$ と $f^-$ は非負可測函数である. したがって, それぞれの積分

$$
\int_X f^+\, d\mu, \qquad
\int_X f^-\, d\mu
$$

は定義される.

少なくとも一方が有限であるとき,

$$
\int_X f\, d\mu
=
\int_X f^+\, d\mu-\int_X f^-\, d\mu
$$

と定める.

特に

$$
\int_X |f|\, d\mu<\infty
$$

であるとき, $f$ は可積分であるという.

この場合,

$$
\int_X f^+\, d\mu<\infty,
\qquad
\int_X f^-\, d\mu<\infty
$$

であり, 積分値は有限の実数である.

## 積分の基本性質

可積分函数 $f, g$ と $a, b\in\mathbb{R}$ に対して,

$$
\int_X(af+bg)\, d\mu
=
a\int_Xf\, d\mu+b\int_Xg\, d\mu
$$

が成り立つ.

また,

$$
f\leq g\quad \mu\text{-a.e.}
$$

ならば

$$
\int_X f\, d\mu
\leq
\int_X g\, d\mu
$$

である.

さらに

$$
\left|\int_X f\, d\mu\right|
\leq
\int_X |f|\, d\mu
$$

が成り立つ.

## Riemann 積分との整合性

Lebesgue 積分は Riemann 積分を置き換えて別の値を与えるものではない. 有界閉区間 $[a, b]$ 上の有界函数 $f$ が Riemann 積分可能ならば, $f$ は Lebesgue 可測であり, Lebesgue 積分可能で,

$$
\int_a^b f(x)\, dx
=
\int_{[a, b]} f\, d\mu
$$

が成り立つ. ここで右辺の $\mu$ は $[a, b]$ 上の Lebesgue 測度である.

この事実は, Riemann 積分の Darboux 和を Lebesgue 積分の言葉で見ると自然である. 区間分割

$$
a=x_0<x_1<\cdots<x_n=b
$$

に対し, 各小区間上の下限と上限を用いて階段函数

$$
s_\Delta(x)=\sum_{i=1}^n m_i\mathbf{1}_{[x_{i-1}, x_i)}(x),
\qquad
t_\Delta(x)=\sum_{i=1}^n M_i\mathbf{1}_{[x_{i-1}, x_i)}(x)
$$

を作ると,

$$
s_\Delta\leq f\leq t_\Delta
$$

であり,

$$
\int s_\Delta\, d\mu
=
\underline{\mathcal{S}}(f,\Delta),
\qquad
\int t_\Delta\, d\mu
=
\overline{\mathcal{S}}(f,\Delta)
$$

である. Riemann 積分可能性は, 分割を細かくすることで上 Darboux 和と下 Darboux 和の差を任意に小さくできることだった. したがって, Lebesgue 積分で見ても $f$ は下からの単函数近似と上からの単函数近似に挟まれ, その積分値は Riemann 積分値と一致する.

ここでは端点の扱いを半開区間で書いたが, 端点全体は有限集合であり Lebesgue 測度 $0$ である. したがって, 端点の値は積分値に影響しない.

この意味で, Lebesgue 積分は Riemann 積分の拡張である. 違いが現れるのは, Riemann 積分では扱いにくい函数や, 函数列の極限を扱う場面である.

## 可積分函数の作るベクトル空間

### 可積分函数全体

可積分な実数値可測函数全体の集合を

$$
V
:=
\left\{
f:X\to\mathbb{R}
\;\middle|\;
f\text{ は可測},\ \int_X|f|\,d\mu<\infty
\right\}
$$

とおく.

上の線形性から, 可積分函数の線形結合も可積分である.
すなわち, $f,g\in V$ と $a,b\in\mathbb{R}$ に対して $af+bg \in V$ である. したがって, $V$ は実数体上のベクトル空間をなす.

### $L^1$ 半ノルムと a.e. 一致

$V$ の各函数 $f$ に対して

$$
\|f\|_1
:=
\int_X |f|\, d\mu
$$

とおく. これは $V$ 上の半ノルムである.

特に, $f,g\in V$ に対して

$$
\|f-g\|_1=0
\quad\Longleftrightarrow\quad
f=g\ \ \mu\text{-a.e.}
$$

が成り立つ.

実際, $f=g$ が $\mu$-a.e. で成り立てば $|f-g|=0$ も $\mu$-a.e. であるから

$$
\|f-g\|_1
=
\int_X |f-g|\, d\mu
=
0
$$

である. 逆に $\|f-g\|_1=0$ ならば, 非負可測函数 $|f-g|$ の積分が $0$ であるから, $|f-g|>0$ となる点の集合は零集合であり, したがって $f=g$ が $\mu$-a.e. で成り立つ.

このように, $V$ の上では a.e. で一致する二つの函数の距離が $0$ になる. したがって, 真のノルム空間を得るためには, そのような函数を同一視するのが自然である.

### 商空間としての $L^1(\mu)$

次に, $V$ の上に

$$
f\sim g
\quad\Longleftrightarrow\quad
f=g\ \ \mu\text{-a.e.}
$$

という関係を入れる. これは同値関係であるから, 各 $f\in V$ に対してその同値類 $[f]$ を考えることができる. さらに, a.e. で等しい函数は積分値を変えないので, 和と実数倍

$$
[f]+[g]:=[f+g],\qquad
c[f]:=[cf]
$$

は同値類の取り方によらずよく定まる. よって, 商空間 $V/{\sim}$ も実数体上のベクトル空間になる.

この商空間を

$$
L^1(\mu)
$$

と書く.

各同値類 $[f]\in L^1(\mu)$ に対して

$$
\|[f]\|_1
:=
\int_X |f|\, d\mu
$$

と定める. これは代表元の取り方によらない. 実際, $f=g$ が $\mu$-a.e. で成り立てば $|f|=|g|$ も $\mu$-a.e. であるから

$$
\int_X |f|\, d\mu
=
\int_X |g|\, d\mu
$$

である.

以後は慣例に従って, 同値類 $[f]$ をその代表元 $f$ と同一視し,

$$
f\in L^1(\mu),\qquad
\|f\|_1=\int_X |f|\, d\mu
$$

と書く.

したがって, 零集合上でのみ値が異なる二つの函数は $L^1(\mu)$ の同じ元を表し, 積分値も一致する.

### $L^p(\mu)$ への一般化

同じ構成は, より一般に $1\leq p<\infty$ に対しても成り立つ.

可測函数 $f$ に対して

$$
\int_X |f|^p\, d\mu<\infty
$$

であるとき, $f$ は $p$ 乗可積分であるという. このような函数全体から出発し, $\mu$-a.e. に等しい函数を同一視して得られる商空間を

$$
L^p(\mu)
$$

と書く.

各同値類に対して

$$
\|f\|_p
:=
\left(\int_X |f|^p\, d\mu\right)^{1/p}
$$

と定めると, これは $L^p(\mu)$ 上のノルムになる.

特に $p=1$ の場合が, ここで扱っている $L^1(\mu)$ である. また, $p=\infty$ の場合には本質的上限

$$
\|f\|_\infty
:=
\operatorname*{ess\,sup}_{x\in X}|f(x)|
$$

を用いて $L^\infty(\mu)$ を定める.

## この章の中心メッセージ

Lebesgue 積分は, 非負単函数の積分を出発点とし, 非負可測函数を下から単函数で近似することで定義される. 一般の函数は正部分と負部分に分けて積分する. 可積分性は $\int |f|\, d\mu<\infty$ によって定義される. また, Riemann 積分可能な函数に対しては Lebesgue 積分は同じ値を与える.
