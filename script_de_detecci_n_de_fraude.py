import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generar_dataset_simulado(num_registros=1000):
    """
    Genera un conjunto de datos simulado de transacciones financieras
    para pruebas de detección de fraude en un entorno fintech.
    """
    np.random.seed(42)
    
    # IDs y Usuarios
    transaction_ids = [f"TXN_{10000 + i}" for i in range(num_registros)]
    user_ids = [f"USR_{np.random.randint(100, 200)}" for _ in range(num_registros)]
    
    # Fechas y Horarios
    fecha_inicio = datetime(2026, 10, 1, 0, 0, 0)
    timestamps = [fecha_inicio + timedelta(minutes=int(np.random.randint(0, 40000))) for _ in range(num_registros)]
    
    # Montos (Distribución normal con algunos valores atípicos elevados)
    amounts = np.round(np.random.exponential(scale=15000, size=num_registros) + 500, 2)
    
    # Ubicaciones y Dispositivos
    ubicaciones = ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'Ubicación Desconocida / VPN']
    prob_ubicaciones = [0.5, 0.2, 0.15, 0.1, 0.05]
    locations = np.random.choice(ubicaciones, size=num_registros, p=prob_ubicaciones)
    
    dispositivos = ['Android App', 'iOS App', 'Web Browser', 'Dispositivo Emulado']
    prob_dispositivos = [0.55, 0.30, 0.12, 0.03]
    device_types = np.random.choice(dispositivos, size=num_registros, p=prob_dispositivos)
    
    # Estados de transacción iniciales
    statuses = ['Aprobada'] * num_registros
    
    df = pd.DataFrame({
        'transaction_id': transaction_ids,
        'user_id': user_ids,
        'amount': amounts,
        'timestamp': timestamps,
        'location': locations,
        'device_type': device_types,
        'status': statuses
    })
    
    # Inyección deliberada de patrones sospechosos para prueba de reglas
    # 1. Ráfaga de transacciones rápidas para un usuario
    user_rafaga = 'USR_105'
    tiempo_base = datetime(2026, 10, 15, 23, 10, 0)
    for i in range(4):
        df.loc[i, 'user_id'] = user_rafaga
        df.loc[i, 'timestamp'] = tiempo_base + timedelta(minutes=i)
        df.loc[i, 'amount'] = 45000.00
        
    # 2. Transacción de alto monto en horario nocturno
    df.loc[10, 'amount'] = 350000.00
    df.loc[10, 'timestamp'] = datetime(2026, 10, 18, 3, 15, 0) # 3:15 AM
    
    # 3. Transacción desde ubicación / dispositivo riesgoso
    df.loc[20, 'location'] = 'Ubicación Desconocida / VPN'
    df.loc[20, 'device_type'] = 'Dispositivo Emulado'
    df.loc[20, 'amount'] = 180000.00
    
    return df

def procesamiento_y_limpieza(df):
    """
    Efectúa la limpieza, formateo y ordenamiento del DataFrame.
    """
    # Conversión explícita a datetime y orden cronológico
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by=['user_id', 'timestamp']).reset_index(drop=True)
    
    # Extracción de características temporales
    df['hora'] = df['timestamp'].dt.hour
    df['es_nocturno'] = df['hora'].apply(lambda x: 1 if (x >= 0 and x <= 5) else 0)
    
    return df

def aplicar_reglas_deteccion(df):
    """
    Aplica reglas operativas de FraudOps para detectar anomalías.
    """
    df['regla_monto_nocturno'] = False
    df['regla_rafaga_tiempo'] = False
    df['regla_entorno_riesgo'] = False
    
    # REGLA 1: Montos atípicos en horario nocturno (00:00 a 05:00)
    # Definimos umbral atípico como > percentil 95 de los montos generales
    umbral_monto_alto = np.percentile(df['amount'], 95)
    df['regla_monto_nocturno'] = (df['es_nocturno'] == 1) & (df['amount'] > umbral_monto_alto)
    
    # REGLA 2: Múltiples transacciones en menos de 5 minutos para un mismo usuario
    df['tiempo_previo'] = df.groupby('user_id')['timestamp'].shift(1)
    df['diferencia_minutos'] = (df['timestamp'] - df['tiempo_previo']).dt.total_seconds() / 60.0
    df['regla_rafaga_tiempo'] = df['diferencia_minutos'].apply(lambda x: True if (pd.notnull(x) and x <= 5) else False)
    
    # REGLA 3: Transacciones desde Ubicación Desconocida/VPN o Dispositivo Emulado
    df['regla_entorno_riesgo'] = (df['location'] == 'Ubicación Desconocida / VPN') | (df['device_type'] == 'Dispositivo Emulado')
    
    # Evaluación general de alerta
    df['es_sospechosa'] = df['regla_monto_nocturno'] | df['regla_rafaga_tiempo'] | df['regla_entorno_riesgo']
    
    # Nivel de riesgo asignado
    def calcular_nivel_riesgo(row):
        alertas = sum([row['regla_monto_nocturno'], row['regla_rafaga_tiempo'], row['regla_entorno_riesgo']])
        if alertas >= 2:
            return 'ALTO'
        elif alertas == 1:
            return 'MEDIO'
        return 'BAJO'

    df['nivel_riesgo'] = df.apply(calcular_nivel_riesgo, axis=1)
    
    return df

def generar_reporte_y_exportar(df):
    """
    Muestra estadísticas clave del análisis y exporta el reporte de alertas a un archivo CSV.
    """
    total_transacciones = len(df)
    transacciones_sospechosas = df[df['es_sospechosa']]
    total_alertas = len(transacciones_sospechosas)
    porcentaje_fraude = (total_alertas / total_transacciones) * 100
    
    monto_total_riesgo = transacciones_sospechosas['amount'].sum()
    
    print("="*60)
    print("REPORTE DE DETECCIÓN DE FRAUDE FINTECH - FRAUDOPS")
    print("="*60)
    print(f"Total de transacciones analizadas: {total_transacciones}")
    print(f"Total de alertas de sospecha: {total_alertas} ({porcentaje_fraude:.2f}%)")
    print(f"Monto total en riesgo detectado: ${monto_total_riesgo:,.2f}")
    print("-" * 60)
    print("Desglose por Nivel de Riesgo:")
    print(df['nivel_riesgo'].value_counts())
    print("-" * 60)
    print("Alertas por tipo de regla:")
    print(f" - Montos atípicos nocturnos: {df['regla_monto_nocturno'].sum()}")
    print(f" - Ráfaga de transacciones (< 5 min): {df['regla_rafaga_tiempo'].sum()}")
    print(f" - Entornos de alto riesgo (VPN/Emulador): {df['regla_entorno_riesgo'].sum()}")
    print("="*60)
    
    # Exportar resultados con alertas a CSV
    columnas_exportar = [
        'transaction_id', 'user_id', 'timestamp', 'amount', 
        'location', 'device_type', 'nivel_riesgo', 'es_sospechosa',
        'regla_monto_nocturno', 'regla_rafaga_tiempo', 'regla_entorno_riesgo'
    ]
    
    archivo_salida = 'alertas_fraude_reporte.csv'
    df[df['es_sospechosa']][columnas_exportar].to_csv(archivo_salida, index=False)
    print(f"\n[INFO] Archivo de alertas exportado exitosamente como: {archivo_salida}")

if __name__ == '__main__':
    # 1. Cargar datos
    raw_df = generar_dataset_simulado(1200)
    
    # 2. Procesar datos
    clean_df = procesamiento_y_limpieza(raw_df)
    
    # 3. Aplicar motor de reglas de fraude
    analyzed_df = aplicar_reglas_deteccion(clean_df)
    
    # 4. Generar reporte y exportar CSV
    generar_reporte_y_exportar(analyzed_df)