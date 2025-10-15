import random as rd
class JugadorIA:
    def __init__(self, estrategia="optima"):
        self.estrategia = estrategia

    def decidir_jugada(self, palitos, palitos_max):
        if self.estrategia == "dificil":
            return self.jugada_optima(palitos,palitos_max)
        elif self.estrategia == "facil":
            return self.jugada_aleatoria(palitos,palitos_max)

    def jugada_optima(self, restantes, palitos_max):
        # estrategia para los ultimos palitos
        if restantes <= palitos_max + 1:
            if restantes == 1:
                # Nos toca tomar el último - hemos perdido
                return 1
            else:
                # Dejamos exactamente 1 palito al oponente
                return restantes - 1
        
        # Estrategia general para misère Nim
        optimo = (restantes - 1) % (palitos_max + 1)
        
        if optimo == 0:
            # Posición perdedora
            return rd.randint(1, min(restantes, palitos_max))
        else:
            # Posición ganadora
            return optimo
    
    def jugada_aleatoria(self,palitos,palitos_max):
        cantidad = rd.randrange(1, min(palitos,palitos_max+1))
        return cantidad