import sys
import os
import argparse
import asyncio
import logging

# Add src to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
# Add vendor to sys.path if needed, or assume installed. 
# But since 'thrift' was in root, maybe it's custom? 
# I moved it to src/linebot/vendor.
sys.path.append(os.path.join(os.path.dirname(__file__), "src", "linebot", "vendor"))

from linebot.core.client import LineClient

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="LINE Bot Manager")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # selfbot
    sb_parser = subparsers.add_parser("selfbot", help="Run Selfbot")
    sb_parser.add_argument("mid", help="User MID (or config key)")
    sb_parser.add_argument("--token", help="Auth Token")
    sb_parser.add_argument("--password", help="Password")

    # loginbot
    lb_parser = subparsers.add_parser("loginbot", help="Run LoginBot (Auto Login)")
    lb_parser.add_argument("--token", help="Auth Token", required=True)
    lb_parser.add_argument("--password", help="Password", required=True)

    # protect
    pt_parser = subparsers.add_parser("protect", help="Run Protect Bot")
    pt_parser.add_argument("mid", help="User MID")

    # pub_protect
    pp_parser = subparsers.add_parser("pub_protect", help="Run Public Protect Bot")

    args = parser.parse_args()

    if args.command == "selfbot":
        from linebot.bots.self_bot.main import Selfbot
        import aiohttp
        
        loop = asyncio.get_event_loop()
        connector = aiohttp.ClientSession()
        client = None
        
        # Logic adapted from original selfbot.py
        if args.token and args.password:
            client = LineClient(
                token=args.token,
                passwd=args.password,
                connector=connector
            )
        
        # If no token/pass, Selfbot might rely on existing session or crash if not handled.
        # But we pass what we have.
        try:
            sb = Selfbot(client, connector, args.mid)
            sb.main()
        except Exception as e:
            logger.error(f"Error running Selfbot: {e}")
            raise

    elif args.command == "loginbot":
        from linebot.bots.auto_login.main import LoginBot
        import aiohttp
        
        connector = aiohttp.ClientSession()
        client = LineClient(
            token=args.token,
            passwd=args.password,
            connector=connector
        )
        lb = LoginBot(client)
        lb.main()
        
    elif args.command == "protect":
        from linebot.bots.protect.main import Protect
        pb = Protect(args.mid)
        pb.start()
        
    elif args.command == "pub_protect":
        from linebot.bots.pub_protect.main import Protect as PubProtect
        pb = PubProtect()
        pb.start()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
