from src.app import App


class AppManager:
    def __init__(self):
        self.ai_controllers = []

    def run(self):
        while True:
            app = App()
            app.init(self.ai_controllers)
            self.ai_controllers = app.ai_controllers
            app.run()
