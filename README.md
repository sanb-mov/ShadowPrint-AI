***
# 🕵️ ShadowPrint AI
> **Perfilado de Comportamiento por Micro-Tiempos Humanos**  
> *Autenticación Continua (Zero Trust) basada en Biometría Conductual.*

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AI](https://img.shields.io/badge/AI-Scikit--Learn-orange)
![Privacy](https://img.shields.io/badge/Privacy-100%25-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**ShadowPrint AI** es una herramienta de ciberseguridad y análisis forense que verifica la identidad del usuario analizando **cómo** interactúa con la computadora, no **qué** escribe. Utiliza algoritmos de Machine Learning (Isolation Forest) para detectar patrones biométricos invisibles como la latencia entre teclas, la velocidad del mouse y el micro-temblor de la mano.

---

## 🧩 Características Principales

*   **🔒 Privacidad Absoluta:** No registra texto (no es un keylogger). Solo captura marcas de tiempo (timestamps) y vectores numéricos.
*   **🧠 Identificación Biométrica:** Crea una "Huella Digital de Comportamiento" única basada en ritmos subconscientes.
*   **⚡ Detección en Tiempo Real:** Analiza el flujo de trabajo en ventanas de 10 segundos para autenticar continuamente.
*   **🤖 Anti-Bot:** Distingue fácilmente entre un humano y un script automatizado (los bots son demasiado "perfectos" o lineales).
*   **🚨 Detección de Intrusos:** Si dejas tu PC desbloqueada y alguien intenta usarla, el sistema detectará la anomalía conductual.

---

## ⚙️ Cómo Funciona

El sistema opera en un ciclo de tres fases:

1.  **Captura (Collector):** Escucha eventos de hardware a nivel de driver.
    *   *Dato:* `Key Press` en `t=16200.045`
    *   *Dato:* `Mouse Move` a `(x=500, y=200)`
2.  **Modelado (Features):** Transforma datos crudos en estadísticas.
    *   *Velocidad de tipeo:* `0.12s` (promedio)
    *   *Jitter del mouse:* `2.4º` (desviación angular)
3.  **Inferencia (Brain):** Un modelo **Isolation Forest** determina si el comportamiento actual pertenece al dueño legítimo o es una anomalía.

---

## 🚀 Instalación

Requiere Python 3.8 o superior.

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/sanb-mov/ShadowPrint-AI
   cd ShadowPrint-AI
   ```

2. **Crear entorno virtual (Recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
**Posible error de las librerias**
Depende de la versión de Python que tengas, algunas librerías pueden no funcionar.

  ```En tal caso utiliza este comando
  pip install pandas scikit-learn pynput numpy joblib colorama
  ```
---

## 🕹️ Uso

El sistema se controla desde `main.py` con tres modos de operación:

### 1. Grabar tu Perfil (`record`)
Usa este modo para "enseñarle" al sistema quién eres. Úsalo mientras trabajas normalmente (escribiendo correos, programando, navegando) durante 5-10 minutos.

```bash
python main.py record
```
> *Presiona `CTRL+C` para detener la grabación y guardar los datos en `data/raw_behavior.csv`.*

### 2. Entrenar la IA (`train`)
Genera el modelo matemático basado en los datos recolectados.

```bash
python main.py train
```
> *Esto creará el archivo `data/user_model.pkl`.*

### 3. Vigilancia Activa (`watch`)
Inicia el monitor en tiempo real. Si detecta un patrón ajeno al tuyo, lanzará alertas.

```bash
python main.py watch
```

---

## 📂 Estructura del Proyecto

```text
ShadowPrintAI/
├── data/                 # Almacenamiento de logs y modelos
│   ├── raw_behavior.csv  # Dataset crudo (tu huella)
│   └── user_model.pkl    # Modelo de IA entrenado
├── src/
│   ├── collector.py      # Captura de eventos (Pynput)
│   ├── features.py       # Ingeniería de características (Matemáticas)
│   └── model.py          # Lógica de detección de anomalías
├── main.py               # CLI y Orquestador
└── requirements.txt      # Dependencias
```

---

## 🛡️ Nota de Privacidad y Ética

**ShadowPrint AI NO ES UN SPYWARE.**

*   El código fuente en `src/collector.py` demuestra explícitamente que **se ignoran los caracteres** de las teclas presionadas.
*   `_on_key_press(key)`: El valor de `key` se descarta; solo se almacena `time.time()`.
*   El archivo CSV resultante contiene solo números abstractos que **no pueden** ser revertidos para obtener el texto original.

---

## 🧪 Ajuste de Sensibilidad

Si el sistema no te reconoce (falsos positivos) o es demasiado permisivo, ajusta el parámetro `contamination` en `src/model.py`:

```python
# contamination=0.01  -> Muy permisivo (solo detecta bots o comportamientos muy extraños)
# contamination=0.10  -> Muy estricto (alta seguridad, requiere comportamiento consistente)
self.model = IsolationForest(..., contamination=0.05)
```

---

## 📝 Roadmap

*   [x] MVP: Captura y Detección Básica.
*   [ ] Análisis de Dígrafos (Tiempos específicos entre pares de teclas como 'Ctrl'+'C').
*   [ ] API Rest para separar el cliente de recolección del servidor de análisis.
*   [ ] Bloqueo automático de sesión en Windows/Linux ante intrusiones.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---
*Desarrollado con fines educativos y de investigación en Biometría Conductual.*
```
