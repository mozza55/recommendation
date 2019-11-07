# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, Integer, String, Table, Text
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Broadcast(db.Model):
    __tablename__ = 'broadcast'

    brod_id = db.Column(db.Integer, primary_key=True)
    channel_ch_id = db.Column(db.Integer, nullable=False)
    product_prod_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(45))
    brod_date = db.Column(db.DateTime)
    brod_state = db.Column(db.Integer)
    thumbnail_url = db.Column(db.String(500), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    media_id = db.Column(db.String(100))


class Cart(db.Model):
    __tablename__ = 'cart'

    user_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    product01_id = db.Column(db.Integer, server_default=db.FetchedValue())
    product01_quantity = db.Column(db.Integer, server_default=db.FetchedValue())
    product02_id = db.Column(db.Integer, server_default=db.FetchedValue())
    product02_quantity = db.Column(db.Integer, server_default=db.FetchedValue())


class CartProduct(db.Model):
    __tablename__ = 'cartProduct'

    cartProduct_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_prod_id = db.Column(db.Integer)


class Category(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(45))
    parent_id = db.Column(db.Integer)
    code = db.Column(db.String(45))


class Channel(db.Model):
    __tablename__ = 'channel'

    ch_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(45))
    description = db.Column(db.String(255))
    follower_num = db.Column(db.Integer)
    category_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float)
    cost = db.Column(db.Integer)
    views = db.Column(db.Integer)
    ER = db.Column(db.Float)
    addr_city = db.Column(db.String(45))
    addr_gu = db.Column(db.String(45))
    addr_dong = db.Column(db.String(45))
    h_code = db.Column(db.Integer)
    brod_type = db.Column(db.String(45))
    banner_img = db.Column(db.String(500))
    representVideo = db.Column(db.Integer)
    target_w = db.Column(db.Float)
    target_m = db.Column(db.Float)
    target_10 = db.Column(db.Float)
    target_20 = db.Column(db.Float)
    target_30 = db.Column(db.Float)
    target_40 = db.Column(db.Float)
    target_50 = db.Column(db.Float)
    target_60 = db.Column(db.Float)


class ChannelCategory(db.Model):
    __tablename__ = 'channelCategory'

    chCategory_id = db.Column(db.Integer, primary_key=True)
    channel_ch_id = db.Column(db.Integer)
    category_ctgr_id = db.Column(db.Integer)


class Chatting(db.Model):
    __tablename__ = 'chatting'

    chat_id = db.Column(db.Integer, primary_key=True)
    brodcast_brod_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    chatText = db.Column(db.String(255))
    time = db.Column(db.DateTime, nullable=False)
    broadcast_brod_id = db.Column(db.Integer)
    use_id = db.Column(db.Integer)


class Contract(db.Model):
    __tablename__ = 'contract'

    cont_id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer)
    influencer_id = db.Column(db.Integer, nullable=False)
    provider_id = db.Column(db.Integer, nullable=False)
    times = db.Column(db.Integer)
    onePerTime = db.Column(db.Integer)
    price = db.Column(db.Integer)
    requirement = db.Column(db.String(45))
    con_date = db.Column(db.DateTime)
    del_at = db.Column(db.DateTime)
    product_id = db.Column(db.Integer, nullable=False)


class ContractProduct(db.Model):
    __tablename__ = 'contractProduct'

    contProd_id = db.Column(db.Integer, primary_key=True)
    contract_con_id = db.Column(db.Integer, nullable=False)
    product_prod_id = db.Column(db.Integer, nullable=False)


class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.Integer, nullable=False)
    broadcast_id = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


class Follower(db.Model):
    __tablename__ = 'follower'

    follower_id = db.Column(db.Integer, primary_key=True)
    channel_ch_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


class Gifticon(db.Model):
    __tablename__ = 'gifticon'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    isUsing = db.Column(db.Integer, nullable=False)
    issue_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, nullable=False)


t_hibernate_sequence = db.Table(
    'hibernate_sequence',
    db.Column('next_val', db.BigInteger)
)


class Messenger(db.Model):
    __tablename__ = 'messenger'

    msg_id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, nullable=False)
    user2_id = db.Column(db.Integer, nullable=False)
    msg_date = db.Column(db.DateTime)
    del_at = db.Column(db.DateTime)


class MessengerText(db.Model):
    __tablename__ = 'messengerText'

    msgText_id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, nullable=False, index=True)
    to_user_id = db.Column(db.String(45), nullable=False)
    text = db.Column(db.String(255))
    messenger_msg_id = db.Column(db.Integer, nullable=False)
    msgText_date = db.Column(db.DateTime)
    del_at = db.Column(db.DateTime)


class NoticeBoard(db.Model):
    __tablename__ = 'noticeBoard'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.Integer, nullable=False)


class Order(db.Model):
    __tablename__ = 'order'

    odr_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    totalPrice = db.Column(db.Integer)
    time = db.Column(db.DateTime, nullable=False)
    product01_id = db.Column(db.Integer)
    product01_quantity = db.Column(db.Integer)
    product02_id = db.Column(db.Integer)
    product02_quantity = db.Column(db.Integer)
    addr_city = db.Column(db.String(45))
    addr_gu = db.Column(db.String(45))
    addr_dong = db.Column(db.String(45))
    addr_detail = db.Column(db.String(45))


class OrderProduct(db.Model):
    __tablename__ = 'orderProduct'

    orderProduct_id = db.Column(db.Integer, primary_key=True)
    order_odr_id = db.Column(db.Integer, nullable=False)
    product_prod_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)


class Product(db.Model):
    __tablename__ = 'product'

    prod_id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(45))
    price = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    description = db.Column(db.Text)
    provider_id = db.Column(db.Integer, nullable=False)
    del_at = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(6000))
    changed_price = db.Column(db.Integer)
    detail_img_url = db.Column(db.String(6000))


class SaleEvent(db.Model):
    __tablename__ = 'saleEvent'

    id = db.Column(db.Integer, primary_key=True)
    saleEvent_type = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    discount_percent = db.Column(db.Integer, nullable=False)


class Shop(db.Model):
    __tablename__ = 'shop'

    shop_id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(45), nullable=False)
    provider_user_id = db.Column(db.Integer, nullable=False)
    uri = db.Column(db.String(45), nullable=False)
    addr_city = db.Column(db.String(45), nullable=False)
    addr_gu = db.Column(db.String(45), nullable=False)
    addr_dong = db.Column(db.String(45), nullable=False)
    addr_detail = db.Column(db.String(45), nullable=False)
    h_code = db.Column(db.Integer)
    follower_num = db.Column(db.String(45), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    area_code = db.Column(db.Integer)
    profile_img = db.Column(db.String(500))
    banner_img = db.Column(db.String(500))
    target_w = db.Column(db.Float)
    target_m = db.Column(db.Float)
    target_10 = db.Column(db.Float)
    target_20 = db.Column(db.Float)
    target_30 = db.Column(db.Float)
    target_40 = db.Column(db.Float)
    target_50 = db.Column(db.Float)
    target_60 = db.Column(db.Float)
    isDelete = db.Column(db.Integer, nullable=False)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))
    name = db.Column(db.String(45))
    role = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    age = db.Column(db.Integer)
    birth = db.Column(db.DateTime)
    del_at = db.Column(db.DateTime)
    balance = db.Column(db.Integer, nullable=False)
    addr_city = db.Column(db.String(45))
    addr_gu = db.Column(db.String(45))
    addr_dong = db.Column(db.String(45))
    addr_detail = db.Column(db.String(45))
    isDelete = db.Column(db.Integer, nullable=False)
    profile_img = db.Column(db.String(255))


class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    uploader_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=False)
    uploadAt = db.Column(db.DateTime, nullable=False)
