-- ==========================================================
-- FINTECH FRAUD ANALYTICS - CONSULTAS SQL ANALÍTICAS 
-- Compatible con PostgreSQL y Supabase
-- ==========================================================

-- 1. Resumen general de alertas agrupadas por nivel de riesgo
SELECT 
    nivel_riesgo,
    COUNT(*) AS total_transacciones,
    SUM(amount) AS monto_total_riesgo,
    ROUND(AVG(amount), 2) AS promedio_monto
FROM alertas_fraude_reporte
GROUP BY nivel_riesgo
ORDER BY monto_total_riesgo DESC;

-- 2. Top 10 de usuarios con mayor concentración de operaciones sospechosas
SELECT 
    user_id,
    COUNT(*) AS total_alertas,
    SUM(amount) AS monto_acumulado_riesgo
FROM alertas_fraude_reporte
WHERE es_sospechosa = TRUE
GROUP BY user_id
ORDER BY total_alertas DESC
LIMIT 10;

-- 3. Desglose de efectividad por cada regla operativa de FraudOps
SELECT 
    SUM(CASE WHEN regla_monto_nocturno THEN 1 ELSE 0 END) AS total_alertas_nocturnas,
    SUM(CASE WHEN regla_rafaga_tiempo THEN 1 ELSE 0 END) AS total_alertas_rafagas,
    SUM(CASE WHEN regla_entorno_riesgo THEN 1 ELSE 0 END) AS total_alertas_entorno_riesgo
FROM alertas_fraude_reporte;