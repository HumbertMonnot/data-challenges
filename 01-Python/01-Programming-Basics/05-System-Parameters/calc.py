# pylint: disable=missing-module-docstring,missing-function-docstring,eval-used
import sys

def main(args=None):
    """Implement the calculator"""
    if args is None:
        args = sys.argv
    nb1 = args[1]
    nb2 = args[3]
    return eval(f"{nb1}{args[2]}{nb2}")


if __name__ == "__main__":
    print(main())
