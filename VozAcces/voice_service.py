import speech_recognition as sr

class VoiceService:
    """
    Patrón Facade para ocultar la complejidad de SpeechRecognition y PyAudio.
    Proporciona una interfaz simple para capturar y traducir voz.
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def capturar_voz(self, timeout=3, phrase_time_limit=3):
        """
        Escucha a través del micrófono con límites estrictos de tiempo.
        Retorna (texto, confianza) o (None, 0).
        """
        try:
            with self.microphone as source:
                print(f"Escuchando (Límite: {phrase_time_limit}s)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            # Usando Google Web Speech API (requiere internet)
            # Para uso off-line se podría usar Sphinx o similar.
            resultado = self.recognizer.recognize_google(audio, language="es-ES", show_all=True)
            
            if not resultado or 'alternative' not in resultado:
                return None, 0
                
            mejor_opcion = resultado['alternative'][0]
            texto = mejor_opcion['transcript']
            confianza = mejor_opcion.get('confidence', 0.8) # Algunas respuestas no traen confianza
            
            return texto.lower().strip(), confianza

        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
        except sr.RequestError as e:
            print(f"Error en el servicio de reconocimiento: {e}")
        except Exception as e:
            print(f"Error inesperado al capturar voz: {e}")
            
        return None, 0
