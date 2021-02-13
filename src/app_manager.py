from src.app import App


class AppManager:
    def __init__(self, is_training_mode, debug):
        self.ai_controllers = []
        self.is_training_mode = is_training_mode
        self.debug = debug

    def run(self):
        running = True

        while running:
            app = App(self.is_training_mode, self.debug)
            app.init(self.ai_controllers)
            self.ai_controllers = app.ai_controllers
            should_exit = app.run()
            running = not should_exit
