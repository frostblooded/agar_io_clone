from src.app_manager import AppManager
import argparse


def main(is_training_mode, debug):
    appManager = AppManager(is_training_mode, debug)
    appManager.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--training', action='store_true')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    main(args.training, args.debug)
