from src.app_manager import AppManager
import argparse


def main(is_training_mode):
    appManager = AppManager(is_training_mode)
    appManager.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--training', action='store_true')
    args = parser.parse_args()
    main(args.training)
