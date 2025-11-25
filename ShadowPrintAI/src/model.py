from sklearn.ensemble import IsolationForest
import joblib
import numpy as np
import os

MODEL_PATH = 'data/user_model.pkl'

class ShadowBrain:
    def __init__(self):
        # Contamination: qué porcentaje de los datos de entrenamiento creemos que es ruido.
        # Low contamination = modelo estricto.
        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        self.is_trained = False

    def train(self, X_matrix):
        """Entrena el modelo con una matriz de vectores de comportamiento"""
        print(f"🧠 Entrenando con {len(X_matrix)} muestras de comportamiento...")
        self.model.fit(X_matrix)
        self.is_trained = True
        self.save_model()
        print("✅ Modelo entrenado y guardado.")

    def predict(self, feature_vector):
        if not self.is_trained:
            self.load_model()
        
        # IsolationForest devuelve: 1 (Normal/Dueño), -1 (Anomalía/Intruso)
        prediction = self.model.predict([feature_vector])[0]
        # Score negativo indica anomalía, positivo normalidad
        score = self.model.decision_function([feature_vector])[0]
        
        return prediction, score

    def save_model(self):
        joblib.dump(self.model, MODEL_PATH)

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.is_trained = True
            print("📂 Modelo cargado desde disco.")
        else:
            print("⚠️ No existe modelo entrenado.")