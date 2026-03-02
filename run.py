import os
from fetch import main as fetch_main
from display import main as display_main

if __name__ == "__main__":
    if os.environ["MODE"] == "fetch":
        fetch_main()
    else:
        display_main()