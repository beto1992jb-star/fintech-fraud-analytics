# 🛡️ Fintech Fraud Analytics & FraudOps Engine

Proyecto técnico enfocado en la detección automatizada de anomalías y análisis de riesgo transaccional en entornos fintech, diseñado para optimizar los procesos de revisión de backoffice (FraudOps).

## 🚀 Stack Tecnológico
- **Python (Pandas, NumPy):** Procesamiento de datos, estructuración temporal y motor lógicos de reglas.
- **SQL / PostgreSQL (Supabase):** Consultas analíticas y segmentación de riesgo.
- **Git & GitHub:** Control de versiones y despliegue del portfolio.

## 📂 Estructura del Repositorio
- `scripts/fraud_detection.py`: Script principal con el motor de reglas de fraude.
- `sql/queries_analiticas.sql`: Consultas SQL para análisis de métricas en bases de datos relacionales.
- `data/alertas_fraude_reporte.csv`: Reporte exportado con el análisis de transacciones sospechosas.

## ⚙️ Reglas de Negocio Implementadas (FraudOps)
1. **Montos Atípicos Nocturnos:** Identificación de operaciones en el percentil 95 superior de montos ejecutadas entre las 00:00 y 05:00 hs.
2. **Ráfagas de Transacciones:** Detección de múltiples movimientos del mismo usuario en un intervalo menor a 5 minutos.
3. **Entornos de Alto Riesgo:** Filtrado de transacciones originadas en dispositivos emulados o conexiones de riesgo.

---
*Desarrollado como parte del portfolio profesional de Data Science & Data Analytics.*