**<u><big>Texto em negrito significa texto vindo da transformação anterior</big></u>**

**<big>1. Liste o nome de todos os clientes que fizeram encomendas contendo produtos de preço superior a €50 no ano de 2023:</big>**

 - **1. Rename product name (for natural join):**
    - ρ<sub><small>name→product_name</small></sub>(product)
 - **2. Get needed tables:** 
    - (customer ⋈ places ⋈ order ⋈ contains ⋈ **product**) 
 - **3. Filter by year and price:**
    - σ<sub><small>date=2023 ∧ price>50</small></sub>(**tabela anterior**)
 - **4. Get customer names:**
    - π<sub><small>name</small></sub>(**tabela anterior**)

 Resposta: π<sub><small>name</small></sub>(σ<sub><small>date=2023 ∧ price>50</small></sub>(customer ⋈ places ⋈ order ⋈ contains ⋈ ρ<sub><small>name→product_name</small></sub>(product)))

 <br>
 <br>
 
 **<big>2. Liste o nome de todos os empregados que trabalham em armazéns e não em escritórios e processaram encomendas em Janeiro de 2023:</big>**

 - **1. Rename department name (for natural join):**
    - ρ<sub><small>name→department_name</small></sub>(works)
 - **2. Get needed tables:**
    - (order ⋈ process ⋈ employee ⋈ **works** ⋈ workplace ⋈ warehouse)
 - **3. Filter by month:**
    - σ<sub><small>date=2023-01</small></sub>(**tabela anterior**)
 - **4. Get employee names:**
    - π<sub><small>name</small></sub>(**tabela anterior**)

 Resposta: π<sub><small>name</small></sub>(σ<sub><small>date=2023-01</small></sub>(order ⋈ process ⋈ employee ⋈ ρ<sub><small>name→department_name</small></sub>(works) ⋈ workplace ⋈ warehouse))

 <br>
 <br>

 **<big>3. Indique o nome do produto mais vendido:</big>**

 - **1. Get needed tables:**
    - (sale ⋈ order ⋈ contains ⋈ product)
 - **2. Group by product name and count:**
    - <sub><small>name</sub></small>G<sub><small>SUM(qty)</sub></small>(**tabela anterior**)
 - **3. Get max:**
    - π<sub><small>name, MAX(qty)</sub></small>(**tabela anterior**)
 - **4. Get product name:**
    - π<sub><small>name</small></sub>(**tabela anterior**)

 Resposta: π<sub><small>name</small></sub>(π<sub><small>name, MAX(qty)</small></sub>(<sub><small>name</sub></small>G<sub><small>SUM(qty)</sub></small>(sale ⋈ order ⋈ contains ⋈ product)))

 <br>
 <br>

 **<big>4. Indique o valor total de cada venda realizada:</big>**
 - **1. Get needed tables:**
    - (sale ⋈ order ⋈ contains ⋈ product)
 - **2. Group by product name, quantity and price**
    - <sub><small>name, price</sub></small>G<sub><small>SUM(qty)</sub></small>(**tabela anterior**)
 - **3. Calculate total value:**
    - π<sub><small>name, price*qty</small></sub>(**tabela anterior**)

 Resposta: π<sub><small>name, price*qty</small></sub>(<sub><small>name, price</sub></small>G<sub><small>SUM(qty)</sub></small>(sale ⋈ order ⋈ contains ⋈ product))