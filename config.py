class Parameters:

    def __init__(self):
        self.t_weld = 120
        self.t_press = 260
        self.t_i = 0
        self.a = 0.007
        self.k = 0.25
        self.c = 2000
        self.ro = 1300
        self.a_area = 1
        self.num_node = 5
        self.delta_tau = 1
        self.epsilon = 0.01
        self.ae = 89.28571428571429
        self.ae6 = 178.57142857142858
        self.aw = 89.28571428571429
        self.aw2 = 178.57142857142858
        self.w = 7280.0
        self.label_ae = None
        self.label_ae6 = None
        self.label_aw = None
        self.label_aw2 = None
        self.label_w = None
        self.folder_path = None
        self.folder_name = ""

    def update_params(self, name, value):
        setattr(self, name, value)

params = Parameters()