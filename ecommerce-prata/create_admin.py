from app.core.database import SessionLocal

from app.models.user import User
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.category import Category
from app.models.order import Order
from app.models.order_item import OrderItem
from app.core.security import hash_password
from getpass import getpass

def create_admin():
    db = SessionLocal()

    try:
        name = input("Nome do administrador: ").strip()
        email = input("E-mail do administrador: ").strip().lower()
        password = getpass("Senha do administrador: ")

        if not name:
            print("Erro: o nome é obrigatório.")
            return

        if not email:
            print("Erro: o e-mail é obrigatório.")
            return

        if not password:
            print("Erro: a senha é obrigatória.")
            return

        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            if existing_user.is_admin:
                print("Este usuário já é administrador.")
                return

            confirm = input(
                "Este e-mail já existe. "
                "Deseja transformar este usuário em administrador? (s/n): "
            ).strip().lower()

            if confirm != "s":
                print("Operação cancelada.")
                return

            existing_user.is_admin = True
            db.commit()

            print("Usuário promovido a administrador com sucesso!")
            print(f"E-mail: {existing_user.email}")
            return

        password_hash = hash_password(password)

        admin = User(
            name=name,
            email=email,
            password_hash=password_hash,
            is_admin=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print()
        print("Administrador criado com sucesso!")
        print(f"ID: {admin.id}")
        print(f"Nome: {admin.name}")
        print(f"E-mail: {admin.email}")
        print(f"Administrador: {admin.is_admin}")

    except Exception as exc:
        db.rollback()
        print(f"Erro ao criar administrador: {exc}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()