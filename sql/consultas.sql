-- Quantas linhas existem em cada tabela, e qual o período coberto pelos dados?

SELECT COUNT(*) AS quant_linhas
  FROM cidade;

SELECT COUNT(*) AS quant_linhas, MIN(data) AS primeiro_dia, MAX(data) AS dia_final
  FROM clima;

SELECT nome, COUNT(*) AS lin_por_cidade_tabelaclima
  FROM clima
 INNER JOIN cidade 
    ON clima.cidade_id = cidade.id
 GROUP BY nome;

-- Resultado: 27 cidades na tabela cidade, 59184 linhas na tabela clima, período dos dados de 2020-01-01 a 2025-12-31, 2192 linhas para cada cidade na tabela clima.



-- Existe alguma data faltando dentro do período coberto?

  WITH cidade_data AS (
SELECT nome, cidade_id, data
  FROM clima
 INNER JOIN cidade
    ON clima.cidade_id  = cidade.id
    ),

       data_faltante AS (
SELECT nome, data, LEAD(data, 1) OVER (PARTITION BY cidade_id ORDER BY data ASC) AS proxima_data
  FROM cidade_data
    )
    
SELECT nome, data, proxima_data, (proxima_data - data) AS diferenca_data
  FROM data_faltante
 WHERE (proxima_data - data) > 1;
 
 
SELECT nome
  FROM cidade
 INNER JOIN clima
    ON cidade.id = clima.cidade_id
 GROUP BY nome
HAVING MIN(data) <>'2020-01-01'
    OR MAX(data) <> '2025-12-31';

-- Resultado: 0 datas faltando, data inicial e final corretas.




-- Qual cidade teve a maior temperatura média no período de 6 anos?

SELECT nome, ROUND(AVG(temperatura_media_c)::numeric, 2) AS media_temperatura
  FROM cidade
 INNER JOIN clima
    ON cidade.id = clima.cidade_id
 GROUP BY nome
 ORDER BY media_temperatura DESC
 LIMIT 1;

-- Resultado: Teresina, com média de 28,21°C




-- Qual foi o mês/ano mais chuvoso de cada cidade?

  WITH soma_precipitacao_mes AS (
SELECT nome, EXTRACT(MONTH FROM data) AS mes, EXTRACT(YEAR FROM data) AS ano, ROUND(SUM(precipitacao_mm)::numeric, 2) AS precipitacao
  FROM clima
 INNER JOIN cidade 
    ON cidade.id = clima.cidade_id
 GROUP BY nome, EXTRACT(MONTH FROM data), EXTRACT(YEAR FROM data)
 ),
 
        ranking_chuva AS (
 SELECT nome, mes, ano, precipitacao, RANK() OVER (PARTITION BY nome ORDER BY precipitacao DESC) as posicao
   FROM soma_precipitacao_mes
   )
   
 SELECT nome, mes, ano, precipitacao
   FROM ranking_chuva
  WHERE posicao = 1;
 
 -- Resultado: Mostra o mês/ano mais chuvoso de cada cidade, e precipitação.
 
 
 
 
 
 -- Duração da luz do dia e radiação solar se relacionam com a temperatura?
 
 SELECT nome, ROUND(CORR(duracao_luz_dia_h, temperatura_media_c)::numeric, 3) AS corr_luz_temp, 
 		ROUND(CORR(radiacao_solar_mj_m2, temperatura_media_c)::numeric, 3) AS corr_rad_temp
   FROM clima
  INNER JOIN cidade
     ON clima.cidade_id = cidade.id
  GROUP BY nome;

 -- Resultado: Mostra a correlação entre duração da luz do dia e temperatura, e a correlação entre radiação solar e temperatura.

