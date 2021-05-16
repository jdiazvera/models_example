# coding: utf-8
import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, \
    Boolean, JSON
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql.base import MONEY

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model


class DBUtils:
    def json(self, *args):
        new_json = {}
        for col in self.__table__.columns:
            val = self.__getattribute__(col.name)
            new_json[col.name] = str(val) if not isinstance(val, int) and val is not None else val

        for rel in self.__mapper__.relationships:
            if rel.key in args:
                actual_model = self.__getattribute__(rel.key)
                if actual_model is not None:
                    if type(actual_model) is InstrumentedList:
                        for sub_model in actual_model:
                            if rel.key not in new_json:
                                new_json[rel.key] = []
                            new_json[rel.key].append(sub_model.json(*args))
                    else:
                        new_json[rel.key] = actual_model.json(*args)
                else:
                    new_json[rel.key] = None
        return new_json


class Address(Base, DBUtils):
    __tablename__ = 'addresses'

    address_id = Column(BigInteger, primary_key=True, server_default=FetchedValue())
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    address = Column(String(100), nullable=False)
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())

    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)

    city = Column(String(16), nullable=False)
    department = Column(String(32), nullable=False)
    neighborhood = Column(String(32), nullable=False)
    names = Column(String(64), nullable=False)
    description = Column(String(64))
    phone = Column(String(16))

    user = relationship('User', primaryjoin='Address.user_id == User.user_id', backref='addresses')


class AuditLog(Base, DBUtils):
    __tablename__ = 'audit_logs'

    traza_id = Column(BigInteger, primary_key=True, server_default=FetchedValue())
    solicitude = Column(String(60), nullable=False)
    action = Column(String(60), nullable=False)
    name = Column(String(60))
    user_id = Column(Integer)
    createdsince = Column(DateTime, server_default=FetchedValue())
    updatedsince = Column(DateTime)


class Category(Base, DBUtils):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    name = Column(String(100), nullable=False)
    fullname = Column(Text, nullable=False)
    banner = Column(String(200))
    parent_path = Column(String(250))
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    in_menu = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)

    parent_id = Column(ForeignKey('categories.category_id'))
    """
    parent = relationship('Category',
                          foreign_keys=category_id,
                          primaryjoin="Category.category_id == Category.parent_id",
                          remote_side=[parent_id])
    """
    parent = relationship("Category", remote_side=parent_id, primaryjoin="Category.category_id == Category.parent_id")
    users_preferred = relationship('User', secondary='cetegory_preferred')

    users_history = relationship('User', secondary='history_category_user')


class ChatRoom(Base, DBUtils):
    __tablename__ = 'chat_room'

    room_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    store_id = Column(ForeignKey('store.store_id'), nullable=False)
    seller_id = Column(ForeignKey('users.user_id'), nullable=False)
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, nullable=False, server_default=FetchedValue())
    updated_since = Column(DateTime)

    # store = relationship('Store', primaryjoin='ChatRoom.store_id == Store.store_id', backref='chat_rooms')
    user = relationship('User', primaryjoin='ChatRoom.user_id == User.user_id', backref='chat_rooms')
    seller = relationship('User', primaryjoin='ChatRoom.seller_id == User.user_id')


class Claim(Base, DBUtils):
    __tablename__ = 'claims'

    claim_id = Column(BigInteger, primary_key=True, server_default=FetchedValue())
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    content = Column(String(350), nullable=False)
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)

    user = relationship('User', primaryjoin='Claim.user_id == User.user_id', backref='claims')


class DocumentType(Base, DBUtils):
    __tablename__ = 'document_type'

    type_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    name = Column(String(80), nullable=False)
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)


class File(Base, DBUtils):
    __tablename__ = 'files'

    file_id = Column(BigInteger, primary_key=True, server_default=FetchedValue())
    product_id = Column(ForeignKey('products.product_id'), nullable=False)
    url = Column(String(200), nullable=False)
    main = Column(SmallInteger, server_default=FetchedValue())
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)

    file_product = relationship('Product', primaryjoin='File.product_id == Product.product_id', backref='files')


class Message(Base, DBUtils):
    __tablename__ = 'messages'

    message_id = Column(BigInteger, primary_key=True, server_default=FetchedValue())
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    room_id = Column(ForeignKey('chat_room.room_id'), nullable=False)
    content = Column(Text)
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, nullable=False, server_default=FetchedValue())
    updated_since = Column(DateTime)

    room = relationship('ChatRoom', primaryjoin='Message.room_id == ChatRoom.room_id', backref='messages')
    user = relationship('User', primaryjoin='Message.user_id == User.user_id', backref='messages')


class Order(Base, DBUtils):
    __tablename__ = 'orders'

    order_id = Column(BigInteger, primary_key=True, server_default=FetchedValue())
    product_id = Column(ForeignKey('products.product_id'), nullable=False)
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    seller_id = Column(ForeignKey('users.user_id'), nullable=False)
    method_id = Column(ForeignKey('payment_methods.method_id'), nullable=False)
    transaction_id = Column(Integer)
    quantity = Column(Integer, server_default=FetchedValue())
    total = Column(Numeric(18, 2))
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)

    method = relationship('PaymentMethod', primaryjoin='Order.method_id == PaymentMethod.method_id',
                          backref='orders')
    product = relationship('Product', foreign_keys=product_id)
    user = relationship('User', primaryjoin='Order.user_id == User.user_id', backref='orders')
    # seller = relationship('User', primaryjoin='Order.seller_id == User.user_id', backref='orders')
    users_qualify = relationship('User', secondary='qualifies_order_store')
    purchase_status = Column(Integer, nullable=True, server_default='1')


class PaymentMethod(Base, DBUtils):
    __tablename__ = 'payment_methods'

    method_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    name = Column(String(50), nullable=False)
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)


class Product(Base, DBUtils):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    category_id = Column(ForeignKey('categories.category_id'), nullable=False)
    user_id = Column(ForeignKey('users.user_id'))
    store_id = Column(ForeignKey('store.store_id'))
    color = Column(String(80))
    title = Column(String(800), nullable=False)
    imagescsv = Column(String(800))
    description = Column(Text, nullable=False)
    information = Column(Text)
    asin = Column(String(20), unique=True)
    sku = Column(String(20))
    usd = Column(MONEY)
    price = Column(MONEY, nullable=False)
    discount = Column(Numeric(18, 2))
    earnings_percentage = Column(Numeric(5, 2), server_default=FetchedValue())
    stock = Column(Integer, nullable=False)
    weight = Column(Numeric(18, 2))
    height = Column(Numeric(18, 2))
    length = Column(Numeric(18, 2))
    width = Column(Numeric(18, 2))
    size = Column(String(8))
    type = Column(String(100))
    product_group = Column(String(150))
    genre = Column(String(150))
    model = Column(String(200))
    edition = Column(String(200))
    platform = Column(String(200))
    format = Column(String(200))
    is_prime = Column(SmallInteger, server_default=FetchedValue())
    is_adult_product = Column(SmallInteger, server_default=FetchedValue())
    package_height = Column(Numeric(10, 2))
    package_length = Column(Numeric(10, 2))
    package_width = Column(Numeric(10, 2))
    package_weight = Column(Numeric(10, 2))
    package_quantity = Column(Numeric(10, 2))
    features = Column(Text)
    category_tree = Column(Text)
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)
    brand = Column(String(200))

    category = relationship('Category', primaryjoin='Product.category_id == Category.category_id', backref='products')
    store = relationship('Store', primaryjoin='Product.store_id == Store.store_id', backref='products')
    user = relationship('User', primaryjoin='Product.user_id == User.user_id', backref='products')
    images = relationship('File', primaryjoin='Product.product_id == File.product_id', backref='files')


    users_suggested = relationship('User', secondary='products_suggested')
    users_favorite = relationship('User', secondary='products_favorite')

    sales_accountant = Column(Integer)

    users_history = relationship('User', secondary='history_product_user')


class Question(Base, DBUtils):
    __tablename__ = 'questions'

    question_id = Column(BigInteger, primary_key=True, server_default=FetchedValue())
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    store_id = Column(ForeignKey('store.store_id'))
    product_id = Column(ForeignKey('products.product_id'), nullable=False)
    content = Column(String(3000), nullable=False)

    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)

    product = relationship('Product', primaryjoin='Question.product_id == Product.product_id', backref='questions')
    store = relationship('Store', primaryjoin='Question.store_id == Store.store_id', backref='questions')
    user = relationship('User', primaryjoin='Question.user_id == User.user_id', backref='questions')
    answers = relationship('Answer', primaryjoin='Question.question_id == Answer.question_id', backref='answers')

class Role(Base, DBUtils):
    __tablename__ = 'role'

    role_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    name = Column(String(60), nullable=False)
    description = Column(String(400))
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)


class Store(Base, DBUtils):
    __tablename__ = 'store'

    store_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    name = Column(String(100), nullable=False)
    business_name = Column(String(100))
    nit = Column(String(15), nullable=False)
    phone = Column(String(20), nullable=False)
    alternative_phone = Column(String(20))
    address = Column(String(100), nullable=False)
    logo = Column(String(150))
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, nullable=False, server_default=FetchedValue())
    updated_since = Column(DateTime)

    user = relationship('User', primaryjoin='Store.user_id == User.user_id', backref='stores')
    products_featured = relationship('Product', secondary='products_featured')

    users_follower_store = relationship('User', secondary='follower_store')


class User(Base, DBUtils):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    role_id = Column(ForeignKey('role.role_id'), nullable=False)
    name = Column(String(50))
    second_name = Column(String(50))
    last_name = Column(String(50))
    second_last_name = Column(String(50))
    email = Column(String(50), nullable=False)
    username = Column(String(50))
    password = Column(String(255), nullable=False)
    photo = Column(String(80))
    document_type = Column(ForeignKey('document_type.type_id'))
    id_number = Column(String(20))
    id_file = Column(String(80))
    phone = Column(String(20))
    alternative_phone = Column(String(20))
    last_login = Column(DateTime)
    register_type = Column(String(15), nullable=False)
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)
    register_token = Column(String(64))
    recovery_token = Column(String(64))
    type_kiero_leader = Column(SmallInteger, nullable=True)
    is_active = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    date_of_birth = Column(DateTime)
    sex = Column(String(1))
    document = Column(String(64))

    document_type1 = relationship('DocumentType', primaryjoin='User.document_type == DocumentType.type_id',
                                  backref='users')
    role = relationship('Role', primaryjoin='User.role_id == Role.role_id', backref='users')

    products_suggested = relationship('Product', secondary='products_suggested')
    products_favorite = relationship('Product', secondary='products_favorite')

    categories_preferred = relationship('Category', secondary='cetegory_preferred')

    orders_qualify = relationship('Order', secondary='qualifies_order_store')
    stories_qualify = relationship('Store')
    stories_follower = relationship('Store', secondary='follower_store')
    categories_history = relationship('Category', secondary='history_category_user')
    products_history = relationship('Product', secondary='history_product_user')


class TransactionsPayu(Base, DBUtils):
    __tablename__ = 'transactions_payu'

    transaction_id = Column(Integer, primary_key=True, unique=True, server_default=FetchedValue())
    order_id_payu = Column(String(50), nullable=False)
    transaction_id_payu = Column(String(50), nullable=False)
    code_response_payu = Column(String(50))
    state_transaction = Column(String(50))
    trazability_code = Column(String(50))
    operation_payu_date = Column(DateTime)
    order_id = Column(ForeignKey('orders.order_id'), nullable=False)
    state = Column(String(50))
    transaction_state = Column(String(50))
    pol_response_code = Column(String(50))
    lap_response_code = Column(String(50))
    lap_transaction_state = Column(String(50))
    msg_payu = Column(String(255))
    ref_code = Column(String(50))

    order = relationship('Order')


class Notifications(Base, DBUtils):
    __tablename__ = 'notifications'

    notification_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    type = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    title = Column(String(64))
    text = Column(String(255))
    readed = Column(DateTime, server_default=FetchedValue())
    order_id = Column(Integer)
    link = Column(String(255))
    image = Column(String(255))
    created_since = Column(DateTime, server_default=FetchedValue())


# New table: Yuri
class ProductSuggested(Base, DBUtils):
    __tablename__ = 'products_suggested'

    product_suggested_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)


class ProductFavorite(Base, DBUtils):
    __tablename__ = 'products_favorite'

    product_favorite_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)


class ProductFeaturedStore(Base, DBUtils):
    __tablename__ = 'products_featured'

    product_featured_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    store_id = Column(Integer, ForeignKey('store.store_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)


class CategoryPreferredUser(Base, DBUtils):
    __tablename__ = 'cetegory_preferred'

    cetegory_preferred_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.category_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)


class QualifyOrderStore(Base, DBUtils):
    __tablename__ = 'qualifies_order_store'

    qualify_order_store_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)
    value = Column(Integer)


class ProductFeedBack(Base, DBUtils):
    __tablename__ = 'products_feedback'

    product_feedback_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)
    feedback = Column(Integer)


class FollowerStore(Base, DBUtils):
    __tablename__ = 'follower_store'

    follower_store_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    stored_id = Column(Integer, ForeignKey('store.store_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)


class HistoryCategoryUser(Base, DBUtils):
    __tablename__ = 'history_category_user'

    history_category_user_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    category = Column(Integer, ForeignKey('categories.category_id'), primary_key=True)
    product_feedback_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)
    visitor_count = Column(Integer)
    feedback = Column(Integer)


class HistoryProductUser(Base, DBUtils):
    __tablename__ = 'history_product_user'

    history_product_user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    product = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)
    visitor_count = Column(Integer)


class ContactMails(Base, DBUtils):
    __tablename__ = 'contacts_mails'

    email_id = Column(Integer, primary_key=True, unique=True, server_default=FetchedValue())
    email = Column(String(50))
    created_since = Column(DateTime, server_default=FetchedValue())


class RatingProduct(Base, DBUtils):
    __tablename__ = 'rating_products'

    rating_products_id = Column(Integer, primary_key=True, server_default=FetchedValue())
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    product_id = Column(ForeignKey('products.product_id'), nullable=False)
    value = Column(Integer, nullable=False)

    user = relationship('User', primaryjoin='RatingProduct.user_id == User.user_id', backref='rating_products')
    product = relationship('Product', primaryjoin='RatingProduct.product_id == Product.product_id',
                           backref='rating_products')


class SellerProductsSuggested(Base, DBUtils):
    __tablename__ = 'seller_products_suggested'

    seller_products_suggested_id = Column(Integer, primary_key=True, unique=True, server_default=FetchedValue())
    seller_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    update_since = Column(DateTime, server_default=FetchedValue())

    seller = relationship('User', primaryjoin='SellerProductsSuggested.seller_id == User.user_id',
                          backref='seller_products_suggested')
    products = relationship('Product', primaryjoin='SellerProductsSuggested.product_id == Product.product_id',
                            backref='seller_products_suggested')


class AnulateUser(Base, DBUtils):
    __tablename__ = 'anulate_user'

    anulate_user_id = Column(Integer, primary_key=True, unique=True, server_default=FetchedValue())
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    movites = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)
    created_since = Column(DateTime, server_default=FetchedValue())
    update_since = Column(DateTime, server_default=FetchedValue())

    user = relationship('User', primaryjoin='AnulateUser.user_id == User.user_id', backref='anulate_user')


class ProductGlobal(Base, DBUtils):
    __tablename__ = 'products_global'

    product_global_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    active = Column(Boolean, default=True)
    is_variant = Column(Boolean, default=False)
    product_asin = Column(String(20), unique=True)
    price = Column(MONEY, nullable=False)
    package_weight = Column(Numeric(10, 2))
    color = Column(String(80))
    title = Column(String(800), nullable=False)
    size = Column(String(8))
    url = Column(String(200), nullable=True)
    #product = relationship('Product', foreign_keys=product_id)
    product = relationship('Product', primaryjoin='ProductGlobal.product_id == Product.product_id',
                           backref='product_global_products')
    product_variants = relationship('ProductVariant', lazy=True,
                                    foreign_keys='ProductVariant.product_global_id', cascade="all, delete")
    product_files = relationship('FileGlobal', lazy=True,
                                    foreign_keys='FileGlobal.product_global_id', cascade="all, delete")
    images = relationship('FileGlobal', primaryjoin='ProductGlobal.product_global_id == FileGlobal.product_global_id', backref='files')


class ProductVariant(Base, DBUtils):
    __tablename__ = 'products_global_variants'

    product_variant_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    product_global_id = Column(Integer, ForeignKey('products_global.product_global_id'), primary_key=True)
    variant_id = Column(Integer, ForeignKey('variants.variant_id'), primary_key=True)
    variant = relationship('Variant', foreign_keys=variant_id)
    product_global = relationship('ProductGlobal', foreign_keys=product_global_id)


class Variant(Base, DBUtils):
    __tablename__ = 'variants'

    variant_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    dimension_id = Column(Integer, ForeignKey('dimensions.dimension_id'), primary_key=True)
    html_color = Column(String(20))
    value = Column(String(100))
    dimension = relationship('Dimension', foreign_keys=dimension_id,lazy='subquery')


class Dimension(Base, DBUtils):
    __tablename__ = 'dimensions'

    dimension_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(20))
    display_type = Column(String(20))


class FileGlobal(Base, DBUtils):
    __tablename__ = 'files_global'

    file_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    product_global_id = Column(ForeignKey('products_global.product_global_id'), nullable=False)
    url = Column(String(200), nullable=False)
    main = Column(SmallInteger, server_default=FetchedValue())
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)
    file_product_global = relationship('ProductGlobal', primaryjoin='FileGlobal.product_global_id == ProductGlobal.product_global_id', backref='files')

class ProductCopy(Base, DBUtils):
    __tablename__ = 'products_errors'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    error = Column(String(800), nullable=False)

class StoreDetails(Base, DBUtils):
    __tablename__ = 'store_details'

    store_details_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(ForeignKey('store.store_id'), nullable=False)
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    visit = Column(Integer)
    domain = Column(String(100), unique=True)
    design = Column(String(100))
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)

    user = relationship('User', primaryjoin='StoreDetails.user_id == User.user_id', backref='store_details')
    store = relationship('Store', primaryjoin='StoreDetails.store_id == Store.store_id', backref='store_details')
    google_analytic = Column(String(100))
    template_id = Column(String(100))
    facebook_pixel = Column(String(100))
    facebook_vinculate = Column(Boolean, default=False)
    google_ads_intention = Column(String(100))
    google_ads_confirmation_hashtag = Column(String(100))
    google_ads_confirmation_fragment = Column(String(100))
    google_ads_remarketing_hashtag = Column(String(100))
    google_ads_remarketing_fragment = Column(String(100))

class ProductDetails(Base, DBUtils):
    __tablename__ = 'product_details'

    product_details_id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(ForeignKey('store.store_id'), nullable=False)
    product_id = Column(ForeignKey('products.product_id'), nullable=False)
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    store_details_id = Column(ForeignKey('store_details.store_details_id'), nullable=False)
    is_features = Column(Integer, server_default=FetchedValue())
    sold = Column(Integer, server_default=FetchedValue())
    on_sale = Column(Integer, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)

    store = relationship('Store', primaryjoin='ProductDetails.store_id == Store.store_id', backref='product_details')
    user = relationship('User', primaryjoin='ProductDetails.user_id == User.user_id', backref='product_details')
    product = relationship('Product', primaryjoin='ProductDetails.product_id == Product.product_id', backref='product_details')
    store_details = relationship('StoreDetails', primaryjoin='ProductDetails.store_details_id == StoreDetails.store_details_id', backref='product_details')


class RatePurchase(Base, DBUtils):
    __tablename__ = 'rate_purchase'

    rate_purchase_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    rate_purchase = Column(Integer)
    rate_product = Column(Integer)
    comments = Column(Text, nullable=True)
    images = Column(JSON)
    created_since = Column(DateTime,  default=datetime.datetime.utcnow)

class Banner(Base, DBUtils):
    __tablename__ = 'm_banner'

    banner_id = Column(BigInteger, primary_key=True, autoincrement=True)
    my_url = Column(String(200), nullable=False)
    url = Column(String(200), nullable=False)
    created_since = Column(DateTime, server_default=FetchedValue())

class ImageCategory(Base, DBUtils):
    __tablename__ = 'm_image_category'

    image_category_id = Column(BigInteger, primary_key=True, autoincrement=True)
    url = Column(String(200), nullable=False)
    category_id = Column(Integer, nullable=False)
    created_since = Column(DateTime, server_default=FetchedValue())


class Answer(Base, DBUtils):
    __tablename__ = 'answers'

    answers_id = Column(BigInteger,  primary_key=True, autoincrement=True)
    question_id = Column(ForeignKey('questions.question_id'), nullable=False)
    user_id = Column(ForeignKey('users.user_id'), nullable=False)
    content = Column(String(3000), nullable=False)
    status = Column(SmallInteger, nullable=False, server_default=FetchedValue())
    created_since = Column(DateTime, server_default=FetchedValue())
    updated_since = Column(DateTime)

    user = relationship('User', primaryjoin='Answer.user_id == User.user_id', backref='users')
