#Proyecto 3
#Andrea Elias


#Se importan las librerias necesarias para el proyecto
import os 
import pygame
import pyglet
from math import pi, cos, sin, atan2

#Variables del personaje y el mundo
CLOCK = pygame.time.Clock()
tamanioPantalla = 250
mitadPantalla = 125
zoom = 70
ubicacionInicialX = 20
ubicacionInicialY = 20
tamanioBloque = 50
anguloApertura = pi/3
anguloInicialRotacion = 0
colorNegro = 0.1
tamanioSprite = 256
tamanioPersonaje = 32
resolucionPersonaje = 102


#Cargas de imagenes de texturas
poster1 = pygame.image.load('./alfombraWall.png')
poster2 = pygame.image.load('./blue.png')
poster3 = pygame.image.load('./gold.png')
poster4 = pygame.image.load('./jasmineWall.png')
poster5 = pygame.image.load('./sultanWall.png')
poster6 = pygame.image.load('./genieWall.png')
poster7 = pygame.image.load('./abuWall.png')
poster8 = pygame.image.load('./rajahWall.png')
Coins = pygame.image.load('./coinsBowlWall.png')

#Asignacion de imagenes en un diccionario
textures = {
  "1": poster1,
  "2": poster2,
  "3": Coins,
  "4": poster3,
  "5": poster4,
  "6": poster5,
  "7": poster6,
  "8": poster7,
  "9": poster8
}

#Carga de imagenes de la mano
hand = pygame.image.load('./playerLamp.png')
hand1 = pygame.image.load('./playerLamp.png')
hand2 = pygame.image.load('./threeCoins.png')
hand3 = pygame.image.load('./twoCoins.png')
hand4 = pygame.image.load('./OneCoin.png')
hand5 = pygame.image.load('./emptyHand.png')

#Carga de imagenes de sprites en sus posiciones en un arreglo de diccionarios 
enemies = [
  {
    "x": 920,
    "y": 175,
    "texture": pygame.image.load('./meditatingMonk.png')
  },
  {
    "x": 275,
    "y": 170,
    "texture": pygame.image.load('./camel2.png')
  },
  {
    "x": 1375,
    "y": 160,
    "texture": pygame.image.load('./jafarPix.png')
  },
  {
    "x": 830,
    "y": 280,
    "texture": pygame.image.load('./muslim.png')
  },
  {
    "x": 175,
    "y": 510,
    "texture": pygame.image.load('./iago.png')
  },
  {
    "x": 175,
    "y": 235,
    "texture": pygame.image.load('./prayingMonk.png')
  },
  {
    "x": 90,
    "y": 625,
    "texture": pygame.image.load('./sultan2.png')
  },
  {
    "x": 915,
    "y": 480,
    "texture": pygame.image.load('./flautista.png')
  },
  {
    "x": 1430,
    "y": 590,
    "texture": pygame.image.load('./servamt2.png')
  },
  {
    "x": 1430,
    "y": 290,
    "texture": pygame.image.load('./meditate.png')
  }
]

#Metodo para iniciar el Raycaster en donde se crean las variables basicas del raycaster
class Raycaster(object):

  def __init__(self, screen):
    _, _, self.width, self.height = screen.get_rect()
    self.screen = screen
    self.blocksize = tamanioBloque
    self.player = {
      "x": self.blocksize + ubicacionInicialX,
      "y": self.blocksize + ubicacionInicialY,
      "a": anguloInicialRotacion,
      "fov": anguloApertura
    }
    self.map = []
    self.zbuffer = [-float('inf') for _ in range(0,tamanioPantalla)]

  #Metodo para limpiar el fondo con un solo color
  def clear(self):
    self.screen.fill((colorNegro,colorNegro,colorNegro))

  #Metodo dibujar puntos
  def point(self, x, y, c = None):
    screen.set_at((x, y), c)

  #Metodo leer el mapa del juego en un archivo .txt
  def load_map(self, filename):
    with open(filename) as f:
      for line in f.readlines():
        self.map.append(list(line))

  #Metodo lanzar rayos del personajes a los objetos del mapa y calcular variables de distancia, mapeo y tx
  def cast_ray(self, a):
    d = 0
    while True:
      x = self.player["x"] + d*cos(a)
      y = self.player["y"] + d*sin(a)

      i = int(int(x)/tamanioBloque)
      j = int(int(y)/tamanioBloque)

      if self.map[j][i] != ' ':
        hitx = x - i*tamanioBloque
        hity = y - j*tamanioBloque

        if 1 < hitx < 49:
          maxhit = hitx
        else:
          maxhit = hity

        tx = int(maxhit * tamanioSprite/tamanioBloque)
        return d, self.map[j][i], tx

      d += 1

  #Metodo renderizar las paredes del juego
  def draw_stake(self, x, h, texture, tx):
    start = int(mitadPantalla - h/2)
    end = int(mitadPantalla + h/2)
    for y in range(start, end):
      ty = int((y - start) * tamanioSprite/(end - start))
      c = texture.get_at((tx,ty))
      self.point(x, y, c)

  
  

  #Metodo renderizar a cada sprite o enemigo
  def draw_sprite(self, sprite):
    sprite_a = atan2(sprite["y"] - self.player["y"], sprite["x"] - self.player["x"])
    sprite_d = ((self.player["x"] - sprite["x"])**2 + (self.player["y"] - sprite["y"])**2)**(1/2)
    sprite_size = (tamanioPantalla/sprite_d) * zoom
    sprite_x = (tamanioPantalla*(sprite_a - self.player["a"])/self.player["fov"] + mitadPantalla - sprite_size/2)
    sprite_y = (mitadPantalla - sprite_size/2)

    sprite_x = int(sprite_x)
    sprite_y = int(sprite_y)
    sprite_size = int(sprite_size)

    #Aqui se va recorriendo el sprite y se va obteniendo el color de la imagen para ser renderizado
    for x in range(sprite_x, sprite_x + sprite_size):
      for y in range(sprite_y, sprite_y + sprite_size):
        if 0 < x < tamanioPantalla and self.zbuffer[x] >= sprite_d:
          tx = int((x - sprite_x) * tamanioSprite/sprite_size)
          ty = int((y - sprite_y) * tamanioSprite/sprite_size)
          c = sprite["texture"].get_at((tx, ty))
          #print(c)
          if c != (47, 3, 3, 255) and c != (28, 80, 71, 255) and c != (39, 70, 89, 255) and c != (177, 159, 111, 255) and c != (216, 221, 235, 255) and c != (152, 0, 136, 255):
            self.point(x, y, c)
            self.zbuffer[x] = sprite_d

  #Metodo renderizar al jugador en primera persona
  def draw_player(self, xi, yi, w = resolucionPersonaje, h = resolucionPersonaje):
    for x in range(xi, xi + w):
      for y in range(yi, yi + h):
        tx = int((x - xi) * tamanioPersonaje/w)
        ty = int((y - yi) * tamanioPersonaje/h)
        c = hand.get_at((tx, ty))
        if c != (152, 0, 136, 255):
          self.point(x, y, c)


  def draw_rectangle(self, x, y, texture):
    for cx in range(x, x + 10):
      for cy in range(y, y + 10):
        tx = int((cx - x)*300/ 50)
        ty = int((cy - y)*300/ 50)
        c = texture.get_at((tx, ty))
        self.point(cx, cy, c)

  #Metodo renderizar los objetos que se veran en el mundo
  def render(self):
    for i in range(0, tamanioPantalla):
      a =  self.player["a"] - self.player["fov"]/2 + self.player["fov"]*i/tamanioPantalla
      d, c, tx = self.cast_ray(a)
      x = i
      h = tamanioPantalla/(d*cos(a-self.player["a"])) * zoom
      self.draw_stake(x, h, textures[c], tx)

      self.zbuffer[i] = d

   
  # #Minimap rendering
  #   for x in range(0, 100, 10):
  #     for y in range(0, 100, 10):
  #       i = int(x/10)
  #       j = int(y/10)
  #       if self.map[j][i] != ' ':
  #         y =  100 + y
  #         z = 100 + x
  #         self.draw_rectangle(z, y, textures[self.map[j][i]])

  #   self.point(int(self.player["x"] * 0.21) + 180, int(self.player["y"] * 0.21) + 180, (255,255,255))

    #Render de los enemigos
    for enemy in enemies:
      self.point(enemy["x"], enemy["y"], (0, 0, 0))
      self.draw_sprite(enemy)

    #Render del jugador
    self.draw_player(tamanioPantalla - resolucionPersonaje - 50, tamanioPantalla - resolucionPersonaje)

def mostrarFPS(clock,screen):
    string = "FPS: " + str(int(clock.get_fps()))
    font = pygame.font.SysFont('Verdana', 17,  True)
    fps = font.render(string,0,(255,105,180))
    screen.blit(fps, (150,5))


#Variables para iniciar el juego
pygame.init()
pygame.mixer.init()
#Para centrar el GameOVER
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Efectos de sonido
effectmonedas = pygame.mixer.Sound('swapCoin.wav')

effectCoins = pygame.mixer.Sound('money1.wav')

effectlordSave = pygame.mixer.Sound('lordSave.wav')

effectCambio = pygame.mixer.Sound('Cambio.wav')

#Musica de fondo
pygame.mixer.music.load("alibaba.mp3") 
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.3)

#Pantalla de Bienvenida
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Bienvenida - Agrabah')
#Se carga la pantalla de bienvenida
bienvenida = pygame.image.load("WelcomeAgrabah.png").convert()
screen.blit(bienvenida,(0,0))
pygame.display.flip()

#Render de la ventana de Bienvenida
inicio = True
while (inicio):
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        inicio = False
        pygame.display.quit()

#Pantalla de Explicacion del Juego
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('The Game - Agrabah')
#Se carga la pantalla de explicacion del juego
explicacion = pygame.image.load("theme.png").convert()
screen.blit(explicacion,(0,0))
pygame.display.flip()

#Render de la ventana de Explicacion del Juego
expli = True
while (expli):
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        expli = False
        pygame.display.quit()
        
nivel = 3

#Pantalla de Nivel
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Nivel - Agrabah')
#Se cargan las pantallas de nivel

level3 = pygame.image.load("LEVEL1.png").convert()
level4 = pygame.image.load("LEVEL2.png").convert()
level5 = pygame.image.load("LEVEL3.png").convert()

#Render de la ventana de Nivel
choose = True
while (choose):
  if nivel == 3:
    screen.blit(level3,(0,0))
    pygame.display.flip()
  elif nivel == 4:
    screen.blit(level4,(0,0))
    pygame.display.flip()
  elif nivel == 5:
    screen.blit(level5,(0,0))
    pygame.display.flip()
  

  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
      choose = False
      pygame.display.quit()
      
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        if nivel == 1:
          nivel = 5
        else:
          nivel = nivel - 1
      elif event.key == pygame.K_DOWN:
        if nivel == 5:
          nivel = 1
        else:
          nivel = nivel + 1


#Pantalla de Instrucciones
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Instrucciones - Agrabah')
#Se carga la pantalla de instrucciones
instruct = pygame.image.load("Instructions.png").convert()
screen.blit(instruct,(0,0))
pygame.display.flip()

#Render de la ventana de Instrucciones
instru = True
while (instru):
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        instru = False
        pygame.display.quit()


#Set de Pantalla de 200X200
screen = pygame.display.set_mode((tamanioPantalla, tamanioPantalla),pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.HWACCEL)
screen.set_alpha(None)
r = Raycaster(screen)
r.load_map('./mapa.txt')
contadormonedas = 3
giro = 0
monedas = False
gameOver = True

#Para que se pueda dejar presionada una tecla de direccion o rotacion
pygame.key.set_repeat(1,1)

#Puntos
punto1 = 0
punto2 = 0
punto3 = 0
punto4 = 0
punto5 = 0
punto6 = 0
punto7 = 0
punto8 = 0
punto9 = 0
punto10 = 0


      
#Corriendo el juego
while gameOver:
  r.clear()
  

  try:
    #Controles de salida del juego
    for e in pygame.event.get():
      if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
        gameOver = False
        #pygame.quit()
        #pygame.display.quit()
        #exit(0)

      #Manejo de controles de direccion y rotacion
      #Rotacion
      if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_a:
          r.player["a"] -= pi/10
          if r.player["a"] <= -11*pi/10:
            r.player["a"] = 9*pi/10
          else:
            pass
        
        elif e.key == pygame.K_d:
          r.player["a"] += pi/10
          if r.player["a"] >= 11*pi/10:
            r.player["a"] = -9*pi/10
          else:
            pass

        #Direccion
        elif e.key == pygame.K_RIGHT:
          r.player["y"] += 10*cos(r.player["a"])
          r.player["x"] += -1*10*sin(r.player["a"])
          if r.player["y"] <= 65 or r.player["y"] >= 630 or r.player["x"] <= 65 or r.player["x"] >= 1430:
            r.player["y"] -= 10*cos(r.player["a"])
            r.player["x"] -= -1*10*sin(r.player["a"])
            
        elif e.key == pygame.K_LEFT:
          r.player["y"] += -1*10*cos(r.player["a"])
          r.player["x"] += 1*10*sin(r.player["a"])
          if r.player["y"] <= 65 or r.player["y"] >= 630 or r.player["x"] <= 65 or r.player["x"] >= 1430:
            r.player["y"] -= -1*10*cos(r.player["a"])
            r.player["x"] -= 1*10*sin(r.player["a"])

        elif e.key == pygame.K_UP:
          r.player["x"] += 10*cos(r.player["a"])
          r.player["y"] += 10*sin(r.player["a"])
          if r.player["y"] <= 65 or r.player["y"] >= 630 or r.player["x"] <= 65 or r.player["x"] >= 1430:
            r.player["x"] -= 10*cos(r.player["a"])
            r.player["y"] -= 10*sin(r.player["a"])
        

        elif e.key == pygame.K_DOWN:
          r.player["x"] += -1*10*cos(r.player["a"])
          r.player["y"] += -1*10*sin(r.player["a"])
          if r.player["y"] <= 65 or r.player["y"] >= 630 or r.player["x"] <= 65 or r.player["x"] >= 1430:
            r.player["x"] -= -1*10*cos(r.player["a"])
            r.player["y"] -= -1*10*sin(r.player["a"])


        
        #Manejo de lampara magica y monedas
        elif e.key == pygame.K_SPACE:
          effectCambio.play()
          if monedas == False:
            if contadormonedas == 3:
              hand = hand2
            elif contadormonedas == 2:
              hand = hand3
            elif contadormonedas == 1:
              hand = hand4
            elif contadormonedas == 0:
              hand = hand5
            monedas = True
          else:
            hand = hand1
            monedas = False
          

        #Dejar monedas de oro
        elif e.key == pygame.K_z:
          if contadormonedas == 0:
            pass
          elif contadormonedas == 3:
            hand = hand3
            contadormonedas = contadormonedas - 1
            effectmonedas.play()
            if 870 <= r.player["x"] <= 970 and 125 < r.player["y"] <= 225: 
              effectlordSave.play()
              if punto1 != 1:
                punto1 = punto1 + 1
              else:
                pass
            elif 225 <= r.player["x"] <= 325 and 120 < r.player["y"] <= 220: 
              effectlordSave.play()
              if punto2 != 1:
                punto2 = punto2 + 1
              else:
                pass
            elif 1325 <= r.player["x"] <= 1425 and 110 < r.player["y"] <= 210: 
              effectlordSave.play()
              if punto3 != 1:
                punto3 = punto3 + 1
              else:
                pass
            elif 780 <= r.player["x"] <= 880 and 230 < r.player["y"] <= 330: 
              effectlordSave.play()
              if punto4 != 1:
                punto4 = punto4 + 1
              else:
                pass
            elif 125 <= r.player["x"] <= 225 and 460 < r.player["y"] <= 560: 
              effectlordSave.play()
              if punto5 != 1:
                punto5 = punto5 + 1
              else:
                pass
            elif 125 <= r.player["x"] <= 225 and 185 < r.player["y"] <= 285: 
              effectlordSave.play()
              if punto6 != 1:
                punto6 = punto6 + 1
              else:
                pass
            elif 40 <= r.player["x"] <= 140 and 575 < r.player["y"] <= 675: 
              effectlordSave.play()
              if punto7 != 1:
                punto7 = punto7 + 1
              else:
                pass
            elif 865 <= r.player["x"] <= 965 and 430 < r.player["y"] <= 530: 
              effectlordSave.play()
              if punto8 != 1:
                punto8 = punto8 + 1
              else:
                pass
            elif 1380 <= r.player["x"] <= 1480 and 540 < r.player["y"] <= 640:
              effectlordSave.play()
              if punto9 != 1:
                punto9 = punto9 + 1
              else:
                pass
            elif 1380 <= r.player["x"] <= 1480 and 240 < r.player["y"] <= 340:
              effectlordSave.play()
              if punto10 != 1:
                punto10 = punto10 + 1
              else:
                pass
            
          elif contadormonedas == 2:
            hand = hand4
            contadormonedas = contadormonedas - 1
            effectmonedas.play()
            if 870 <= r.player["x"] <= 970 and 135 < r.player["y"] <= 215: 
              effectlordSave.play()
              if punto1 != 1:
                punto1 = punto1 + 1
              else:
                pass
            elif 245 <= r.player["x"] <= 305 and 140 < r.player["y"] <= 200: 
              effectlordSave.play()
              if punto2 != 1:
                punto2 = punto2 + 1
              else:
                pass
            elif 1345 <= r.player["x"] <= 1405 and 130 < r.player["y"] <= 190: 
              effectlordSave.play()
              if punto3 != 1:
                punto3 = punto3 + 1
              else:
                pass
            elif 800 <= r.player["x"] <= 860 and 250 < r.player["y"] <= 310: 
              effectlordSave.play()
              if punto4 != 1:
                punto4 = punto4 + 1
              else:
                pass
            elif 145 <= r.player["x"] <= 205 and 480 < r.player["y"] <= 540: 
              effectlordSave.play()
              if punto5 != 1:
                punto5 = punto5 + 1
              else:
                pass
            elif 145 <= r.player["x"] <= 205 and 205 < r.player["y"] <= 265: 
              effectlordSave.play()
              if punto6 != 1:
                punto6 = punto6 + 1
              else:
                pass
            elif 60 <= r.player["x"] <= 120 and 595 < r.player["y"] <= 655: 
              effectlordSave.play()
              if punto7 != 1:
                punto7 = punto7 + 1
              else:
                pass
            elif 885 <= r.player["x"] <= 945 and 450 < r.player["y"] <= 510: 
              effectlordSave.play()
              if punto8 != 1:
                punto8 = punto8 + 1
              else:
                pass
            elif 1400 <= r.player["x"] <= 1460 and 560 < r.player["y"] <= 620:
              effectlordSave.play()
              if punto9 != 1:
                punto9 = punto9 + 1
              else:
                pass
            elif 1400 <= r.player["x"] <= 1460 and 260 < r.player["y"] <= 320:
              effectlordSave.play()
              if punto10 != 1:
                punto10 = punto10 + 1
              else:
                pass
              
          elif contadormonedas == 1:
            hand = hand5
            contadormonedas = contadormonedas - 1
            effectmonedas.play()
            if 870 <= r.player["x"] <= 970 and 135 < r.player["y"] <= 215: 
              effectlordSave.play()
              if punto1 != 1:
                punto1 = punto1 + 1
              else:
                pass
            elif 245 <= r.player["x"] <= 305 and 140 < r.player["y"] <= 200: 
              effectlordSave.play()
              if punto2 != 1:
                punto2 = punto2 + 1
              else:
                pass
            elif 1345 <= r.player["x"] <= 1405 and 130 < r.player["y"] <= 190: 
              effectlordSave.play()
              if punto3 != 1:
                punto3 = punto3 + 1
              else:
                pass
            elif 800 <= r.player["x"] <= 880 and 250 < r.player["y"] <= 310: 
              effectlordSave.play()
              if punto4 != 1:
                punto4 = punto4 + 1
              else:
                pass
            elif 145 <= r.player["x"] <= 205 and 460 < r.player["y"] <= 540: 
              effectlordSave.play()
              if punto5 != 1:
                punto5 = punto5 + 1
              else:
                pass
            elif 145 <= r.player["x"] <= 205 and 205 < r.player["y"] <= 265: 
              effectlordSave.play()
              if punto6 != 1:
                punto6 = punto6 + 1
              else:
                pass
            elif 60 <= r.player["x"] <= 120 and 595 < r.player["y"] <= 655: 
              effectlordSave.play()
              if punto7 != 1:
                punto7 = punto7 + 1
              else:
                pass
            elif 885 <= r.player["x"] <= 945 and 450 < r.player["y"] <= 510: 
              effectlordSave.play()
              if punto8 != 1:
                punto8 = punto8 + 1
              else:
                pass
            elif 1400 <= r.player["x"] <= 1460 and 560 < r.player["y"] <= 620:
              effectlordSave.play()
              if punto9 != 1:
                punto9 = punto9 + 1
              else:
                pass
            elif 1400 <= r.player["x"] <= 1460 and 260 < r.player["y"] <= 320:
              effectlordSave.play()
              if punto10 != 1:
                punto10 = punto10 + 1
              else:
                pass
          
        #Recoger monedas de oro
        elif e.key == pygame.K_x and 250 <= r.player["x"] <= 300 and 50 < r.player["y"] <= 90:
          if contadormonedas == 3:
            pass
          else:
            contadormonedas = 3
            hand = hand2
            effectCoins.play()
        elif e.key == pygame.K_x and 450 <= r.player["x"] <= 500 and 620 < r.player["y"] <= 650:
          if contadormonedas == 3:
            pass
          else:
            contadormonedas = 3
            hand = hand2
            effectCoins.play()
        elif e.key == pygame.K_x and 100 <= r.player["x"] <= 150 and 320 < r.player["y"] <= 430:
          if contadormonedas == 3:
            pass
          else:
            contadormonedas = 3
            hand = hand2
            effectCoins.play()
        elif e.key == pygame.K_x and 800 <= r.player["x"] <= 850 and 620 < r.player["y"] <= 650:
          if contadormonedas == 3:
            pass
          else:
            contadormonedas = 3
            hand = hand2
            effectCoins.play()
            
        #Manejo de tamanio de pantalla
        if e.key == pygame.K_f:
          if screen.get_flags() and pygame.FULLSCREEN:
            pygame.display.set_mode((tamanioPantalla, tamanioPantalla))
          else:
            pygame.display.set_mode((tamanioPantalla, tamanioPantalla),  pygame.DOUBLEBUF|pygame.HWACCEL|pygame.FULLSCREEN|pygame.HWSURFACE)

    #Se realiza el render de la escena
    r.render() 
    
    mostrarFPS(CLOCK, screen)
    pygame.display.flip()
    CLOCK.tick(60)

    #Condicion de Ganar
    if (punto1 + punto2 + punto3 + punto4 + punto5 + punto6 + punto7 + punto8 + punto9 + punto10) == nivel*2:
      gameOver = False
      
  except ZeroDivisionError:
    pass

#Cerramoas la pantalla del juego
pygame.display.quit()


#Pantalla de Congrats
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Congrats - You rock as Prince Ali')
#Se carga la pantalla de bienvenida
congrats = pygame.image.load("Winner.png").convert()
screen.blit(congrats,(0,0))
pygame.display.flip()

#Render de la ventana de Bienvenida
congrat = True
while (congrat):
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
      congrat = False
      pygame.display.quit()

      
#Pantalla de Game Over
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Game Over - Agrabah')
image = pygame.image.load("Bye.png").convert()
#Desplegamos la imagen
screen.blit(image,(0,0))
pygame.display.flip()

#Render de la ventana de Game Over
final = True
while (final):
  for event in pygame.event.get():
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
      final = False
      pygame.display.quit()

#Cerrar pygame     
pygame.quit()

#Despedida
print("Gracias por visitar Agrabah")


