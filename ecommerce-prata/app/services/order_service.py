from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.models.order import Order
from app.models.order_item import OrderItem


class OrderService:

    def __init__(self, db: Session):
        self.db = db
        self.cart_repository = CartRepository(db)
        self.order_repository = OrderRepository(db)
        self.order_item_repository = OrderItemRepository(db)
    
    def finalize_order(self, user_id: int):
  

        # ============================
        # 1. Buscar carrinho
        # ============================

        cart = self.cart_repository.get_by_user_id(user_id)

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )

        if not cart.items:
            raise HTTPException(
                status_code=400,
                detail="Carrinho vazio."
            )

        # ============================
        # 2. Validar produtos
        # ============================

        subtotal = Decimal("0.00")
        discount = Decimal("0.00")
        shipping = Decimal("0.00")
        tax = Decimal("0.00")

        for item in cart.items:

            product = item.product

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Produto não encontrado."
                )

            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para {product.name}"
                )

            item_subtotal = product.price * item.quantity

            subtotal += item_subtotal

        # ============================
        # 3. Calcular total
        # ============================

        total = subtotal - discount + shipping + tax

        try:

            # ============================
            # 4. Criar pedido
            # ============================

            order = self.order_repository.create(
                user_id=user_id,
                status="PENDING",
                subtotal=subtotal,
                discount=discount,
                shipping=shipping,
                tax=tax,
                total=total
            )

            # ============================
            # 5. Criar itens do pedido
            # ============================

            for item in cart.items:

                product = item.product

                item_subtotal = product.price * item.quantity

                self.order_item_repository.create(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=item.quantity,
                    unit_price=product.price,
                    subtotal=item_subtotal
                )

                # ============================
                # 6. Atualizar estoque
                # ============================

                product.stock -= item.quantity

            # ============================
            # 7. Limpar carrinho
            # ============================

            cart.items.clear()

            # ============================
            # 8. Salvar tudo
            # ============================

            self.db.commit()

            self.db.refresh(order)

            return order

        except Exception:

            self.db.rollback()

            raise

    # =========================================================
    # CANCELAR PEDIDO
    # =========================================================

    def cancel_order(
        self,
        order_id: int,
        user_id: int
    ):

        # ============================
        # 1. Buscar pedido
        # ============================

        order = self.order_repository.get_by_id(order_id)

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Pedido não encontrado."
            )

        # ============================
        # 2. Verificar proprietário
        # ============================

        if order.user_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Você não tem permissão para cancelar este pedido."
            )

        # ============================
        # 3. Verificar status
        # ============================

        if order.status == "CANCELLED":
            raise HTTPException(
                status_code=400,
                detail="Este pedido já foi cancelado."
            )

        if order.status not in ["PENDING", "CONFIRMED"]:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Este pedido não pode mais ser cancelado "
                    f"no status atual: {order.status}."
                )
            )

        try:

            # ============================
            # 4. Restaurar estoque
            # ============================

            self.restore_stock(order)

            # ============================
            # 5. Alterar status
            # ============================

            order.status = "CANCELLED"

            # ============================
            # 6. Salvar alterações
            # ============================

            self.db.commit()

            self.db.refresh(order)

            return order

        except Exception:

            self.db.rollback()

            raise

    # =========================================================
    # RESTAURAR ESTOQUE
    # =========================================================

    def restore_stock(self, order: Order):

        """
        Devolve ao estoque a quantidade dos produtos
        pertencentes aos itens do pedido.

        Este método não faz commit.
        O commit é realizado pelo método cancel_order().
        """

        if not order.items:
            return

        for order_item in order.items:

            product = order_item.product

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Produto do item {order_item.id} "
                        "não encontrado."
                    )
                )

            # Devolver ao estoque a quantidade
            # que foi retirada na finalização do pedido
            product.stock += order_item.quantity