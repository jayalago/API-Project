from . import orders, order_details, menu, sandwiches, resources, customer, payment, promotion, rating

from ..dependencies.database import engine


def index():

    customer.Base.metadata.create_all(engine)
    order_details.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    payment.Base.metadata.create_all(engine)
    promotion.Base.metadata.create_all(engine)
    rating.Base.metadata.create_all(engine)
    menu.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)