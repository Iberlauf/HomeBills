"""Main module."""

from sqlmodel import Session, select

from database import create_db_and_tables, engine
from models import Address, User, Business
# from create_instances import create_address, create_user, create_business, create_bill


def get_address(address_id: int) -> Address | None:
    """Get address by id.

    Args:
        address_id (int): Id number of the Address class instance.

    Returns:
        Address | None
    """
    with Session(bind=engine) as session:
        address = session.get(entity=Address, ident=address_id)
        if address:
            return address
        return None


def get_user(user_id: int) -> User | None:
    """Get user by id.

    Args:
        user_id (int): Id number of the User class instance.

    Returns:
        User | None
    """
    with Session(bind=engine) as session:
        user = session.get(entity=User, ident=user_id)
        if user:
            return user
        return None


def get_buiness(business_id: int) -> Business | None:
    """Get business by id.

    Args:
        business_id (int): Id number of the User class instance.

    Returns:
        Business | None
    """
    with Session(bind=engine) as session:
        business = session.get(entity=Business, ident=business_id)
        if business:
            return business
        return None


def select_business_by_account(account: int) -> Business | None:
    """Select business by its bank account number.

    Args:
        account (int): Bank account number.

    Returns:
        Business | None
    """
    with Session(bind=engine) as session:
        business = session.exec(
            select(Business).where(Business.bank_account == account)
        ).first()
        if business:
            return business
        return None


def main() -> None:
    """Main function."""

    create_db_and_tables()
    # get_user(user_id=1)
    # get_address(address_id=1)


if __name__ == "__main__":
    main()
