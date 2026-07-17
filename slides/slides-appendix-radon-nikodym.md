---
layout: section
---

# Appendix Radon-Nikodym の定理

一つの測度を別の測度に対する密度として表す

---
layout: default
---

# 目的

同じ可測空間上の二つの測度を比較し, 一方が他方に関して密度函数を持つとはどういうことかを見る.

Radon-Nikodym の定理は, 測度の絶対連続性を積分表示に変換する定理である.

---
layout: default
---

# 同じ可測空間上の二つの測度

同じ可測空間 $(X,\mathfrak{B})$ 上に二つの測度 $\mu,\nu$ があるとする.

$$
\mu,\nu:\mathfrak{B}\to[0,\infty]
$$

同じ集合 $A\in\mathfrak{B}$ に対して, $\mu(A)$ と $\nu(A)$ は異なる大きさを与える.

Radon-Nikodym の定理は, $\nu$ を $\mu$ に対する重み付き測度として表せる条件を与える.

---
layout: default
---

# 絶対連続性

$\nu$ が $\mu$ に関して絶対連続であるとは,

$$
\mu(A)=0\quad\Rightarrow\quad \nu(A)=0
$$

がすべての $A\in\mathfrak{B}$ で成り立つことである.

このとき

$$
\nu\ll\mu
$$

と書く.

---
layout: default
---

# $\sigma$-有限性

測度 $\mu$ が $\sigma$-有限であるとは, $X$ が可算個の有限測度集合で覆えることをいう.

$$
X=\bigcup_{n=1}^{\infty}X_n,
\qquad
\mu(X_n)<\infty
$$

Radon-Nikodym の定理では, $\sigma$-有限性が重要な仮定になる.

---
layout: default
---

# 定理の主張

$(X,\mathfrak{B})$ 上の $\sigma$-有限測度 $\mu,\nu$ について, $\nu\ll\mu$ ならば, 非負可測函数 $f$ が存在して

$$
\nu(A)=\int_A f\,d\mu
$$

がすべての $A\in\mathfrak{B}$ で成り立つ.

この $f$ を Radon-Nikodym 微分と呼び,

$$
f=\frac{d\nu}{d\mu}
$$

と書く.

---
layout: default
---

# 密度函数としての解釈

Radon-Nikodym 微分 $d\nu/d\mu$ は, $\mu$ を基準にして $\nu$ がどれだけ重み付けされているかを表す密度函数である.

$$
d\nu=f\,d\mu
$$

という記法は, この関係を直観的に表している.

つまり各可測集合 $A$ について

$$
\nu(A)=\int_A f\,d\mu
$$

と読む.

---
layout: default
---

# 確率論的解釈

確率測度 $P,Q$ について $Q\ll P$ なら,

$$
\frac{dQ}{dP}
$$

は $P$ を基準にした $Q$ の尤度比として読める.

期待値の変換は

$$
\int X\,dQ
=
\int X\frac{dQ}{dP}\,dP
$$

と書ける.

---
layout: default
---

# 本編との関係

本編では, 一つの測度空間上で函数を積分する枠組みを作った.

Radon-Nikodym の定理は, 測度そのものを変えるときに, その変化を積分内の密度函数として扱うための定理である.

---
layout: end
---

# この Appendix の中心メッセージ

- 絶対連続性 $\nu\ll\mu$ は, $\mu$ の零集合を $\nu$ も零集合と見ることを意味する.
- Radon-Nikodym の定理は, $\nu$ を $\mu$ に対する密度函数として表す.
- 確率論では, 測度変更や尤度比の基礎になる.
