# 第3章 Lebesgue 可測性と Lebesgue 測度

## 目的

この章の目的は, 第2章で導入した Lebesgue 外測度 $\mu^*$ から, Lebesgue 可測集合と Lebesgue 測度を取り出すことである.

Lebesgue 外測度は $\mathbb{R}^N$ の任意の部分集合に対して定義されるが, 任意集合の上でそのまま可算加法的になるわけではない. そこで, 外測度が加法的に振る舞う集合だけを選び出し, その集合族の上で測度を定める.

この章では $\mathbb{R}^N$ 上の Lebesgue 外測度 $\mu^*$ に限って議論する. 一般の外測度から同じ形式で測度を作る抽象的な議論は第4章で扱う.

## Lebesgue 内測度

有界集合 $A \in \mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)$ をとり, $A\subset I$ を満たす有界区間 $I\in\mathfrak{I}_N$ を一つ固定する.

外側からは区間による可算被覆を考えればよい. しかし, 内側から一般の集合を区間で埋め尽くすことは難しい. そのため, 内側の大きさは補集合の外測度を用いて間接に定める.

このとき

$$
\mu_*(A; I):=m(I)-\mu^*(I\cap A^c)
$$

を $I$ に関する $A$ の **Lebesgue 内測度** と呼ぶ.

これは, 外側の箱 $I$ の体積から, その中で $A$ の外に残る部分 $I\cap A^c$ の Lebesgue 外測度を引いた量である. したがって, $\mu_*(A; I)$ は $A$ を内側から見た大きさを表している.

なお, $I$ は区間であるから

$$
\mu^*(I)=m(I)
$$

が成り立つ. したがって

$$
\mu_*(A; I)=\mu^*(I)-\mu^*(I\cap A^c).
$$

![Lebesgue 内測度の図式](../../figures/measure/animations/lebesgue_inner_measure/gif/lebesgue_inner_measure.gif)

ここでは, 閉曲線で表した集合 $A$ を長方形 $I$ が囲み, その中で補集合部分 $I\cap A^c$ だけを外側から覆っていく様子を描いている. 右のグラフでは, 段階 $n$ の $I\cap A^c$ の外側被覆コストを $C_n$ として, $m(I)-C_n$ が内測度 $\mu_*(A;I)$ に近づく様子を示している.


## 外測度との関係

Lebesgue 内測度は, 外測度と無関係に別に導入される量ではない. 補集合の外測度を通して定まる内側の大きさである.

実際, 可算劣加法性より

$$
I=(I\cap A)\cup(I\cap A^c)
$$

であるから

$$
m(I)=\mu^*(I)\leq \mu^*(I\cap A)+\mu^*(I\cap A^c)\leq \mu^*(A)+\mu^*(I\cap A^c)
$$

となる. よって

$$
\mu_*(A; I)=m(I)-\mu^*(I\cap A^c)\leq \mu^*(A)
$$

である.

つまり, 外側から見た大きさ $\mu^*(A)$ は, 内側から見た大きさ $\mu_*(A;I)$ 以上になる.

$$
\mu_*(A; I)\leq \mu^*(A)
$$


## 可測性への動機

ここで $A\subset I$ であるから $\mu^*(A)=\mu^*(I\cap A)$ であり, 外測度 $\mu^*(A)$ と内測度 $\mu_*(A; I)$ の差は

$$
\delta(A; I)
:=
\mu^*(A)-\mu_*(A; I)
=
\mu^*(I \cap A)+\mu^*(I\cap A^c)-\mu^*(I)
$$

と書ける. これは, 区間 $I$ を $A$ と $A^c$ で切ったときに生じる外測度のずれを表している.

したがって, もし $A\subset I$ を満たす区間 $I$ に対して

$$
\mu^*(I)=\mu^*(I\cap A)+\mu^*(I\cap A^c)
$$

が成り立つなら, $A$ は区間 $I$ による切断に関して外測度を壊さない集合であるとみなせる.

この考えを区間 $I \in \mathfrak{I}_N \subset 2^{\mathbb{R}^N}$ だけでなく, 任意の集合 $B\in 2^{\mathbb{R}^N}$ に対して要求することで, Lebesgue 可測性が定義される.

![外測度と内外近似](../../figures/measure/animations/lebesgue_inner_outer_overlap/gif/lebesgue_inner_outer_overlap.gif)


## Lebesgue 可測集合

集合 $E\in 2^{\mathbb{R}^N}$ が, 任意の集合 $B\in 2^{\mathbb{R}^N}$ に対して

$$
\mu^*(B)
=
\mu^*(B\cap E)+\mu^*(B\cap E^c)
$$

を満たすとき, $E$ を **Lebesgue 可測集合** という.

Lebesgue 可測集合全体を

$$
\mathfrak{M}_{\mu^*}
:=
\{E\in 2^{\mathbb{R}^N} \mid
\forall B\in 2^{\mathbb{R}^N},\quad
\mu^*(B)=\mu^*(B\cap E)+\mu^*(B\cap E^c)\}
$$

と書く.

可測集合 $E$ は, 任意の集合 $B$ を $B\cap E$ と $B\cap E^c$ に切り分けたとき, Lebesgue 外測度を加法的に分解する集合である.

![Lebesgue 可測性による切断](../../figures/measure/animations/lebesgue_measurable/gif/lebesgue_measurable.gif)

外測度の可算劣加法性から, 任意の $B,E\in 2^{\mathbb{R}^N}$ について

$$
\mu^*(B)
\leq
\mu^*(B\cap E)+\mu^*(B\cap E^c)
$$

は常に成り立つ. Lebesgue 可測性は, 逆向きの不等式も含めて等号が成り立つことを要求している.

## 零集合と可算集合は可測である

第2章では, Lebesgue 外測度が $0$ になる集合を零集合と呼んだ.

零集合 $N\subset\mathbb{R}^N$ は Lebesgue 可測である. 実際, 任意の $B\subset\mathbb{R}^N$ に対して

$$
\mu^*(B\cap N)\leq \mu^*(N)=0
$$

であるから

$$
\mu^*(B\cap N)=0
$$

である. また $B\cap N^c\subset B$ より

$$
\mu^*(B\cap N^c)\leq \mu^*(B)
$$

である. 一方, 可算劣加法性より

$$
\mu^*(B)
\leq
\mu^*(B\cap N)+\mu^*(B\cap N^c)
=
\mu^*(B\cap N^c)
$$

となる. したがって

$$
\mu^*(B)
=
\mu^*(B\cap N)+\mu^*(B\cap N^c)
$$

が成り立つ.

よって $N$ は Lebesgue 可測である.

第2章で見たように, 任意の可算集合 $A\subset\mathbb{R}^N$ は $\mu^*(A)=0$ を満たす. したがって, 任意の可算集合は Lebesgue 可測集合であり, Lebesgue 測度 $0$ を持つ.

## 有理点集合との対応

第1章で見た有理点集合

$$
A=\mathbb{Q}^2\cap[0,1]^2
$$

では, $A$ も $A^c$ も内部に正の面積を持つ長方形を含まないため, Jordan 的な有限近似では内外近似が破綻した.

これに対して Lebesgue 外測度では, $A$ 自身は可算集合なので $\mu^*(A)=0$ であり, 補集合 $A^c$ は $[0,1]^2$ のほとんど全部を占める. したがって $I=[0,1]^2$ に対して

$$
\mu_*(A;I)=m(I)-\mu^*(I\cap A^c)=1-1=0
$$

となる. これは, 有理点集合が Jordan 的には内外近似を壊す一方で, Lebesgue の枠組みでは零集合として自然に扱われることを示している.

![有理数集合の Lebesgue 内測度](../../figures/measure/animations/rational_inner_measure/gif/rational_inner_measure.gif)

## Lebesgue 測度

Lebesgue 可測集合全体 $\mathfrak{M}_{\mu^*}$ は可算加法族になる. すなわち,

1. （空集合に対する閉性）$\emptyset\in\mathfrak{M}_{\mu^*}$.
2. （補集合に対する閉性）$E\in\mathfrak{M}_{\mu^*}$ ならば $E^c\in\mathfrak{M}_{\mu^*}$.
3. （可算和に対する閉性）$E_1,E_2,\ldots\in\mathfrak{M}_{\mu^*}$ ならば

$$
\bigcup_{n=1}^{\infty}E_n\in\mathfrak{M}_{\mu^*}.
$$

さらに, Lebesgue 外測度

$$
\mu^*: 2^{\mathbb{R}^N}\to[0,\infty]
$$

を Lebesgue 可測集合族 $\mathfrak{M}_{\mu^*} \subset 2^{\mathbb{R}^N}$ に制限したもの

$$
\mu^*|_{\mathfrak{M}_{\mu^*}}:\mathfrak{M}_{\mu^*}\to[0,\infty]
$$

は可算加法的になる.

この制限を **Lebesgue 測度** と呼び,

$$
\mu:=\mu^*|_{\mathfrak{M}_{\mu^*}}
$$

と書く.

特に, 互いに素な Lebesgue 可測集合列 $E_1,E_2,\ldots\in\mathfrak{M}_{\mu^*}$ に対して

$$
\mu\left(\bigcup_{n=1}^{\infty}E_n\right)
=
\sum_{n=1}^{\infty}\mu(E_n)
$$

が成り立つ.

この可算加法性は, $\mu^*$ を任意集合上で見るだけでは得られない. Lebesgue 可測集合に制限することで初めて得られる.

第4章では, この事実を一般の外測度に対する Carathéodory の定理として整理し直す.

## ここまでの主要な測度の比較

第1章からこの章までに現れた主要な集合函数を並べると, 次のようになる.

| 対象 | 定義域 | 値域 | 位置づけ |
| --- | --- | --- | --- |
| 体積 $m$ | $\mathfrak{I}_N$ | $[0,\infty)$ | $N$ 次元区間の体積 |
| 体積 $m$ | $\mathfrak{F}_N$ | $[0,\infty)$ | 区間塊の体積 |
| Jordan 内測度 $J_*$ | $\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)$ | $[0,\infty)$ | 有界集合を内側から近似して定める集合函数 |
| Jordan 外測度 $J^*$ | $\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)$ | $[0,\infty)$ | 有界集合を外側から近似して定める集合函数 |
| Jordan 測度 $J$ | $\mathcal{J}_N$ | $[0,\infty)$ | $J_*=J^*$ が成り立つ Jordan 可測集合上の測度 |
| Lebesgue 外測度 $\mu^*$ | $2^{\mathbb{R}^N}$ | $[0,\infty]$ | 任意集合に対して定義される外測度 |
| Lebesgue 内測度 $\mu_*(\cdot;I)$ | $2^{\mathbb{R}^N}$ | $[0,\infty)$ | 固定した区間 $I$ の中で補集合の外測度を用いて定める内側の量 |
| Lebesgue 測度 $\mu$ | $\mathfrak{M}_{\mu^*}$ | $[0,\infty]$ | $\mu^*$ を Lebesgue 可測集合に制限して得られる測度 |

この流れを大づかみに言えば, まず体積 $m$ が基本図形に対して定まり, そこから Jordan では有界集合上の内測度・外測度を経て Jordan 測度 $J$ が得られる. これに対して Lebesgue では, 任意集合上の外測度 $\mu^*$ を先に定め, 必要に応じて内測度 $\mu_*(\cdot;I)$ も補助的に用いながら, 可測集合族 $\mathfrak{M}_{\mu^*}$ を取り出して Lebesgue 測度 $\mu$ を得る.

## この章の中心メッセージ

Lebesgue 可測集合とは, Lebesgue 外測度が加法的に振る舞う集合である. 零集合, とくに可算集合は Lebesgue 可測であり, 測度 $0$ を持つ.

Lebesgue 外測度 $\mu^*$ を Lebesgue 可測集合族 $\mathfrak{M}_{\mu^*}$ に制限すると, 可算加法的な Lebesgue 測度 $\mu$ が得られる.
