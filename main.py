"""Mainn module."""

from database import create_db_and_tables


def main() -> None:
    """Main function."""
    create_db_and_tables()


if __name__ == "__main__":
    main()
