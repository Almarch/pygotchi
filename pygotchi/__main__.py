import uvicorn

import uvicorn
import sys

def main():
    host = "127.0.0.1"
    port = 8000

    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Error: Port must be an integer.")
            sys.exit(1)

    uvicorn.run("pygotchi.app:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    main()
