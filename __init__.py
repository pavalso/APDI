import sys
import os

from urllib.parse import urlparse
from urllib.error import URLError
from argparse import ArgumentParser

from src import main


__usage__ = f"Usage: python \"{__file__}\" [auth_api] [-d db] [-p port] [-l listening] [-s storage]"

def _url(url: str) -> str:
    result = urlparse(url)
    if all([result.scheme, result.netloc]):
        return url
    raise URLError

def _parse_args() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "auth_api", 
        type=_url)

    parser.add_argument(
        "-d", "--db",
        type=str,
        default=None)

    parser.add_argument(
        "-p", "--port", 
        type=int,
        default=3002)

    parser.add_argument(
        "-l", "--listening",
        type=str,
        default="0.0.0.0")

    parser.add_argument(
        "-s", "--storage",
        type=str,
        default="storage")

    return parser.parse_args()

if __name__ == "__main__":

    try:
        args = _parse_args()
    except URLError:
        print(f"[!] Invalid URL.\n{__usage__}")
        sys.exit(1)

    if args.db is None:
        args.db = "pyblob.db"
    elif not os.path.isfile(args.db):
        print(f"[!] Database file {args.db} does not exist.\n{__usage__}")
        sys.exit(1)

    try:
        main(
            port=args.port,
            host=args.listening,
            db_path=args.db,
            storage=args.storage,
            auth_api=args.auth_api
            )
    except RuntimeError:
        print(f"[!] Auth API at {args.auth_api} is not running.")
        sys.exit(2)

    sys.exit(0)
