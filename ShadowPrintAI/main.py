import sys
import time
import pandas as pd
import os
from src.collector import DataCollector
from src.features import extract_features
from src.model import ShadowBrain
from colorama import Fore, Style, init

init(autoreset=True)

DATA_FILE = 'data/raw_behavior.csv'

def mode_record():
    """Graba sesiones de comportamiento para crear el dataset"""
    collector = DataCollector()
    print(Fore.CYAN + "=== MODO GRABACIÓN ===")
    print("Usa la PC normalmente. El sistema capturará micro-patrones.")
    print("Presiona CTRL+C para terminar y guardar.\n")
    
    collector.start_listening()
    dataset = []

    try:
        while True:
            # Capturamos en ventanas de 10 segundos
            time.sleep(10)
            events = collector.get_buffer_and_clear()
            features = extract_features(events)
            
            if features:
                print(f"Capturado bloque de actividad: {features}")
                dataset.append(features)
            else:
                print("Usuario inactivo...")

    except KeyboardInterrupt:
        collector.stop_listening()
        print(Fore.YELLOW + "\nGuardando datos...")
        
        # Guardar a CSV
        df = pd.DataFrame(dataset, columns=['k_avg', 'k_std', 'm_avg', 'm_std', 'm_ang_std', 'activity'])
        
        # Append si ya existe, sino crear
        if os.path.exists(DATA_FILE):
            df.to_csv(DATA_FILE, mode='a', header=False, index=False)
        else:
            df.to_csv(DATA_FILE, index=False)
            
        print(Fore.GREEN + f"✅ Datos guardados en {DATA_FILE}. Total muestras: {len(df)}")

def mode_train():
    """Entrena la IA con los datos guardados"""
    print(Fore.CYAN + "=== MODO ENTRENAMIENTO ===")
    if not os.path.exists(DATA_FILE):
        print(Fore.RED + "Error: No hay datos grabados. Ejecuta 'record' primero.")
        return

    df = pd.read_csv(DATA_FILE)
    brain = ShadowBrain()
    brain.train(df.values)

def mode_watch():
    """Monitor en tiempo real"""
    print(Fore.CYAN + "=== MODO VIGILANCIA (WATCHER) ===")
    brain = ShadowBrain()
    brain.load_model()
    collector = DataCollector()
    
    collector.start_listening()
    
    try:
        while True:
            time.sleep(8) # Ventana de análisis de 8 segundos
            events = collector.get_buffer_and_clear()
            features = extract_features(events)
            
            if features:
                pred, score = brain.predict(features)
                
                # Isolation Forest: 1 = Normal (Dueño), -1 = Anomalía (Intruso)
                if pred == 1:
                    print(Fore.GREEN + f"[OK] Usuario Legítimo (Score: {score:.4f})")
                else:
                    print(Fore.RED + Style.BRIGHT + f"[ALERTA] COMPORTAMIENTO SOSPECHOSO DETECTADO (Score: {score:.4f})")
                    # AQUÍ PODRÍAS: Bloquear PC, Mandar Email, etc.
            else:
                print(Fore.BLUE + "[Inactivo] Esperando inputs...")

    except KeyboardInterrupt:
        collector.stop_listening()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py [record | train | watch]")
    else:
        mode = sys.argv[1]
        if mode == 'record': mode_record()
        elif mode == 'train': mode_train()
        elif mode == 'watch': mode_watch()
        else: print("Modo desconocido.")