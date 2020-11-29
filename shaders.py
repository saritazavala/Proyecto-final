#Sara Zavala
#Ultimo proyecto
#Graficas por computador

vertex_shader = """
#version 460
layout (location = 0) in vec4 pos;
layout (location = 1) in vec4 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projectionMatrix;

uniform vec4 color;
uniform vec4 light;

out vec4 vertexColor;
out vec2 vertexTexcoords;

void main()
{
    float intensity = dot(model * normal, normalize(light - pos));

    gl_Position = projectionMatrix * view * model * pos;
    vertexColor = color * intensity;
    vertexTexcoords = texcoords;
}
"""

toon_vertex_shader = """
#version 460
layout (location = 0) in vec4 pos;
layout (location = 1) in vec4 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projectionMatrix;

uniform vec4 color;
uniform vec4 light;

out vec4 vertexColor;
out vec2 vertexTexcoords;

void main()
{
    float intensity = dot(model * normal, normalize(light - pos));
    intensity = intensity > 0.95 ? 1 : (intensity > 0.7 ? 0.7 : (intensity > 0.4 ? 0.4 : (intensity > 0.1 ? 0.1 : 0.05)));

    gl_Position = projectionMatrix * view * model * pos;
    vertexColor = color * intensity;
    vertexTexcoords = texcoords;
}
"""

reverse_vertex_shader = """
#version 460
layout (location = 0) in vec4 pos;
layout (location = 1) in vec4 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projectionMatrix;

uniform vec4 color;
uniform vec4 light;

out vec4 vertexColor;
out vec2 vertexTexcoords;

void main()
{
    float intensity = 1 - dot(model * normal, normalize(light - pos));

    gl_Position = projectionMatrix * view * model * pos;
    vertexColor = color * intensity;
    vertexTexcoords = texcoords;
}
"""


fragment_shader = """
#version 460
layout (location = 0) out vec4 diffuseColor;

in vec4 vertexColor;
in vec2 vertexTexcoords;

uniform sampler2D tex;

void main()
{
    diffuseColor =  vertexColor * texture(tex, vertexTexcoords);
}
"""

fragment_neg_shader = """
#version 460
layout (location = 0) out vec4 diffuseColor;

in vec4 vertexColor;
in vec2 vertexTexcoords;

uniform sampler2D tex;

void main()
{
    vec4 neg = vec4(1.0);
    diffuseColor = vertexColor * (neg - texture(tex, vertexTexcoords));
}
"""

fragment_static_shader = """
#version 460

float rnd(vec2 x)
{
    int n = int(x.x * 40.0 + x.y * 6400.0);
    n = (n << 13) ^ n;
    return 1.0 - float( (n * (n * n * 15731 + 789221) + \
             1376312589) & 0x7fffffff) / 1073741824.0;
}

layout (location = 0) out vec4 diffuseColor;

in vec4 vertexColor;
in vec2 vertexTexcoords;

uniform sampler2D tex;

void main()
{
    vec4 text = texture(tex, vertexTexcoords);
    vec4 colors = vec4(rnd(text.xy));
    diffuseColor = vertexColor * colors;
}
"""