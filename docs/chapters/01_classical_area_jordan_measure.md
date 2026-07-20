# 第1章 古典的面積概念と Jordan 測度

## 目的

この章の目的は, 古典的な長さ・面積・体積の基礎を確認し, Jordan 測度を有限個の基本図形による内外近似の極限として位置づけることである.

## 古典的面積概念

図形が与えられたとき, その面積を定める古典的な方法は, 図形を有限個の長方形など何らかの基本図形の直和で近似することである. 
すなわち, 図形の内部に含まれる有限個の基本図形の和を内側近似とし, 図形を覆う有限個の基本図形の和を外側近似として, 内側近似と外側近似の差が小さくなるように, 図形を細分していく.
このとき, 内側近似および外側近似がある極限値に収束するならば, その極限値を図形の面積と定める.
以下では, この古典的な面積概念を Jordan 測度の定義に基づいて定式化する.

![基本図形を増やしながら円板の面積を近似する図](../../figures/measure/animations/classical_area_coverings/gif/classical_area_coverings.gif)

## 区間と区間塊

### 区間: 基本図形

Euclid 空間 $\mathbb{R}^N$ において, 半開**区間**

$$
I=[a_1, b_1)\times\cdots\times[a_N, b_N)
$$

を基本図形とする. ここで

$$
-\infty\leq a_k<b_k\leq\infty
$$

とする.

このような**区間の全体**を $\mathfrak{I}_N$ と書く.
すなわち,
$$
\mathfrak{I}_N = \{[a_1, b_1)\times\cdots\times[a_N, b_N) \subset \mathbb{R}^N \mid -\infty\leq a_k<b_k\leq\infty, \ k=1, \ldots, N\}
$$

有界な区間 $I \in \mathfrak{I}_N$ に対して, その**体積**を表す集合函数

$$
m: \mathfrak{I}_N \to [0, \infty)
$$

を

$$
m(I):=\prod_{k=1}^{N}(b_k-a_k)
$$

と定める. 空集合 $\emptyset \in \mathfrak{I}_N$ に対しては

$$
m(\emptyset):=0
$$

と定める.

![半開区間と体積の概念図](../../figures/measure/static/concepts/half_open_interval_volume.png)

### 区間塊: 有限個の区間の直和

互いに素な区間の有限個 $I_1, \ldots, I_n \in \mathfrak{I}_N$ の直和として表される集合

$$
E= \sum_{k=1}^{n} I_k = I_1+\cdots+I_n \quad (I_i \cap I_j = \emptyset \ (i\neq j))
$$

を**区間塊**と呼ぶ. **区間塊全体**を $\mathfrak{F}_N$ と書く.

すなわち,
$$
\mathfrak{F}_N := \{E\subset \mathbb{R}^N \mid E= \sum_{k=1}^{n} I_k, \ I_k\in\mathfrak{I}_N, \ I_i \cap I_j = \emptyset \ (i\neq j), \ k=1, \ldots, n, \ n\in\mathbb{N}\}
$$

区間塊 $E$ を互いに素な区間 $I_1, \ldots, I_n \in \mathfrak{I}_N$ の直和として表したとき, その体積を

$$
m(E):=\sum_{k=1}^{n}m(I_k)
$$

と定める.

このとき, 体積を表す函数 $m$ は, 区間全体 $\mathfrak{I}_N$ から区間塊全体 $\mathfrak{F}_N$ へ拡張される.

$$
m: \mathfrak{F}_N \to [0, \infty)
$$

この定義が表示の仕方によらないことは, 区間を共通細分することで確認できる.つまり, 同じ区間塊を異なる直和表示で表した場合でも, 十分細かい共通分割を取れば, 両方の表示は同じ有限個の小区間の直和に帰着される.


![同じ区間塊を異なる長方形分割で表す図](../../figures/measure/static/concepts/interval_block_decomposition.png)

重ならない有限個の区間塊 $E_1, \ldots, E_n \in \mathfrak{F}_N$ を合わせたときの体積は, 各部分の体積の和として自然に計算できる.

$$
m\Bigl(\sum_{k=1}^{n} E_k\Bigr) = \sum_{k=1}^{n} m(E_k)
$$

## Jordan 内測度と Jordan 外測度

有界集合 $A\subset\mathbb{R}^N$ を考える.

区間塊 $E\in\mathfrak{F}_N$ によって $A$ を内側から近似し, その体積の上限を取ることで **Jordan 内測度** を定める.

$$
J_*(A)
:=
\sup\{m(E)\mid E\subset A, \ E\in\mathfrak{F}_N\}
$$

また, 区間塊 $F\in\mathfrak{F}_N$ によって $A$ を外側から覆い, その体積の下限を取ることで **Jordan 外測度** を定める.

$$
J^*(A)
:=
\inf\{m(F)\mid A\subset F, \ F\in\mathfrak{F}_N\}
$$

常に

$$
J_*(A)\leq J^*(A)
$$

である. これは, $E\subset A\subset F$ ならば単調性により $m(E)\leq m(F)$ となるためである.

![Jordan 的な面積近似](../../figures/measure/animations/jordan_curve_area/gif/jordan_curve_area.gif)


ここで定義域を整理しておく. 一般に, 集合 $X$ の部分集合全体を

$$
2^X
:=
\{A\mid A\subset X\}
$$

と書く. これは $X$ の**冪集合**である.

この記号を用いて, Euclid 空間 $\mathbb{R}^N$ 上の**有界集合全体**を

$$
\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)
:=
\{A\in 2^{\mathbb{R}^N}\mid A\text{ は有界}\}
$$

と書く. つまり, $\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)$ は冪集合 $2^{\mathbb{R}^N}$ のうち, 有界な部分集合だけを集めた集合族である.

Jordan 内測度 $J_*$ および Jordan 外測度 $J^*$ は, $\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N) \subset 2^{\mathbb{R}^N}$ 上で定義される集合函数である. すなわち,

$$
J_*, J^*
:
\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)
\to
[0,\infty)
$$

である.

## Jordan 可測性

### 定義

有界集合 $A\in\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)$ が

$$
J_*(A)=J^*(A)
$$

を満たすとき, $A$ は **Jordan 可測** であるという. この共通値を

$$
J(A):=J_*(A)=J^*(A)
$$

と書き, $A$ の **Jordan 測度** と呼ぶ.

**Jordan 可測な有界集合全体**を

$$
\mathcal{J}_N
:=
\{A\in\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N) \mid J_*(A)=J^*(A)\}
$$

と書く.

同値な見方として, 任意の正数 $\epsilon>0$ に対して, 区間塊 $E, F\in\mathfrak{F}_N$ が存在して

$$
E\subset A\subset F
$$

かつ

$$
m(F)-m(E)<\epsilon
$$

となるとき, $A$ は Jordan 可測である.

この条件は, 有限個の区間からなる内側近似と外側近似の差を任意に小さくできることを意味する.

Jordan 測度 $J$ は, Jordan 可測集合全体 $\mathcal{J}_N \subset \mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N) \subset 2^{\mathbb{R}^N}$ 上で定義される集合函数

$$
J: \mathcal{J}_N \to [0, \infty)
$$

であり, Jordan 内測度 $J_*$ および Jordan 外測度 $J^*$ の Jordan 可測集合への制限である.

$$
J=J_*|_{\mathcal{J}_N}=J^*|_{\mathcal{J}_N}
$$

したがって, $J_*$ と $J^*$ は有界集合全体に定義されるが, Jordan 測度 $J$ はそのうち内測度と外測度が一致する集合にだけ定義される. この点は, 任意集合に外測度を定義してから可測集合を取り出す Lebesgue 測度の構成と対比される.


### ここまでの集合函数と定義域

ここまでに出てきた集合函数とその定義域を整理すると, 次のようになる.

| 集合函数 | 定義域 | 値域 |
| --- | --- | --- |
| 区間の体積 $m$ | 半開区間全体 $\mathfrak{I}_N$ | $[0,\infty)$ |
| 区間塊の体積 $m$ | 区間塊全体 $\mathfrak{F}_N$ | $[0,\infty)$ |
| Jordan 内測度 $J_*$ | 有界部分集合全体 $\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)$ | $[0,\infty)$ |
| Jordan 外測度 $J^*$ | 有界部分集合全体 $\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)$ | $[0,\infty)$ |
| Jordan 測度 $J$ | Jordan 可測集合全体 $\mathcal{J}_N$ | $[0,\infty)$ |

つまり, $m$ は基本図形である区間と区間塊に対する体積であり, $J_*$ と $J^*$ は有界集合全体に対する内外近似である. そのうち $J_*(A)=J^*(A)$ が成り立つ集合だけを集めたものが $\mathcal{J}_N$ であり, その上で Jordan 測度 $J$ が定義される.


### 有限近似としての見方

ここで重要なのは, 体積 $m$ がまず有限個の区間の直和で表される区間塊 $\mathfrak{F}_N$ に対して定まる函数だという点である.
Jordan 内測度 $J_*$ と Jordan 外測度 $J^*$ は, この $m$ を区間塊による内側近似の上限と外側近似の下限として sup / inf で拡張したものであり, Jordan 測度 $J$ はそれらが一致する集合上で定まる.
したがって, 曲がった図形の面積も, 可算個の区間で直接覆って求めるのではなく, あくまで有限個の区間の和による近似の極限として定まる.

この見方は, 円盤の面積を内接正 $n$ 角形で近似する古典的な計算と同じ発想である.
半径 $r$ の円盤 $D_r$ に内接する正 $n$ 角形を $P_n$ とし, それを

$$
P_n=\bigsqcup_{k=1}^{n}T_{n,k}
$$

と $n$ 個の二等辺三角形の直和に分けると,

$$
Area(P_n)=\sum_{k=1}^{n}m(T_{n,k})
=\frac{n}{2}r^2\sin\frac{2\pi}{n}
\longrightarrow \pi r^2
\qquad (n\to\infty)
$$

となる. 外側近似も同様に, 外接正 $n$ 角形の面積が円盤の面積 $\pi r^2$ に収束する. したがって, 円盤は面積 $\pi r^2$ を持つことが定まる.
Jordan 測度でも本質は同じであり, 各段階では有限和で表される図形の体積を計算し, その極限として曲がった図形の面積を定める.


### 補足: 境界と内部近似

以下は, Jordan 可測性の直観を補うための補足説明である.

有界集合 $A\in\mathcal{P}_{\mathrm{bd}}(\mathbb{R}^N)$ について, Jordan 可測性は境界 $\partial A$ の Jordan 外測度が $0$ であることと深く関係する.

直観的には, 内側近似と外側近似の差は境界付近に集中する.したがって, 境界の体積が $0$ と見なせるならば, 内側近似と外側近似の差は消える.

例えば, 円板や球の境界は曲線または曲面であり, $N$ 次元の体積としては $0$ である.そのため, これらは有限個の直方体で正確には表せないが, Jordan 可測である.

![穴を持つ集合の Jordan 的近似](../../figures/measure/animations/jordan_holes_adaptive/gif/jordan_holes_adaptive.gif)


## Jordan可測でない例：有理点集合

平面上の有理点集合

$$
A=\mathbb{Q}^2\cap[0, 1]^2
$$

を考える.

任意の空でない長方形は有理点を含むので, $A$ は $[0, 1]^2$ 上で稠密である. また, 任意の空でない長方形は無理数成分を持つ点も含むので, $A^c$ も $[0, 1]^2$ 上で稠密である.

ここで重要なのは, この稠密性のため $A$ も $A^c$ も $[0, 1]^2$ において内部の長方形を持たないことである. すなわち, 有理点だけからなる空でない長方形も, 無理数点だけからなる空でない長方形も存在しない. したがって, Jordan 的な内側近似の出発点になる正の面積の長方形を, $A$ に対しても $A^c$ に対しても取ることができない.

端的に言えば, 有限個の長方形で外側から $A$ を覆おうとすると, $[0, 1]^2$ の中に正の面積を持つ隙間を残すことはできない. そのような隙間には必ず有理点が入り込み, その点を覆い損ねるからである. 逆に, 内側から $A$ に正の面積を持つ長方形を入れようとすると, その長方形には必ず無理数成分を持つ点が入り込み, $A$ の内側に収まらない. したがって, 外側近似は全体 $[0, 1]^2$ まで膨らみ, 内側近似は面積 $0$ にとどまる.

![有理点集合の拡大図](../../figures/measure/animations/rational_density_zoom_centered/gif/rational_density_zoom_centered.gif)

まず, $A$ に含まれる正の面積の長方形は取れない. ある有理点を中心にどれほど小さい正方形を取っても, その内部には必ず無理数成分を持つ点が入り込むからである.

このため, $A$ に含まれる区間塊で正の面積を持つものは存在しない. したがって

$$
J_*(A)=0
$$

である. 実際, もし $E\in\mathfrak{F}_2$ が $E\subset A$ を満たして正の面積を持つならば, $E$ は正の面積を持つ長方形を含むはずであるが, そのような長方形は存在しない.

![有理点集合の稠密性](../../figures/measure/animations/rational_density_zoom/gif/rational_density_zoom.gif)

次に, $A^c$ に含まれる正の面積の長方形も取れない. 見えている有理点を避けるように小正方形を選んだつもりでも, その内部にはなお有理点が存在するからである. したがって, 無理数点だけを内部に持つ長方形も存在しない.

一方, $A$ を含む区間塊 $F$ は, 稠密性のため $[0, 1]^2$ 全体を覆うように振る舞う. 少なくとも外側からの有限長方形近似では, $[0, 1]^2$ の面積を避けることができない. したがって

$$
J^*(A)=1
$$

となる. 実際, $F\in\mathfrak{F}_2$ が $A\subset F\subset [0, 1]^2$ を満たすとする. もし $F\neq [0, 1]^2$ ならば, $[0, 1]^2\cap F^c$ は正の面積を持つ長方形を含む. しかし $[0, 1]^2\cap F^c\subset A^c$ であるから, これは $A^c$ が正の面積を持つ長方形を含まないことに反する.

よって

$$
0 = J_*(A)\neq J^*(A) = 1
$$

であり, $A$ は Jordan 可測ではない.

有理点集合では, 集合そのものにもその補集合にも, Jordan 的な近似の材料になる正の面積の長方形が現れない. そのため, 有限個の長方形による内外近似はここで破綻する.

しかし, $A$ は可算集合である. Lebesgue 測度では, 可算集合は測度 $0$ になる. この差が, Jordan 測度から Lebesgue 測度へ進む動機になる.

## この章の中心メッセージ

Jordan 測度は, 有限個の基本図形による内外近似の極限として自然な面積概念である. しかし, 可算集合や稠密集合を安定に扱うには不十分である. Lebesgue 測度への移行点は, 有限近似から可算被覆へ移るところにある.
