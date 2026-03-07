SELECT
    country        AS nm_country,
    state          AS nm_state,
    brewery_type   AS ds_brewery_type,
    COUNT(*)       AS qtd_total_breweries
FROM silver.tb_breweries
GROUP BY
    country,
    state,
    brewery_type