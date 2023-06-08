import subprocess
from argparse import ArgumentParser, Namespace

arg_parser = ArgumentParser()
arg_parser.add_argument(
    "type",
    metavar="TYPE",
    choices=["manipulator", "controller", "sensor"],
    help="Type of service to run (manipulator, controller, sensor)"
)


def run(args: Namespace):
    match args.type:
        case "controller":
            subprocess.run("uvicorn mcs.controller:app --port 21234")
        case _:
            print(f"type '{args.type}' is not supported yet")


if __name__ == '__main__':
    try:
        run(arg_parser.parse_args())
    except KeyboardInterrupt:
        pass
