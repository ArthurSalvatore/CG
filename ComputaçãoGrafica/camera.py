class CameraState:
    def __init__(self):
        self.current_cam_pos = None
        self.target_cam_pos = None
        self.start_cam_pos = None
        self.is_transitioning = False
        self.transition_start_time = 0
        self.transition_duration = 0.5  # 500ms para transições