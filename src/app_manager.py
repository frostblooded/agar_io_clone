from src.app import App


class AppManager:
    def __init__(self, is_training_mode):
        self.ai_controllers = []
        self.is_training_mode = is_training_mode

    def run(self):
        while True:
            app = App(self.is_training_mode)
            app.init(self.ai_controllers)
            self.ai_controllers = app.ai_controllers
            app.run()
