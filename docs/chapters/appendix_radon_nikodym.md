# Appendix Radon-Nikodym の定理

## 目的

この Appendix の目的は, Radon-Nikodym の定理を, 測度間の関係を密度函数として表す定理として紹介することである.

本編の到達点は優収束定理であり, Radon-Nikodym の定理の証明は扱わない.ここでは, 定理が何を述べているか, また積分の言葉でどのように解釈されるかを確認する.

## 同じ可測空間上の二つの測度

可測空間

$$
(X, \mathfrak{B})
$$

を固定する.

この上に二つの測度

$$
\mu, \nu:\mathfrak{B}\to\mathbb{R}\cup\{\infty\}
$$

が定義されているとする.

Radon-Nikodym の定理は, $\nu$ が $\mu$ に関して絶対連続であるとき, $\nu$ を $\mu$ に対する密度函数によって表せることを述べる.

## 絶対連続性

測度 $\nu$ が測度 $\mu$ に関して絶対連続であるとは, 任意の $A\in\mathfrak{B}$ に対して

$$
\mu(A)=0
\quad\Longrightarrow\quad
\nu(A)=0
$$

が成り立つことをいう.

この関係を

$$
\nu\ll\mu
$$

と書く.

絶対連続性は, $\mu$ が無視する集合を $\nu$ も無視する, という条件である.

例えば, $\mathbb{R}$ 上で

$$
\nu(A)=\int_A f\, d\mu
$$

と定義される測度 $\nu$ を考える.ここで $f$ は非負可測函数である.このとき, $\mu(A)=0$ ならば

$$
\nu(A)=\int_A f\, d\mu=0
$$

である.したがって

$$
\nu\ll\mu
$$

である.

Radon-Nikodym の定理は, 適切な仮定の下で, この逆向きの表示が可能であることを述べる.

## $\sigma$-有限性

測度 $\mu$ が $\sigma$-有限であるとは, 可測集合列 $X_1, X_2, \ldots\in\mathfrak{B}$ が存在して

$$
X=\bigcup_{n=1}^{\infty}X_n
$$

かつ

$$
\mu(X_n)<\infty
\qquad(n=1, 2, \ldots)
$$

を満たすことをいう.

Lebesgue 測度は $\mathbb{R}^N$ 上で $\sigma$-有限である.実際,

$$
\mathbb{R}^N=\bigcup_{n=1}^{\infty}[-n, n)^N
$$

であり, 各 $[-n, n)^N$ の Lebesgue 測度は有限である.

Radon-Nikodym の定理では, 通常 $\mu$ と $\nu$ に $\sigma$-有限性を仮定する.

## 定理の主張

$(X, \mathfrak{B})$ 上の $\sigma$-有限測度 $\mu, \nu$ について

$$
\nu\ll\mu
$$

が成り立つとする.

このとき, 非負可測函数 $f$ が存在して, 任意の $A\in\mathfrak{B}$ に対して

$$
\nu(A)=\int_A f\, d\mu
$$

が成り立つ.

この $f$ を $\nu$ の $\mu$ に関する Radon-Nikodym 微分と呼び,

$$
\frac{d\nu}{d\mu}:=f
$$

と書く.

したがって, 定理の結論は

$$
\nu(A)
=
\int_A \frac{d\nu}{d\mu}\, d\mu
$$

と書ける.

Radon-Nikodym 微分は $\mu$-a.e. の意味で一意である.すなわち, $f$ と $g$ がともに上の表示を満たすならば

$$
f=g\quad \mu\text{-a.e.}
$$

である.

## 密度函数としての解釈

式

$$
\nu(A)
=
\int_A \frac{d\nu}{d\mu}\, d\mu
$$

は, 測度 $\nu$ が測度 $\mu$ に密度函数 $d\nu/d\mu$ を掛けたものとして表されることを意味する.

Lebesgue 測度 $\mu$ に対して

$$
\nu(A)=\int_A f(x)\, d\mu(x)
$$

と書けるとき, $f$ は Lebesgue 測度に関する $\nu$ の密度である.

この見方では, 測度を変える操作は, 基準測度に関する積分の中で重みを掛ける操作として理解される.

## 確率論的解釈

確率空間上の確率測度 $P, Q$ を考える.

もし

$$
Q\ll P
$$

であれば, Radon-Nikodym 微分

$$
\frac{dQ}{dP}
$$

が存在する.

可測函数 $h$ に対して

$$
\mathbb{E}_Q[h]
=
\int h\, dQ
=
\int h\frac{dQ}{dP}\, dP
=
\mathbb{E}_P\left[h\frac{dQ}{dP}\right]
$$

が成り立つ.

この意味で, $dQ/dP$ は $P$ を基準にした $Q$ の密度, または尤度比として解釈できる.

## 本編との関係

本編では, 測度 $\mu$ に対して函数 $f$ を積分する方法を構成した.

Radon-Nikodym の定理は, 別の測度 $\nu$ に関する積分を, 基準測度 $\mu$ に関する積分へ変換する.

つまり

$$
\int h\, d\nu
$$

を

$$
\int h\frac{d\nu}{d\mu}\, d\mu
$$

として扱える.

このため, Radon-Nikodym の定理は, 測度の変換と密度函数の理論を結ぶ基本定理である.

## この Appendix の中心メッセージ

Radon-Nikodym の定理は, 絶対連続な測度 $\nu$ を, 基準測度 $\mu$ に対する密度函数 $d\nu/d\mu$ によって表す定理である.これにより, 測度を変える操作を, 積分の中の重み付けとして扱うことができる.
