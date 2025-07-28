from models.models import Wall, Floor, Gate, Skybox, Balcony, Vehicle, Garage, Guardhouse, LeisureArea
from loadObj import LoadObjs

class SceneBuilder:
    def __init__(self):
        self.components = {
            'walls': [],
            'floors': [],
            'objects': [],
            'gates': [],
            'balconies': [],
            'vehicles': [],
            'garages': [],
            'guardhouses': [],
            'leisure_areas': [],
            'skybox': None
        }
    
    # Métodos existentes
    def add_wall(self, pos, scale, frag_qtd=100, texture_path="textures/wall_texture.jpg", uv_scale=(1.0, 1.0)):
        wall = Wall(pos, scale, frag_qtd, texture_path, uv_scale)
        self.components['walls'].append(wall)
        return wall
    
    def add_floor(self, pos, scale, frag_qtd=100):
        floor = Floor(pos, scale, frag_qtd, texture_path="textures/ground_texture.jpg")
        self.components['floors'].append(floor)
        return floor

    def add_obj(self, obj_path, scale=(1, 1, 1), pos=(0, 0, 0), rotation=(0, 0, 0)):
        obj = LoadObjs(obj_path, scale, pos, rotation)
        self.components['objects'].append(obj)
        return obj

    def add_gate(self, pos=(50, 0, 0), gate_width=20, gate_height=4, pillar_width=0.5, num_bars=5):
        gate = Gate(
            pos_initial=pos,
            gate_width=gate_width,
            gate_height=gate_height,
            pillar_width=pillar_width,
            num_bars=num_bars
        )
        self.components['gates'].append(gate)
        return gate

    def add_skybox(self, texture_path: str = "textures/skybox.png", size: float = 1000.0):
        self.components['skybox'] = Skybox(texture_path, size)
        return self.components['skybox']
    
    # Novos métodos para os modelos modulares
    def add_balcony(self, pos=(0, 10, -0.2), width=5.0, height=1.0, depth=0.2):
        balcony = Balcony(pos, width, height, depth)
        self.components['balconies'].append(balcony)
        return balcony
    
    def add_vehicle(self, pos=(0, 0.35, 0), car_width=3.6, car_length=6.4, car_height=0.7, color=(1.0, 0.0, 0.0)):
        vehicle = Vehicle(pos, car_width, car_length, car_height, color)
        self.components['vehicles'].append(vehicle)
        return vehicle
    
    def add_garage(self, pos=(-25, -0.1, 13), garage_width=50.0, garage_depth=8.0, num_slots=6):
        garage = Garage(pos, garage_width, garage_depth, num_slots)
        self.components['garages'].append(garage)
        return garage
    
    def add_guardhouse(self, pos=(44, 0.15, 12), width=4.0, height=4.0, depth=4.0, texture_path="textures/brick_wall_diffuse.jpg"):
        guardhouse = Guardhouse(pos, width, height, depth, texture_path)
        self.components['guardhouses'].append(guardhouse)
        return guardhouse
    
    def add_leisure_area(self, pos=(-55, 0, -30), area_width=15.0, area_depth=15.0, pillar_height=3.0):
        leisure_area = LeisureArea(pos, area_width, area_depth, pillar_height)
        self.components['leisure_areas'].append(leisure_area)
        return leisure_area
    


    def update(self, delta_time):
        # Atualiza portões (animações)
        for gate in self.components['gates']:
            gate.update(delta_time)
    
    def draw(self):
        # Desenha skybox primeiro
        if self.components['skybox'] is not None:
            self.components['skybox'].draw()
        
        # Desenha todos os componentes
        component_order = [
            'floors', 'walls', 'balconies', 'garages', 'guardhouses', 
            'leisure_areas', 'vehicles', 'objects', 'gates'
        ]
        
        for component_type in component_order:
            for component in self.components[component_type]:
                component.draw()