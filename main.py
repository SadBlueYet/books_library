from src.interface import UserInterface
from src.repository import JsonRepository


def main():
    repository = JsonRepository()
    ui = UserInterface(repository)
    ui.show_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
