import pandas as pd
import numpy as np

def extract_features(events):
    """
    Convierte una lista de eventos raw en un vector de características (una fila de datos).
    Si no hay suficientes datos, devuelve None.
    """
    if len(events) < 10:
        return None

    df = pd.DataFrame(events)
    
    # --- PROCESAMIENTO DE TECLADO ---
    keys = df[df['type'].isin(['key_press', 'key_release'])].copy()
    
    key_hold_times = []
    key_flight_times = []
    
    # Lógica simplificada para Hold Time (tiempo tecla abajo)
    # y Flight Time (tiempo entre soltar una y apretar otra)
    # En producción esto requiere un stack para manejar teclas simultáneas.
    # Aquí usaremos diferencias consecutivas simples para demostración.
    
    if len(keys) > 1:
        keys['dt'] = keys['time'].diff()
        # Filtrar tiempos absurdos (mayores a 2s es una pausa, no tipeo)
        valid_times = keys[keys['dt'] < 2.0]['dt']
        
        if len(valid_times) > 0:
            avg_key_speed = valid_times.mean()
            std_key_speed = valid_times.std()
        else:
            avg_key_speed, std_key_speed = 0, 0
    else:
        avg_key_speed, std_key_speed = 0, 0

    # --- PROCESAMIENTO DE MOUSE ---
    moves = df[df['type'] == 'mouse_move'].copy()
    mouse_speed_avg = 0
    mouse_speed_std = 0
    mouse_angle_std = 0 # "Micro-tremor" o suavidad
    
    if len(moves) > 1:
        # Calcular distancia y velocidad
        moves['dx'] = moves['x'].diff()
        moves['dy'] = moves['y'].diff()
        moves['dt'] = moves['time'].diff()
        
        moves = moves[moves['dt'] > 0] # Evitar div por cero
        moves['dist'] = np.sqrt(moves['dx']**2 + moves['dy']**2)
        moves['speed'] = moves['dist'] / moves['dt']
        
        mouse_speed_avg = moves['speed'].mean()
        mouse_speed_std = moves['speed'].std()
        
        # Calcular ángulos para ver la "rectitud" del movimiento
        moves['angle'] = np.arctan2(moves['dy'], moves['dx'])
        mouse_angle_std = moves['angle'].std() # Alta varianza = movimiento errático

    # Rellenar NaNs con 0
    avg_key_speed = float(avg_key_speed) if not np.isnan(avg_key_speed) else 0.0
    std_key_speed = float(std_key_speed) if not np.isnan(std_key_speed) else 0.0
    mouse_speed_avg = float(mouse_speed_avg) if not np.isnan(mouse_speed_avg) else 0.0
    mouse_speed_std = float(mouse_speed_std) if not np.isnan(mouse_speed_std) else 0.0
    mouse_angle_std = float(mouse_angle_std) if not np.isnan(mouse_angle_std) else 0.0

    # Vector final (Fingerprint)
    return [
        avg_key_speed,
        std_key_speed,
        mouse_speed_avg,
        mouse_speed_std,
        mouse_angle_std,
        len(events) # Intensidad de actividad
    ]