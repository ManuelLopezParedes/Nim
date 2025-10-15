class Logica:
    @staticmethod
    def es_jugada_valida(cantidad, palitos_restantes, palitos_max):
        """Verifica si una jugada es válida"""
        return 1 <= cantidad <= min(palitos_restantes, palitos_max)
    
    @staticmethod
    def es_juego_terminado(palitos_restantes):
        """Verifica si el juego ha terminado"""
        return palitos_restantes <= 0
    
    @staticmethod
    def obtener_ganador(turno_actual, modo_juego):
        """
        Determina el ganador basado en quién tomó el último palito
        El que tomó el último palito pierde
        """
        # El ganador es el jugador que NO estaba en el turno actual
        # porque el turno actual fue el que tomó el último palito
        if modo_juego == 1:  # JvsJ
            return "Jugador 1" if not turno_actual else "Jugador 2"
        else:  # JvsCPU
            return "Jugador 1" if not turno_actual else "CPU"
    
    @staticmethod
    def get_current_player(turno_j1, modo_juego):
        """Obtiene el nombre del jugador actual"""
        if turno_j1:
            return "Jugador 1"
        else:
            return "Jugador 2" if modo_juego == 1 else "CPU"