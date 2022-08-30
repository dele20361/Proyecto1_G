from gl import Renderer, color, V3, V2
from texture import Texture
from shaders import flat, unlit, gourad, toon, glow, textureBlend

width = 960
height = 540

rend = Renderer(width, height)
rend.dirLight = V3(1,0,0)

rend.active_texture = Texture("models/earthDay.bmp")
rend.active_texture2 = Texture("models/earthNight.bmp")
rend.active_shader = textureBlend

rend.glLoadModel("models/model.obj",
                 translate = V3(0, 0,-10),
                 scale = V3(0.01,0.01,0.01),
                 rotate = V3(0,90,0))
                 

rend.glFinish("output.bmp")

