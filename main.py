from src.app_manager import AppManager
import argparse


def main(args):
    appManager = AppManager(args)
    appManager.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--training', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--save-models', type=str,
                        help='Path to serialized neural networks')
    parser.add_argument('--load-models', type=str,
                        help='Path to serialized neural networks')
    args = parser.parse_args()
    main(args)
