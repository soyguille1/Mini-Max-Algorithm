import random
import pygame

tamanho_de_tablero = 8 
tamanho_de_celda = 50
tamanho_de_ventana = tamanho_de_tablero * tamanho_de_celda

tabla = (255, 255, 255)  # Blanco para el fondo del tablero
Raton = (0, 0, 255)  # Azul para el ratón
Gato = (255, 0, 0)  # Rojo para el gato
Escape = (0, 255, 0)  # Verde para la posición de escape
celda1 = (240, 240, 240)  # Gris claro para celdas alternadas
celda2 = (200, 200, 200)  # Gris oscuro para celdas alternadas

#               Arriba    Abajo    Izq     Der
MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

MAX_PROFUNDIDAD = 3  # Profundidad máxima para la recursión

pygame.init()

class Juego:
    def __init__(self):
        self.pantalla = pygame.display.set_mode((tamanho_de_ventana, tamanho_de_ventana))  # Crear ventana del tamaño especificado
        pygame.display.set_caption("Gato y Ratón")  # Nombre de la ventana
        self.clock = pygame.time.Clock()  # Controlar el tiempo del juego
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
        # Devuelve posición aleatoria  (fila, columna) dentro del tablero

    def distancia(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def dibujar_tablero(self): #investigar por que for de for
        self.pantalla.fill(tabla)
        # Dibuja el tablero y las posiciones de los jugadores y el punto de escape
        for i in range(tamanho_de_tablero):
            for j in range(tamanho_de_tablero):
                # Alterna colores de las celdas
                color = celda1 if (i + j) % 2 == 0 else celda2
                pygame.draw.rect(self.pantalla, color, (i * tamanho_de_celda, j * tamanho_de_celda, tamanho_de_celda, tamanho_de_celda))

        # Dibujar la posición de escape
        pygame.draw.rect(self.pantalla, Escape, (self.posicion_escape[0] * tamanho_de_celda, self.posicion_escape[1] * tamanho_de_celda, tamanho_de_celda, tamanho_de_celda))

        # Dibujar el ratón
        pygame.draw.circle(self.pantalla, Raton, (self.posicion_raton[0] * tamanho_de_celda + tamanho_de_celda // 2, self.posicion_raton[1] * tamanho_de_celda + tamanho_de_celda // 2), tamanho_de_celda // 3)

        # Dibujar el gato
        pygame.draw.circle(self.pantalla, Gato, (self.posicion_gato[0] * tamanho_de_celda + tamanho_de_celda // 2, self.posicion_gato[1] * tamanho_de_celda + tamanho_de_celda // 2), int(tamanho_de_celda // 2.5))

        pygame.display.flip()

    def mover_raton(self):
        # Usa Minimax para decidir el próximo movimiento
        _, proximo_movimiento = self.minimax(self.posicion_raton, self.posicion_gato, True, 0) #posicion actual
        if proximo_movimiento:
            self.posicion_raton = proximo_movimiento

        # Redibuja el tablero después del movimiento del ratón
        self.dibujar_tablero()

        # Verifica si el juego ha terminado
        if self.posicion_raton == self.posicion_gato:
            self.terminar_juego("¡El gato atrapó al ratón!")
        elif self.posicion_raton == self.posicion_escape:
            self.terminar_juego("¡El ratón escapó!")

    def mover_gato(self):
        # Usa Minimax para decidir el próximo movimiento
        _, proximo_movimiento = self.minimax(self.posicion_raton, self.posicion_gato, False, 0) #por que el guin bajo
        if proximo_movimiento:
            self.posicion_gato = proximo_movimiento
            self.movimientos_anteriores_gato.append(proximo_movimiento)
            if len(self.movimientos_anteriores_gato) > 4:  # Limitar el historial de movimientos
                self.movimientos_anteriores_gato.pop(0)

    def terminal(self, posicion_raton, posicion_gato, profundidad):# Devuelve True si el juego ha terminado o se ha alcanzado la profundidad máxima
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
            return (distancia_gato_raton - distancia_raton_escape)  # El ratón busca minimizar, el gato maximizar

    def minimax(self, posicion_raton, posicion_gato, maximizando, profundidad):
        if self.terminal(posicion_raton, posicion_gato, profundidad):
            return self.evaluar(posicion_raton, posicion_gato), None 
#por ejemplo, el gato captura al ratón o se agotan los movimientos
        if maximizando:
            max_eval = float('-inf') #Garantiza que el algoritmo encontrará el valor máximo posible al comparar todas las evaluaciones.
            #en la maximizacion este es el valor mas pequenho que no puede ser expresado
            mejor_movimiento = None #si no se encontro  el mejor movimiento
            for movimiento in MOVIMIENTOS:
                nuevo_raton = (posicion_raton[0] + movimiento[0], posicion_raton[1] + movimiento[1]) 
                #Calcula la posi del r luego de hacer un movimiento
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
                #posicion coordenada x y y
                nuevo_gato = (posicion_gato[0] + movimiento[0], posicion_gato[1] + movimiento[1])
                #verificar si esta adentro de los limites del tablero
                if (0 <= nuevo_gato[0] < tamanho_de_tablero and 0 <= nuevo_gato[1] < tamanho_de_tablero and 
                    nuevo_gato not in self.movimientos_anteriores_gato):
                    evaluacion, _ = self.minimax(posicion_raton, nuevo_gato, True, profundidad + 1)
                    #Evalua el estado del juegoen niveles profundos del arbol de decisiones para la mejor
                    if evaluacion < min_eval:
                        min_eval = evaluacion
                        mejor_movimiento = nuevo_gato
            return min_eval, mejor_movimiento
        #todas las posibles posiciones del ratón y el gato para determinar el mejor movimiento posible,
        #  dependiendo de si se está maximizando (ratón) o minimizando (gato). Utiliza un enfoque recursivo 
        # para explorar todas las opciones posibles hasta llegar a una condición terminal o alcanzar la profundidad máxima
        #  permitida. Luego, evalúa estas posiciones y selecciona la mejor opción según el criterio de maximización o minimización

    def terminar_juego(self, mensaje):
        # Termina el juego mostrando un mensaje y cerrando Pygame
        print(mensaje)
        pygame.time.wait(2000)
        pygame.quit()
        quit()

    def jugar(self):
        # Bucle principal del juego
        corriendo = True
        while corriendo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False

            # Mover el gato y redibujar el tablero
            self.mover_gato()
            self.dibujar_tablero()
            if self.posicion_gato == self.posicion_raton:
                self.terminar_juego("¡El gato atrapó al ratón!")
            else:
                self.mover_raton()

            self.clock.tick(1)  # Controla la velocidad del juego (1 FPS)

        pygame.quit()

if __name__ == "__main__":
    # Iniciar el juego
    juego = Juego()
    juego.jugar()
#Backtraking