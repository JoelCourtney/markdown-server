# This is a Test

||toc||

## header two


```[css code]
h1 {
  font-family: times;
}
```



```[python code]
import altair as alt
from vega_datasets import data

cars = data.cars()

chart = alt.Chart(cars).mark_bar().encode(
    x='Origin',
    y='count()'
).properties(
    width=400,
    height=150
)

plot(chart)
```





$$\div\va E = \frac{\rho}{\epsilon_0}$$

hello world

mod this " is in quotes" huh

> This is a block qutoe asdf asdf asdf asdf asdf asdfa;lsdfa;sdlfjas;ldfj;alsdkf ja;lsf 1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9  jal;skdfj ;alsdkfj ;alskdfj a;lksdfj ;laskdfj ;laksdjf ;

<b>embedded & html</b>

```[javascript code]
var trace1 = {
  x: [1, 2, 3, 4],
  y: [10, 15, 13, 17],
  type: 'scatter'
};

var trace2 = {
  x: [1, 2, 3, 4],
  y: [16, 5, 11, 9],
  type: 'scatter'
};

var data = [trace1, trace2];

Plotly.newPlot('plot', data);

log("hello world");
log(5)
```
||plot||

```[tikz code]
\draw (0,0) -- (1,1);
```

```[python code]
from math import pi, sqrt, exp, log10, sin, sin
from astropy import units as u
from astropy.constants import G, k_B, m_e, h, c, L_sun, R_earth, m_p, hbar, e, M_sun
```

```[python code]
delta_lambda = 18*u.nm
lambda_0 = 656.28*u.nm
z = delta_lambda / lambda_0
v = c*((z+1)**2-1)/((z+1)**2+1)
print('velocity: {:0.3}'.format(v.to(u.km/u.s)))
```

```[code python]
for i in range(0,10):
  if i % 2 == 0:
    print(i)
```

asdf

```[code python]
  else:
    print(i)
```

![test image](spiral.png)