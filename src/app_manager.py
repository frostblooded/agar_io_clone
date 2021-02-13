from src.app import App


class AppManager:
    def __init__(self, args):
        self.ai_controllers = []
        self.args = args

    def run(self):
        running = True

        while running:
            app = App(self.args)
            app.init(self.ai_controllers)
            self.ai_controllers = app.ai_controllers
            should_exit = app.run()
            running = not should_exit
