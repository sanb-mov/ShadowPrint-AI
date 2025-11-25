import time
import threading
from pynput import keyboard, mouse

class DataCollector:
    def __init__(self):
        self.events = []
        self.running = False
        self.start_time = time.time()
        # Locks para evitar conflictos entre hilos
        self.lock = threading.Lock()

    def _on_key_press(self, key):
        if not self.running: return False
        with self.lock:
            # Registramos EVENTO y TIMESTAMP. No la tecla.
            self.events.append({
                'type': 'key_press',
                'time': time.time()
            })

    def _on_key_release(self, key):
        if not self.running: return False
        with self.lock:
            self.events.append({
                'type': 'key_release',
                'time': time.time()
            })
        if key == keyboard.Key.esc:
            # Opción de salida de emergencia si se desea
            pass

    def _on_move(self, x, y):
        if not self.running: return False
        with self.lock:
            self.events.append({
                'type': 'mouse_move',
                'time': time.time(),
                'x': x,
                'y': y
            })

    def _on_click(self, x, y, button, pressed):
        if not self.running: return False
        with self.lock:
            action = 'mouse_click_down' if pressed else 'mouse_click_up'
            self.events.append({
                'type': action,
                'time': time.time(),
                'x': x,
                'y': y
            })

    def start_listening(self):
        self.running = True
        self.events = [] # Limpiar buffer
        
        # Iniciar listeners en modo no bloqueante
        self.k_listener = keyboard.Listener(on_press=self._on_key_press, on_release=self._on_key_release)
        self.m_listener = mouse.Listener(on_move=self._on_move, on_click=self._on_click)
        
        self.k_listener.start()
        self.m_listener.start()
        print(">>> Collector iniciado. Escuchando patrones biométricos...")

    def stop_listening(self):
        self.running = False
        if hasattr(self, 'k_listener'): self.k_listener.stop()
        if hasattr(self, 'm_listener'): self.m_listener.stop()
        print(f">>> Collector detenido. Eventos capturados: {len(self.events)}")
        return self.events

    def get_buffer_and_clear(self):
        """Obtiene datos actuales y limpia para la siguiente ventana de tiempo (Real-time)"""
        with self.lock:
            buffer_copy = list(self.events)
            self.events = []
            return buffer_copy