import pygame
import math
import random
import string
import numpy as np
import matplotlib.pyplot as plt
pygame.init()

# Configuración de pantalla
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulación de vehículo en hielo con ray-casting")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN =(0,250,0)
 # Cargar imagen del coche (opcional: crear una simple si no tienes)
car_image = pygame.Surface((50, 30), pygame.SRCALPHA)  # Crear superficie de 50x30 (transparente)
pygame.draw.polygon(car_image, RED, [(0, 0), (50, 15), (0, 30)])  # Dibujar una forma de coche triangular

# Cargar imagen de la pista
track_image = pygame.image.load("Race.png").convert()  # Asegúrate de tener la imagen en la misma carpeta o proporcionar la ruta correcta
track_image = pygame.transform.scale(track_image, (screen_width, screen_height))  # Escalar imagen al tamaño de la pantalla

clock = pygame.time.Clock()
# Configuración del vehículo
class theCar:

      # Velocidad de giro

   
    def __init__(self,wa:float,wb:float,wc:float,nm:str) -> None:
        self.name = nm
        self.car_pos = [400, 120]  # Posición inicial del coche
        self.car_angle = 0         # Ángulo inicial (en grados)
        self.car_speed = 0         # Velocidad del coche
        self.max_speed = 15         # Velocidad máxima
        self.acceleration = 0.05   # Aceleración del coche
        self.friction = 0.02       # Fricción simulada
        self.turn_speed = 3
        self.lifeTime=300
        self.stopTime=0
        self.weights =[wa,wb,wc]
        self.score = 0.1
        self.isLife=True  
    def __str__(self):
        return self.name
    def reset(self):
        self.car_pos = [400, 120]  # Posición inicial del coche
        self.car_angle = 0         # Ángulo inicial (en grados)
        self.car_speed = 0         # Velocidad del coche
        self.max_speed = 10         # Velocidad máxima
        self.acceleration = 0.05   # Aceleración del coche
        self.friction = 0.02       # Fricción simulada
        self.turn_speed = 3
        self.lifeTime=300
        self.stopTime=0
        self.score = 0.1
        self.isLife=True  
    def _kill(self):
        self.isLife=False
    # Función para manejar los movimientos del coche

    def move_car(self):
        self.lifeTime-=1
        if self.lifeTime<0:
            self._kill()
        global car_speed, car_angle

        # Aplicar fricción
        if self.car_speed > 0:
            self.car_speed = max(0, self.car_speed - self.friction)
        elif self.car_speed < 0:
            self.car_speed = min(0, self.car_speed + self.friction)
        if self.car_speed<0:
            self._kill()
        # Actualizar posición del coche según la dirección y velocidad
        self.car_pos[0] += math.cos(math.radians(self.car_angle)) * self.car_speed
        self.car_pos[1] -= math.sin(math.radians(self.car_angle)) * self.car_speed

    # Función para lanzar rayos desde el coche y detectar distancias
    def cast_rays(self):
        ray_length = 300
        ray_offsets = [0, -90 ]
        distances = []

        for offset in ray_offsets:
            ray_angle = math.radians(self.car_angle + offset)
            ray_x = self.car_pos[0]
            ray_y = self.car_pos[1]

            for _ in range(ray_length):
                ray_x += math.cos(ray_angle)
                ray_y -= math.sin(ray_angle)

                if 0 <= int(ray_x) < screen_width and 0 <= int(ray_y) < screen_height:
                    # Verificar si el píxel en la imagen de la pista es negro
                    if track_image.get_at((int(ray_x), int(ray_y))) == BLACK:
                        break
                else:
                    break  # Salir del bucle si el rayo se sale de los límites
            
            distance = math.sqrt((ray_x - self.car_pos[0]) ** 2 + (ray_y - self.car_pos[1]) ** 2)
            if distance<1:
                self.score+= 1-(self.lifeTime/300)
                self._kill()
            distances.append(distance/ray_length)
            pygame.draw.line(screen, BLUE, self.car_pos, (ray_x, ray_y), 1)  # Dibujar el rayo
        if distances[0]<self.weights[0]:
            self.car_speed = max(self.car_speed - self.acceleration, -self.max_speed / 2)  # Frenar (marcha atrás)
        else:
            self.car_speed = min(self.car_speed + self.acceleration, self.max_speed)
        if distances[1]<self.weights[1]:
            self.car_angle += self.turn_speed
        elif distances[1]>self.weights[2]:
            self.car_angle -= self.turn_speed
        mini_ray_lenght = 10
        mini_ray_angle = math.radians(self.car_angle)
        ray_x = self.car_pos[0]
        ray_y = self.car_pos[1]
        for _ in range(mini_ray_lenght):
            ray_x += math.cos(mini_ray_angle)
            ray_y -= math.sin(mini_ray_angle)

            if 0 <= int(ray_x) < screen_width and 0 <= int(ray_y) < screen_height:
                # Verificar si el píxel en la imagen de la pista es negro
                if track_image.get_at((int(ray_x), int(ray_y))) == GREEN and self.lifeTime<280:
                    self.score+=self.lifeTime/300
                    self.score+=1
                    self.lifeTime=300
                    break
            else:
                break  # Salir del bucle si el rayo se sale de los límites
plt.ion()  # Hacer la gráfica interactiva
fig, ax = plt.subplots()
data_inicial = np.zeros((240, 180))
heatmap = ax.imshow(data_inicial, cmap='hot')
plt.colorbar(heatmap)
def update_graph(data):
    # Actualizar los datos del heatmap
    heatmap.set_data(data)
    
    # Ajustar los límites de la escala de colores según los valores actuales
    heatmap.set_clim(vmin=np.min(data), vmax=np.max(data))
    
    plt.draw()
    plt.pause(0.00001)

def generar_string_aleatorio():
    letras = string.ascii_letters  # Incluye letras mayúsculas y minúsculas
    string_aleatorio = ''.join(random.choice(letras) for _ in range(6))
    return string_aleatorio

# Bucle principal del juego
champion = None
envArr = []
ARR_SIZE=70
ELITE = 3
for i in range(0,ARR_SIZE,1):
    
    wa=random.random()
    wb=random.random()
    wc=random.random()
    if wb<wc:
        newCar = theCar(wa,wb,wc,generar_string_aleatorio())
    else:
        newCar = theCar(wa,wc,wb,generar_string_aleatorio())
    envArr.append(newCar)
def sort_by_score(x:theCar):
    return x.score

data = np.zeros((240, 180))

# Dimensiones del mapa de calor
running = True
generation=0
time=0
prosArr=[]
while running:
    time+=1
    if time>60:
        envArr.sort(key=sort_by_score)
        prosArr=envArr[-1:-6:-1]
        time=0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mover el coche
    font = pygame.font.SysFont(None, 20)
    # Dibujar todo en la pantalla
    screen.blit(track_image, (0, 0))  # Dibujar la imagen de la pista
    cementary = 0
    for i in envArr:
        if not i.isLife:
            cementary+=1
            continue
        i.cast_rays()
        i.move_car()
    # Rotar el coche en función del ángulo
        rotated_car = pygame.transform.rotate(car_image, i.car_angle)
        car_rect = rotated_car.get_rect(center=(i.car_pos[0], i.car_pos[1]))

        name_text = font.render(i.name, True,(120,120,120))
        

    # Incrementar el valor en la posición seleccionada
        if i.score>1:
            mapped_x = int(i.car_pos[0]*0.3)
            mapped_y = int(i.car_pos[1]*0.3)
            if mapped_x>=240:
                mapped_x=239
            if mapped_y>=180:
                mapped_y=179
            data[mapped_x, mapped_y] += i.score+generation
        # Dibujar el coche en su nueva posición
        screen.blit(rotated_car, car_rect.topleft)
        screen.blit(name_text,(i.car_pos[0],i.car_pos[1]))
    # Lanzar rayos y detectar distancias
    gen_text = font.render("Generation:"+str(generation),  True, RED)
    list = ""
    pos_y=50
    for i in prosArr:
        list= i.name+": "+str(i.score)
        list_text = font.render(list,True,RED)
        screen.blit(list_text, (50, 50+pos_y))
        pos_y+=10
    screen.blit(gen_text, (50, 50))
    
    if cementary>=ARR_SIZE:
        update_graph(data)
        generation+=1
        envArr.sort(key=sort_by_score)
        eliteArr = envArr[-ELITE:]
        newGenArr=[]
        scoreArr=[]
        for i in envArr:
            scoreArr.append(i.score)

        the_tuple = tuple(scoreArr)
        if ARR_SIZE>25:
            ARR_SIZE-=5
        for i in range(0,ARR_SIZE-ELITE,1):
            father = random.choices(envArr,weights=the_tuple)[0]
            mother = random.choices(envArr,weights=the_tuple)[0]
            while father == mother:
                mother = random.choices(envArr,weights=the_tuple)[0]
            index = random.randint(1,3)
            mutIndex = random.randint(0,2)
            newGenetics = father.weights[:index]+mother.weights[index:]
            mid = ( father.weights[mutIndex]+mother.weights[mutIndex])/2
            dif = abs(father.weights[mutIndex]-mother.weights[mutIndex])/2
            newGenetics[mutIndex] = random.normalvariate(mid,dif)
            if newGenetics[mutIndex]>1:newGenetics[mutIndex]=1
            if newGenetics[mutIndex]<0:newGenetics[mutIndex]=0
            if newGenetics[0]<newGenetics[1]:
                newGenArr.append(theCar(newGenetics[0],newGenetics[1],newGenetics[2],generar_string_aleatorio()))
            else:
                 newGenArr.append(theCar(newGenetics[1],newGenetics[0],newGenetics[2],generar_string_aleatorio()))
        for i in eliteArr:
            i.reset()
        envArr = eliteArr+newGenArr

    pygame.display.flip()
    clock.tick(60)

pygame.quit()