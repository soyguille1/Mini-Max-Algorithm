import random
import pygame

tamanho_de_tablero = 8 
tamanho_de_celda = 50
tamanho_de_ventana = tamanho_de_tablero * tamanho_de_celda

tabla = (255, 255, 255)
Raton = (0, 0, 255)  
Gato = (255, 0, 0) 
Escape = (0, 255, 0) 
celda1 = (240, 240, 240)
celda2 = (200, 200, 200)

#               Arriba    Abajo    Izq     Der
MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

MAX_PROFUNDIDAD = 3  

pygame.init()

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((tamanho_de_ventana, tamanho_de_ventana)) 
        pygame.display.set_caption("Gato y Ratón")
        self.clock = pygame.time.Clock() 
        self.posicion_raton = self.posicion_aleatoria()
        self.posicion_gato = self.posicion_aleatoria()
        self.posicion_escape = random.choice([(0, 0), (0, tamanho_de_tablero - 1), (tamanho_de_tablero - 1, 0), (tamanho_de_tablero - 1, tamanho_de_tablero - 1)])

        while (self.posicion_gato == self.posicion_escape or 
               self.posicion_raton == self.posicion_escape or 
               self.distancia(self.posicion_gato, self.posicion_escape) <= 1 or 
               self.distancia(self.posicion_raton, self.posicion_escape) <= 1 or
               self.posicion_gato == self.posicion_raton):
            self.posicion_raton = self.posicion_aleatoria()
            self.posicion_gato = self.posicion_aleatoria()

        self.movimientos_anteriores_raton = []
        self.movimientos_anteriores_gato = []

    def posicion_aleatoria(self):
        return (random.randint(0, tamanho_de_tablero - 1), random.randint(0, tamanho_de_tablero - 1))

    def distancia(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def dibujar_tablero(self):
        self.pantalla.fill(tabla)
        for i in range(tamanho_de_tablero):
            for j in range(tamanho_de_tablero):
                # Alterna colores de las celdas
                color = celda1 if (i + j) % 2 == 0 else celda2
                pygame.draw.rect(self.pantalla, color, (i * tamanho_de_celda, j * tamanho_de_celda, tamanho_de_celda, tamanho_de_celda))

        pygame.draw.rect(self.pantalla, Escape, (self.posicion_escape[0] * tamanho_de_celda, self.posicion_escape[1] * tamanho_de_celda, tamanho_de_celda, tamanho_de_celda))
        pygame.draw.circle(self.pantalla, Raton, (self.posicion_raton[0] * tamanho_de_celda + tamanho_de_celda // 2, self.posicion_raton[1] * tamanho_de_celda + tamanho_de_celda // 2), tamanho_de_celda // 3)
        pygame.draw.circle(self.pantalla, Gato, (self.posicion_gato[0] * tamanho_de_celda + tamanho_de_celda // 2, self.posicion_gato[1] * tamanho_de_celda + tamanho_de_celda // 2), int(tamanho_de_celda // 2.5))

        pygame.display.flip()

    def mover_raton(self):
        _, proximo_movimiento = self.minimax(self.posicion_raton, self.posicion_gato, True, 0) #posicion actual
        if proximo_movimiento:
            self.posicion_raton = proximo_movimiento

        self.dibujar_tablero()

        if self.posicion_raton == self.posicion_gato:
            self.terminar_juego("¡El gato atrapó al ratón!")
        elif self.posicion_raton == self.posicion_escape:
            self.terminar_juego("¡El ratón escapó!")

    def mover_gato(self):
        _, proximo_movimiento = self.minimax(self.posicion_raton, self.posicion_gato, False, 0)
        if proximo_movimiento:
            self.posicion_gato = proximo_movimiento
            self.movimientos_anteriores_gato.append(proximo_movimiento)
            if len(self.movimientos_anteriores_gato) > 4:
                self.movimientos_anteriores_gato.pop(0)

    def terminal(self, posicion_raton, posicion_gato, profundidad):
        return posicion_raton == posicion_gato or posicion_raton == self.posicion_escape or profundidad >= MAX_PROFUNDIDAD

    def evaluar(self, posicion_raton, posicion_gato):
        # Devuelve una evaluación del estado del juego
        if posicion_raton == self.posicion_escape:
            return 1000000  # El ratón ha escapado
        elif posicion_raton == posicion_gato:
            return -1000000  # El gato ha atrapado al ratón
        else:
            # Evaluación basada en la distancia al objetivo
            distancia_raton_escape = self.distancia(posicion_raton, self.posicion_escape)
            distancia_gato_raton = self.distancia(posicion_gato, posicion_raton)
            return (distancia_gato_raton - distancia_raton_escape) 

    def minimax(self, posicion_raton, posicion_gato, maximizando, profundidad):
        if self.terminal(posicion_raton, posicion_gato, profundidad):
            return self.evaluar(posicion_raton, posicion_gato), None 
        if maximizando:
            max_eval = float('-inf') 
            mejor_movimiento = None 
            for movimiento in MOVIMIENTOS:
                nuevo_raton = (posicion_raton[0] + movimiento[0], posicion_raton[1] + movimiento[1]) 
                if (0 <= nuevo_raton[0] < tamanho_de_tablero and 0 <= nuevo_raton[1] < tamanho_de_tablero and 
                    nuevo_raton not in self.movimientos_anteriores_raton):
                    #verifica si el movimiento esta dentro de los limites y si no ha sido visitao
                    evaluacion, _ = self.minimax(nuevo_raton, posicion_gato, False, profundidad + 1)
                    if evaluacion > max_eval:
                        max_eval = evaluacion
                        mejor_movimiento = nuevo_raton 
            return max_eval, mejor_movimiento
        else:
            min_eval = float('inf')
            mejor_movimiento = None
            for movimiento in MOVIMIENTOS:
                nuevo_gato = (posicion_gato[0] + movimiento[0], posicion_gato[1] + movimiento[1])
                if (0 <= nuevo_gato[0] < tamanho_de_tablero and 0 <= nuevo_gato[1] < tamanho_de_tablero and 
                    nuevo_gato not in self.movimientos_anteriores_gato):
                    evaluacion, _ = self.minimax(posicion_raton, nuevo_gato, True, profundidad + 1)
                    if evaluacion < min_eval:
                        min_eval = evaluacion
                        mejor_movimiento = nuevo_gato
            return min_eval, mejor_movimiento

    def terminar_juego(self, mensaje):
        print(mensaje)
        pygame.time.wait(2000)
        pygame.quit()
        quit()

    def jugar(self):
        corriendo = True
        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
            self.mover_gato()
            self.dibujar_tablero()
            if self.posicion_gato == self.posicion_raton:
                self.terminar_juego("¡El gato atrapó al ratón!")
            else:
                self.mover_raton()

            self.clock.tick(1)
        pygame.quit()

if __name__ == "__main__":
    # Iniciar el juego
    juego = Juego()
    juego.jugar()
