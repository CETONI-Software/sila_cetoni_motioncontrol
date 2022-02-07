import logging
from argparse import ArgumentParser

from .server import Server

logger = logging.getLogger(__name__)


def parse_args():
    parser = ArgumentParser(prog="axis_service", description="Start this SiLA 2 server")
    parser.add_argument("-a", "--ip-address", default="127.0.0.1", help="The IP address (default: '127.0.0.1')")
    parser.add_argument("-p", "--port", type=int, default=50052, help="The port (default: 50052)")
    parser.add_argument("--disable-discovery", action="store_true", help="Disable SiLA Server Discovery")

    log_level_group = parser.add_mutually_exclusive_group()
    log_level_group.add_argument("-q", "--quiet", action="store_true", help="Only log errors")
    log_level_group.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    log_level_group.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")

    return parser.parse_args()


def start_server(args):
    server = Server()

    try:
        server.start_insecure(args.ip_address, args.port, enable_discovery=not args.disable_discovery)
        print(f"Server startup complete, running on {args.ip_address}:{args.port}. Press Enter to stop it")

        try:
            input()
        except KeyboardInterrupt:
            pass
    finally:
        server.stop()
        print("Stopped server")


def setup_basic_logging(args):
    level = logging.WARNING
    if args.verbose:
        level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    if args.quiet:
        level = logging.ERROR

    logging.basicConfig(level=level, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")


if __name__ == "__main__":
    args = parse_args()
    setup_basic_logging(args)
    start_server(args)
