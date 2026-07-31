# 第8章 積分を集合の函数として見る

## 目的

この章の目的は, Lebesgue 積分から自然に生まれる集合函数を調べることである.

これまで, 測度空間

$$
(X,\mathfrak{B},\mu)
$$

上の可測函数 $f: X\to\mathbb{R}$ に対して, 積分

$$
\int_X f(x)\,d\mu(x)
$$

を定義した. ここで視点を少し変える.

可測集合 $E\in\mathfrak{B}$ ごとに

$$
\Phi_f(E):=\int_E f(x)\,d\mu(x)
$$

と定めると, $\Phi_f$ は集合 $E$ を変数とする集合函数になる.

つまり, 第二部で構成した積分から,

$$
\Phi_f:\mathfrak{B}\to\mathbb{R}
$$

という集合函数が生まれる.

第三部では, この具体例から出発し, そこに現れる加法性, 分解, 変動, 絶対連続性を見たあとで, 加法的集合函数の一般論へ進む.

## 非負函数の場合

### 非負函数から測度が生まれる

まず $f:X\to[0,\infty]$ を非負可測函数とする.

可測集合 $E\in\mathfrak{B}$ に対して

$$
\nu_f(E):=\int_E f(x)\,d\mu(x)
$$

と定める. これは

$$
\nu_f(E)=\int_X \mathbf{1}_E(x)f(x)\,d\mu(x)
$$

と書いてもよい.

このとき, $\nu_f$ は $\mathfrak{B}$ 上の測度になる.

実際, 任意の $E\in\mathfrak{B}$ に対して

$$
\nu_f(E)\ge0
$$

であり, **非負性** を満たす.

$$
\nu_f(\emptyset)=\int_\emptyset f(x)\,d\mu(x)=0
$$

である.

また, $A, B\in\mathfrak{B}$ が$A \subset B$ ならば
$$
\nu_f(B)=\nu_f(A)+\nu_f(B-A)\ge\nu_f(A)
$$
であるから, $\nu_f$ は **単調性** を満たす.

さらに, $E_1,E_2,\ldots\in\mathfrak{B}$ が互いに素ならば,

$$
\mathbf{1}_{\sum_{n=1}^{\infty}E_n}(x)f(x)
=
\sum_{n=1}^{\infty}\mathbf{1}_{E_n}(x)f(x)
$$

である. 右辺の部分和は非負可測函数列として単調増加する:

$$
0\le\sum_{n=1}^{N}\mathbf{1}_{E_n}(x)f(x)\nearrow\sum_{n=1}^{\infty}\mathbf{1}_{E_n}(x)f(x)
$$


したがって, 単調収束定理より

$$
\begin{aligned}
\nu_f\left(\sum_{n=1}^{\infty}E_n\right)
&=
\int_X \mathbf{1}_{\sum_{n=1}^{\infty}E_n}(x)f(x)\,d\mu(x) \\
&=
\int_X \sum_{n=1}^{\infty}\mathbf{1}_{E_n}(x)f(x)\,d\mu(x) \\
&=
\sum_{n=1}^{\infty}\int_X \mathbf{1}_{E_n}(x)f(x)\,d\mu(x) \\
&=
\sum_{n=1}^{\infty}\nu_f(E_n).
\end{aligned}
$$

したがって, $\nu_f$ は **可算加法性** を満たす.

ここで重要なのは, 非負函数 $f$ を積分することで新しい測度 $\nu_f$ が得られることである. もとの測度 $\mu$ は集合 $E$ の大きさを直接測った. 一方, $\nu_f$ は $E$ 上の重み $f$ を積分することで, $E$ に新しい大きさを与える.

### 重み付き測度としての意味

$f\ge0$ のとき,

$$
\nu_f(E)=\int_E f(x)\,d\mu(x)
$$

は, $\mu$ に対して重み $f$ を掛けた測度である.

例えば $\mathbb{R}$ 上の Lebesgue 測度 $\lambda$ に対して

$$
\nu_f(E)=\int_E f(x)\,d\lambda(x)
$$

と定めると, $f(x)$ が大きい場所では集合の大きさが強く数えられ, $f(x)$ が小さい場所では弱く数えられる.

特に $f=1$ なら

$$
\nu_f(E)=\lambda(E)
$$

であり, もとの Lebesgue 測度に戻る.

また, $f=\mathbf{1}_A$ なら

$$
\nu_f(E)=\int_E \mathbf{1}_A(x)\,d\mu(x)
=\mu(E\cap A)
$$

となる. これは, 集合 $E$ のうち $A$ に入っている部分だけを測る測度である.

この例は, 測度を変えることが積分の中の重みを変えることとして理解できることを示している.

## 正負を取る函数の場合

次に, $f\in L^1(\mu)$ を実数値可積分函数とする.

同じように

$$
\Phi_f(E):=\int_E f(x)\,d\mu(x)
$$

と定める.

### 測度として何が壊れ, 何が残るか

**非負性は失われる.**

このとき $\Phi_f$ は一般には非負ではない.

$$
\Phi_f:\mathfrak{B}\to\mathbb{R}
$$

例えば $X=[0,1]$, $\mu=\lambda$ (Lebesgue 測度) とし,

$$
f(x)=
\begin{cases}
1 & (0\le x\le 1/2),\\
-1 & (1/2<x\le 1)
\end{cases}
$$

とする.

このとき

$$
A=(1/2,1]
$$

に対して

$$
\Phi_f(A)=\int_A f(x)\,d\lambda(x)=-\frac12
$$

である.

したがって, $\Phi_f$ は非負性を満たさない. この意味で, $\Phi_f$ は測度ではない.

**空集合の値は 0 である.**

一方で, 空集合の値は変わらず 0 である.

$$
\Phi_f(\emptyset)
=
\int_\emptyset f(x)\,d\mu(x)
=
0
$$

**単調性は失われる.**

$f$ が正負を取る場合, $\Phi_f$ は一般に単調ではない.

$$
E, F \in \mathfrak{B} \quad E \subset F
\quad\overset{?}{\Longrightarrow}\quad
\Phi_f(E)\le\Phi_f(F)
$$

上と同じ例で

$$
E=[0,1/2],
\qquad
F=[0,1]
$$

とおけば $E\subset F$ である. しかし,

$$
\Phi_f(E)=\int_E f(x)\,d\lambda(x)=\frac12
$$

である一方,

$$
\Phi_f(F)=\int_F f(x)\,d\lambda(x)=0
$$

である.

したがって

$$
E\subset F
\quad\text{だが}\quad
\Phi_f(E)>\Phi_f(F)
$$

となる.

非負性を失うと, 集合を大きくしても値が大きくなるとは限らない.

**加法性は残る.**

一方で, **加法性** は残る.

第6章で見たように

$$
f=f^+-f^-,
\qquad
f^+\ge0,\quad f^-\ge0
$$

と分解できる. したがって, 任意の $E\in\mathfrak{B}$ に対して

$$
\begin{aligned}
\Phi_f(E)
&=
\int_E f(x)\,d\mu(x) \\
&=
\int_E \left(f^+(x)-f^-(x)\right)\,d\mu(x) \\
&=
\int_E f^+(x)\,d\mu(x)-\int_E f^-(x)\,d\mu(x) \\
&=
\Phi_{f^+}(E)-\Phi_{f^-}(E).
\end{aligned}
$$

ここで $\Phi_{f^+}$ と $\Phi_{f^-}$ は, 非負函数から作られる測度である.

したがって, 互いに素な $E_1,E_2,\ldots\in\mathfrak{B}$ に対して

$$
\begin{aligned}
\Phi_f\left(\sum_{n=1}^{\infty}E_n\right)
&=
\Phi_{f^+}\left(\sum_{n=1}^{\infty}E_n\right)
-
\Phi_{f^-}\left(\sum_{n=1}^{\infty}E_n\right) \\
&=
\sum_{n=1}^{\infty}\Phi_{f^+}(E_n)
-
\sum_{n=1}^{\infty}\Phi_{f^-}(E_n) \\
&=
\sum_{n=1}^{\infty}\left(\Phi_{f^+}(E_n)-\Phi_{f^-}(E_n)\right) \\
&=
\sum_{n=1}^{\infty}\Phi_f(E_n).
\end{aligned}
$$

が成り立つ.

つまり, $f$ が正負を取る場合でも, $\Phi_f(E)=\int_E f(x)\,d\mu(x)$ は **可算加法的** な集合函数になる.

以上より, 
- 正負を取る場合に失われるのは非負性と単調性であり, 
- 空集合の値と加法性は残る. 

ここに, 測度より広い集合函数を考える動機がある.

### 正負分解と変動

**正部分と負部分.**

可積分函数 $f$ の正部分と負部分を

$$
f^+=\max\{f,0\},
\qquad
f^-=\max\{-f,0\}
$$

とする.

このとき

$$
f=f^+-f^-,
\qquad
|f|=f^++f^-
$$

である.

集合函数 $\Phi_f$ もこれに対応して

$$
\begin{aligned}
\Phi_f(E)
&=
\int_E f(x)\,d\mu(x) \\
&=
\int_E f^+(x)\,d\mu(x)-\int_E f^-(x)\,d\mu(x) \\
&=
\Phi_{f^+}(E)-\Phi_{f^-}(E).
\end{aligned}
$$

と分解される.

そこで, この二つの非負測度を

$$
\Phi_f^+(E):=\int_E f^+(x)\,d\mu(x),
\qquad
\Phi_f^-(E):=\int_E f^-(x)\,d\mu(x)
$$

とおく.

すると

$$
\Phi_f=\Phi_f^+-\Phi_f^-
$$

である. ここで $\Phi_f^+$ と $\Phi_f^-$ はどちらも非負測度である.

この分解は, 後で一般の加法的集合函数に対する Jordan 分解として抽象化される.

**上変動・下変動・全変動.**

$\Phi_f^+$ は, $f$ が正である部分から来る量を測る. これをこの具体例における **上変動** と見る.

同様に, $\Phi_f^-$ は, $f$ が負である部分から来る量を測る. これを **下変動** と見る.

両方を合わせた

$$
|\Phi_f|(E):=\Phi_f^+(E)+\Phi_f^-(E)
$$

を **全変動** と見ると,

$$
|\Phi_f|(E)
=
\int_E f^+(x)\,d\mu(x)+\int_E f^-(x)\,d\mu(x)
=
\int_E |f(x)|\,d\mu(x)
$$

となる.

$\Phi_f(E)=\int_E f(x)\,d\mu(x)$ は, 正の寄与と負の寄与が打ち消し合った後の値である. 一方,

$$
|\Phi_f|(E)=\int_E |f(x)|\,d\mu(x)
$$

は, 打ち消し合う前の総量を測る.

この違いが, 全変動の基本的な意味である.

**正の集合と負の集合.**

可積分函数 $f$ に対して

$$
P=\{x\in X\mid f(x)\ge0\},
\qquad
N=\{x\in X\mid f(x)<0\}
$$

とおく.

このとき

$$
X=P+N
$$

である.

$A\in\mathfrak{B}$ かつ $A\subset P$ ならば, $A$ 上で $f\ge0$ であるから

$$
\Phi_f(A)=\int_A f(x)\,d\mu(x)\ge0
$$

である.

一方, $A\in\mathfrak{B}$ かつ $A\subset N$ ならば, $A$ 上で $f<0$ であるから

$$
\Phi_f(A)=\int_A f(x)\,d\mu(x)\le0
$$

である.

つまり, $X$ は $\Phi_f$ が非負的に振る舞う部分 $P$ と, 非正的に振る舞う部分 $N$ に分解される.

この分解は, 後で Hahn 分解として一般化される.

## 基準測度との関係

### 零集合を無視する性質

次に, $\Phi_f$ が零集合に対してどのように振る舞うかを見る.

可測集合 $E\in\mathfrak{B}$ が

$$
\mu(E)=0
$$

を満たすとする. このとき

$$
\Phi_f(E)
=
\int_E f(x)\,d\mu(x)
=
0
$$

である. したがって

$$
\mu(E)=0
\quad\Longrightarrow\quad
\Phi_f(E)=0
$$

が成り立つ.

つまり, もとの測度 $\mu$ が無視する集合を, 積分から作った集合函数 $\Phi_f$ も無視する.

この性質を, $\Phi_f$ は $\mu$ に関して **絶対連続** であるといい,

$$
\Phi_f\ll\mu
$$

と書く.

ここでは積分 $\Phi_f$ についての性質として見ているが, 後で一般の加法的集合函数に対して同じ考えを定義し直す.

### 可算加法的でも積分の形とは限らない

ここまで見た $\Phi_f(E)=\int_E f(x)\,d\mu(x)$ は, 可算加法性を持つ集合函数であった.

しかし, 可算加法性を持つ集合函数がすべて

$$
E\mapsto\int_E f(x)\,d\mu(x)
$$

の形で表せるわけではない.

例えば $\mathbb{R}$ 上で, Dirac 測度

$$
\delta_0(E):=
\begin{cases}
1 & (0\in E),\\
0 & (0\notin E)
\end{cases}
$$

を考える.

$\delta_0$ は, 点 $0$ にすべての質量が集中している測度である. したがって $\delta_0$ は可算加法性を持つ.

実際, 互いに素な可測集合列 $E_1,E_2,\ldots$ に対して, 点 $0$ は高々一つの $E_n$ にしか入らない. したがって

$$
\delta_0\left(\sum_{n=1}^{\infty}E_n\right)
=
\sum_{n=1}^{\infty}\delta_0(E_n)
$$

が成り立つ.

一方, $\delta_0$ は Lebesgue 測度 $\lambda$ に関する積分として

$$
\delta_0(E)=\int_E f(x)\,d\lambda(x)
$$

とは表せない.

なぜなら,

$$
\lambda(\{0\})=0
$$

だが

$$
\delta_0(\{0\})=1
$$

である. したがって

$$
\delta_0\not\ll\lambda
$$

である. Lebesgue 測度が無視する一点集合を, $\delta_0$ は無視しない. この点で, $\delta_0$ は $\lambda$ から積分によって作られる集合函数とは異なる.

さらに, $\delta_0$ は点 $0$ に集中している. 実際,

$$
\mathbb{R}=\{0\}+\left(\mathbb{R}\setminus\{0\}\right)
$$

と分解すると,

$$
\delta_0(\mathbb{R}\setminus\{0\})=0,
\qquad
\lambda(\{0\})=0
$$

である.

この例は, 可算加法性だけでは, 基準測度に関する積分表示ができるとは限らないことを示している.

後で, 積分の形で表せる部分を Radon-Nikodym の定理で扱い, 点に集中するような部分を特異な部分として整理する.

## この章のまとめ

積分を

$$
E\mapsto\int_E f(x)\,d\mu(x)
$$

という集合函数として見ると, 次のことが分かる.

1. $f\ge0$ なら, $\nu_f(E)=\int_E f(x)\,d\mu(x)$ は測度である.
2. $f\in L^1(\mu)$ が正負を取ると, $\Phi_f$ は非負性と単調性を失う.
3. それでも $\Phi_f(\emptyset)=0$ であり, 可算加法性も残る.
4. $f=f^+-f^-$ に対応して, $\Phi_f=\Phi_{f^+}-\Phi_{f^-}$ という分解が現れる.
5. この分解は, 後で上変動・下変動, さらに Jordan 分解として一般化される.
6. $|\Phi_f|(E)=\int_E |f(x)|\,d\mu(x)$ は, 正負の打ち消しを除いた総量を測る.
7. $\mu(E)=0$ なら $\Phi_f(E)=0$ であり, この性質を $\Phi_f\ll\mu$ と書く.
8. Dirac 測度 $\delta_0$ のように, $E\mapsto\int_E f(x)\,d\mu(x)$ の形では表せない加法的集合函数もある.

次章では, この具体例に現れた性質を抽象化し, 加法的集合函数として整理する.
