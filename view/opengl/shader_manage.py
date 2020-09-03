from enum import IntEnum
from pyrr import Vector4
from OpenGL import GL
import OpenGL.GL.shaders


class ShaderManager:
    class ShaderStructEnumerate(IntEnum):
        """
            Class for indexing on array information about shader
        """
        shader = 0  #
        code = 1
        is_compile = 2
        type = 3
        inner_var = 4
        is_attached = 5  # value can not be used
        # inner_var is responsible for list of tuple. The tuple will be initialized when u call prepare_shader.
        # First element of tuple is uniform variable for store. Second is str name of variable

    all_shaders = []
    shader_program = None
    is_program_compile = False
    is_need_rebind = True

    solo_color_shader_code = """
    # version 330
    uniform vec4 vertexColor;
    out vec4 outColor;
    void main()
    {
    outColor = vertexColor;
    }
    """
    vertex_shader_code = """
    # version 330
    in layout(location = 0) vec3 positions;

    void main(){
        gl_Position = vec4(vec3,1 .0)
    }
    """

    solo_color_shader = [None, solo_color_shader_code, False, False, GL.GL_FRAGMENT_SHADER, [[None, "vertexColor"]],
                         False]
    vertex_shader = [None, vertex_shader_code, False, False, GL.GL_VERTEX_SHADER, [], False]

    @classmethod
    def prepare_shader(cls, shader: list):
        """
        shader: use exist in class lists of shaders
        """
        EnSS = cls.ShaderStructEnumerate
        shader[EnSS.shader] = OpenGL.GL.shaders.compileShader(shader[EnSS.code], shader[EnSS.type])
        # check for errors
        shader[EnSS.is_compile] = GL.glGetShaderiv(shader[EnSS.shader], GL.GL_COMPILE_STATUS, None)
        if shader[EnSS.is_compile]:
            cls.all_shaders.append(shader)

    @classmethod
    def compile_program(cls):
        cls.shader_program = OpenGL.GL.shaders.compileProgram(*cls.all_shaders)
        cls.is_program_compile = True

    @classmethod
    def get_all_uniform_loc(cls):
        if cls.is_program_compile:
            # get access to inner uniform values of shader
            EnSS = cls.ShaderStructEnumerate
            for shader in cls.all_shaders:
                for i in range(len(shader[EnSS.inner_var])):
                    temp = shader[EnSS.inner_var][i]
                    # 1 - index of str_name_of_variable
                    value = GL.glGetUniformLocation(cls.shader_program, temp[1])
                    shader[EnSS.inner_var][i] = (value, temp[1])

    @classmethod
    def set_color(cls, color: (iter, list, tuple)):
        if len(color) != 4:
            return False
        EnSS = cls.ShaderStructEnumerate
        if not cls.solo_color_shader_code[EnSS.is_compile] or not cls.solo_color_shader_code[EnSS.is_attached]:
            return False
        value = cls.solo_color_shader_code[EnSS.inner_var][0][0]
        if not value:
            cls.get_all_uniform_loc()
        GL.glUniform4f(value, *color)

    @classmethod
    def attach_all_shaders(cls):
        """
        Attach shaders in list if it hasn't been attach

        """
        EnSS = cls.ShaderStructEnumerate
        for shader in cls.all_shaders:
            if not shader[EnSS.is_attached]:
                GL.glAttachShader(cls.shader_program, shader[EnSS.shader])
                shader[EnSS.is_attached] = True


def main():
    # A = ShaderManager.ShaderStructEnumerate
    # b = [5, 6, 7, 8, 9]
    # print(f"{A.shader} : {b[A.shader]}, {A.code} : {b[A.code]},")
    ShaderManager.prepare_shader(ShaderManager.solo_color_shader)
    ShaderManager.compile_program()
    ShaderManager.get_all_uniform_loc()
    # ShaderManager.prepare_shader(ShaderManager.vertex_shader)
    # ShaderManager.attach_all_shaders()]


if __name__ == '__main__':
    main()
