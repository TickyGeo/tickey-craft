import ursina
import ursina.prefabs.first_person_controller

app = ursina.Ursina() 
player = ursina.prefabs.first_person_controller.FirstPersonController()
player.position = (20, 4, 20)
player.speed = 5
player.gravity = 0.5    
ursina.Sky(texture=ursina.load_texture("assets/sky.jpg"))

voxel_selected = 1

textures = [
    None,
    ursina.load_texture("assets/grass_uv.png"),
    ursina.load_texture("assets/dirt_uv.png"),
    ursina.load_texture("assets/wood_uv.png"),
    ursina.load_texture("assets/stone_uv.png"),
    ursina.load_texture("assets/brick_uv.png"),
    ursina.load_texture("assets/heart_uv.png"),
]

texture_icons = [
    None,
    ursina.load_texture("assets/grass.png"),
    ursina.load_texture("assets/dirt.png"),
    ursina.load_texture("assets/wood.png"),
    ursina.load_texture("assets/stone.png"),
    ursina.load_texture("assets/brick.png"),
    ursina.load_texture("assets/heart.png"),
]

models = {
    "cube" : "assets/cube.obj",
    "tree" : "assets/tree.glb",
    "pig" : "assets/pig.glb",
    "chicken" : "assets/chicken.glb"
}

animal_models = [models["chicken"], models["pig"]]

slot_entities = [None] * 7
start_x = -0.45
spacing = 0.15

for i in range(1, 7):
    slot_x = start_x + i * spacing
    slot_entities[i] = ursina.Entity(
        parent = ursina.camera.ui,
        model = "quad",
        texture = texture_icons[i],
        scale = 0.10,
        position = (slot_x, -0.4)
    )

selector_outline = ursina.Entity(
    parent = ursina.camera.ui,
    model = "quad",
    color = ursina.color.light_gray,
    scale = 0.12,
    z = 0.1,
    position = (slot_entities[voxel_selected].x, -0.4)
)

class Voxel(ursina.Button):
    def __init__(self, position, texture):
        super().__init__(
            parent = ursina.scene,
            color = ursina.color.white,
            highlight_color = ursina.color.light_gray,
            position = position,
            model = models["cube"],
            texture = texture,
            origin_y = 0.5,
            scale = 0.5
        )

class Prop(ursina.Entity):
    def __init__(self, position, model, scale):
        super().__init__(
            parent=ursina.scene,
            position=position,
            model=model,
            origin_y=0.5,
            scale=scale,
            collider="box",
            double_sided=True
        )

class Animal(ursina.Entity):
    def __init__(self, position, model, scale):
        super().__init__(
            parent=ursina.scene,
            position=position,
            model=model,
            origin_y=0.5,
            scale=scale,
            collider="box"
        )

        self.speed = 1
        self.direction = ursina.Vec3(1, 0, 0)
        self.change_timer = 0

    def update(self):
        self.change_timer -= ursina.time.dt

        if self.change_timer <= 0:
            self.direction = ursina.Vec3(
                ursina.random.uniform(-1, 1),
                0,
                ursina.random.uniform(-1, 1)
            ).normalized()

            self.change_timer = ursina.random.uniform(1, 3)


        self.position += self.direction * self.speed * ursina.time.dt


        self.position.x = max(1, min(39, self.position.x))
        self.position.z = max(1, min(39, self.position.z))

def generate_map(num_trees = 2, num_animals = 5):
    num_tiles = 40
    for z in range(num_tiles):
        for x in range(num_tiles):
            Voxel(position=(x, 0, z), texture=textures[1])       

    for _ in range(num_trees):
        tree_x = ursina.random.randint(1, num_tiles - 1)
        tree_z = ursina.random.randint(1, num_tiles - 1)
        Prop(position=(tree_x, 1, tree_z), model=models["tree"], scale=5.5)

    for _ in range(num_animals):
        animal_x = ursina.random.randint(1, num_tiles - 1)
        animal_z = ursina.random.randint(1, num_tiles - 1)
        animal_model = ursina.random.choice(animal_models)
        Animal(position=(animal_x, 1, animal_z), model=animal_model, scale=0.1)

def input(key):
    global voxel_selected

    if key == "escape":
        ursina.application.quit()

    elif key in ['1', '2', '3', '4', '5', '6']:
        voxel_selected = int(key)  
        selector_outline.x = slot_entities[voxel_selected].x  

    if isinstance(ursina.mouse.hovered_entity, Voxel):
        if key == "left mouse down":
            Voxel(
                position = ursina.mouse.hovered_entity.position + ursina.mouse.normal,
                texture = textures[voxel_selected]
            )
        elif key == "right mouse down":
            ursina.destroy(ursina.mouse.hovered_entity)

generate_map()
app.run()