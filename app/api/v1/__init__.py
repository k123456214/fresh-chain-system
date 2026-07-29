from fastapi import APIRouter
from app.api.v1 import auth, users, stores, products, orders, inventory, members, suppliers, employees, marketing, loss, traceability

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/v1", tags=["认证"])
api_router.include_router(users.router, prefix="/v1", tags=["用户管理"])
api_router.include_router(stores.router, prefix="/v1", tags=["门店管理"])
api_router.include_router(products.router, prefix="/v1", tags=["商品管理"])
api_router.include_router(orders.router, prefix="/v1", tags=["订单管理"])
api_router.include_router(inventory.router, prefix="/v1", tags=["库存管理"])
api_router.include_router(members.router, prefix="/v1", tags=["会员管理"])
api_router.include_router(suppliers.router, prefix="/v1", tags=["供应商管理"])
api_router.include_router(employees.router, prefix="/v1", tags=["员工管理"])
api_router.include_router(marketing.router, prefix="/v1", tags=["营销管理"])
api_router.include_router(loss.router, prefix="/v1", tags=["损耗管理"])
api_router.include_router(traceability.router, prefix="/v1", tags=["溯源管理"])
