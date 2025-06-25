from course_work.app.models import Product, Category, Brand
from sqlalchemy import or_

class CatalogRepository:
    def __init__(self, db):
        self.db = db

    def get_filtered_products(self, page, per_page, filters):
        query = self.db.session.query(Product)

        if filters.get("query"):
            query = query.filter(Product.name.ilike(f"%{filters['query']}%"))

        if filters.get("category_ids"):
            query = query.filter(Product.category_id.in_(filters["category_ids"]))

        if filters.get("brand_ids"):
            query = query.filter(Product.brand_id.in_(filters["brand_ids"]))

        if filters.get("min_price") is not None:
            query = query.filter(Product.price >= filters["min_price"])

        if filters.get("max_price") is not None:
            query = query.filter(Product.price <= filters["max_price"])

        if filters.get("available"):
            query = query.filter(Product.stock_quantity > 0)

        pagination = query.paginate(page=page, per_page=per_page)
        return pagination
