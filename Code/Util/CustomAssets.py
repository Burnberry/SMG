from pyglet import image, gl


class CustomAssetGen:
    @staticmethod
    def generate(data, w=16, h=16, fmt="RGBA"):
        img = image.ImageData(w, h, fmt, data)

        texture = img.get_texture()
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(texture.target, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        return img
