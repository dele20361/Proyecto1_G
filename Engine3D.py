from gl import Renderer, color, V3, V2
from texture import Texture
import shader as s 
import math as m 

w = 1024
h = 640

rend = Renderer(w, h)

# Background
rend.background = Texture("models/textures/museumWall.bmp")
rend.glClearBackground()
rend.glLookAt(V3(2,5,-3),V3(0,7.9,1))

################################################################################
#                                      MODELS

# Helicopter
rend.active_shader = s.colrs
rend.active_texture = Texture("models/textures/statue.bmp")
rend.glLoadModel("models/heli.obj",
                 translate = V3(-0.1,6.55,-3.2),
                 rotate = V3(0.1, 90, 0.1),
                 scale = V3(0.045, 0.045, 0.045))

# Skull
rend.active_shader = s.powr
rend.active_texture = Texture("models/textures/skull.bmp")
rend.glLoadModel("models/skull.obj",
                 translate = V3(-0.6,5.7,-2),
                 rotate = V3(240, 15, 0),
                 scale = V3(0.01, 0.01, 0.01))

# Statue
rend.active_shader = s.powr
rend.active_texture = Texture("models/textures/statue.bmp")
rend.glLoadModel("models/statue.obj",
                 translate = V3(1.5,5,-2),
                 rotate = V3(240, 15, 1),
                 scale = V3(0.0065, 0.0065, 0.0065))

# Estatua
rend.active_shader = s.powr
rend.active_texture = Texture("models/textures/statue_diffuse.bmp")
rend.glLoadModel("models/maui.obj",
                 translate = V3(8.7,3.8,-5),
                 rotate = V3(255, 20, 1),
                 scale = V3(0.0065, 0.0065, 0.0065))

# Bird
rend.active_texture = Texture("models/textures/12214_Bird_diffuse.bmp")
rend.normal_map = Texture("models/textures/Map__7_Normal-Bump.bmp") # Normal map
rend.active_shader = s.powr
rend.glLoadModel("models/birdd.obj",
                 translate = V3(11.3,-1.5,-5),
                 rotate = V3(0, 0, 1),
                 scale = V3(0.17, 0.17, 0.17))
################################################################################

# Output
rend.glFinish("output1.bmp")

