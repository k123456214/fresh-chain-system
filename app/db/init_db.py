from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.store import Store
from app.models.product import Product
from app.models.member import MemberLevel
from datetime import datetime

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                username="admin",
                password=get_password_hash("admin123"),
                real_name="系统管理员",
                phone="13800138000",
                email="admin@freshstore.com",
                role="admin"
            )
            db.add(admin)
        
        if not db.query(Store).first():
            stores = [
                Store(name="旗舰店-中心广场店", code="S001", address="市中心广场1号", phone="010-88880001", manager="张经理", area=500),
                Store(name="分店-东湖路店", code="S002", address="东湖路88号", phone="010-88880002", manager="李经理", area=350),
                Store(name="分店-科技园店", code="S003", address="科技园南路168号", phone="010-88880003", manager="王经理", area=280)
            ]
            for store in stores:
                db.add(store)
        
        if not db.query(MemberLevel).first():
            levels = [
                MemberLevel(name="普通会员", min_points=0, discount_rate=1.0, benefits="基础会员服务"),
                MemberLevel(name="银卡会员", min_points=500, discount_rate=0.95, benefits="9.5折优惠,专属客服"),
                MemberLevel(name="金卡会员", min_points=2000, discount_rate=0.90, benefits="9折优惠,免费配送,生日礼包"),
                MemberLevel(name="钻石会员", min_points=5000, discount_rate=0.85, benefits="8.5折优惠,优先购买,专属活动")
            ]
            for level in levels:
                db.add(level)
        
        if not db.query(Product).first():
            products = [
                Product(name="有机番茄", code="P001", barcode="6901234500001", category="蔬菜", unit="kg", price=12.8, cost_price=8.5, stock=200, min_stock=50, max_stock=500, description="新鲜有机番茄，自然成熟"),
                Product(name="海南香蕉", code="P002", barcode="6901234500002", category="水果", unit="kg", price=6.8, cost_price=4.2, stock=300, min_stock=80, max_stock=600, description="海南特产香蕉，香甜可口"),
                Product(name="东北大米", code="P003", barcode="6901234500003", category="粮油", unit="kg", price=8.9, cost_price=6.5, stock=500, min_stock=100, max_stock=1000, description="东北黑土地大米，颗粒饱满"),
                Product(name="新鲜猪肉", code="P004", barcode="6901234500004", category="肉类", unit="kg", price=38.0, cost_price=28.5, stock=100, min_stock=30, max_stock=300, description="当日现宰新鲜猪肉"),
                Product(name="有机菠菜", code="P005", barcode="6901234500005", category="蔬菜", unit="kg", price=5.8, cost_price=3.2, stock=150, min_stock=40, max_stock=400, description="有机种植菠菜，营养丰富"),
                Product(name="智利车厘子", code="P006", barcode="6901234500006", category="水果", unit="kg", price=98.0, cost_price=65.0, stock=50, min_stock=10, max_stock=150, description="进口智利车厘子，香甜多汁"),
                Product(name="土鸡蛋", code="P007", barcode="6901234500007", category="蛋类", unit="kg", price=18.8, cost_price=12.0, stock=200, min_stock=50, max_stock=400, description="农家散养土鸡蛋"),
                Product(name="青岛啤酒", code="P008", barcode="6901234500008", category="饮料", unit="瓶", price=6.5, cost_price=4.5, stock=500, min_stock=100, max_stock=1000, description="青岛纯生啤酒500ml"),
                Product(name="有机胡萝卜", code="P009", barcode="6901234500009", category="蔬菜", unit="kg", price=4.8, cost_price=2.8, stock=180, min_stock=40, max_stock=350, description="有机胡萝卜，脆嫩可口"),
                Product(name="泰国香米", code="P010", barcode="6901234500010", category="粮油", unit="kg", price=15.8, cost_price=11.0, stock=300, min_stock=60, max_stock=600, description="泰国茉莉香米")
            ]
            for product in products:
                db.add(product)
        
        db.commit()
        print("数据库初始化成功！")
        print("默认管理员账号: admin / admin123")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
