SELECT NM_AERONAVE AS TIPO_AERONAVE, 
COUNT(*) AS TOTAL_AERONAVES
FROM TBL_AERONAVES group by NM_AERONAVE