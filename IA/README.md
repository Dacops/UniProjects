Use of package numpy reccomended

Navios:
  1 <-->
  2 <->
  3 <>
  4 -

top, bottom, middle, left, right, water, circle
horizontalmente ou verticalmente

gridsl -> grids em que o navio de tamanho l está localizado - subset de the gridsall

M(i,j) = 1 se cell(i,j) te peça de navio no g0 (inicial)
       = 0 se tem água na cell(i,j) em g0
       = 100 c.c

G(i,j,g) = 1, se cell(i,j) tem peça no grid g
         = 0, c.c
(utilizamos get_value para esta função)

P(i,j,g) = 1 se o G(i,j,g) = 1 ou G(i,j+1,g) ou G(i+1,j,g) = 1 ou G(i+1,j+1,g) = 1
         = 0 , c.c
(utilizamos get_value, adjacent_vertical_values, adjacent_horizontal_values)

y(g) = 1 se o grid g é usado no final grid
     = 0 c.c

Constraints:
  - g∑ j∑ y(g) * G(i,j,g) = Ri ∀i [a soma das células G(i,j,g) da grid final na linha i é igual ao Ri]
  - g∑ i∑ y(g) * G(i,j,g) = Ci ∀j [a soma das células G(i,j,g) da grid final na coluna j é igual ao Ci]
  - (g ε gridsl)∑ y(g) = Sl ∀l [a soma de gridsl tem que ser igual ao número de navios com aquele tamanho]
  - g∑ P(i,j,g) * y(g) ≤ 1 ∀i,j [os grids não se podem contradizer segundo a condição P]
  - g∑ y(g) * G(i,j,g) = M(i,j) ∀i,j|M(i,j) =0 or M(i,j) =1 [cell(i,j) em g0 = cell(i,j) no grid final]
  - y(g) ε {0,1} [y é uma variável decisiva] 
