from fastmcp import FastMCP
from sqlalchemy import func
from database import SessionLocal, Product

mcp = FastMCP("Enterprise Product MCP")


# -------------------- INVENTORY --------------------

@mcp.tool()
def add_inventory(name: str, category: str, price: float, quantity: int):
    """Add new product to the inventory."""
    db = SessionLocal()

    product = Product(
        name=name,
        category=category,
        price=price,
        quantity=quantity
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    db.close()

    return {"message": "Product added", "product_id": product.id}




@mcp.tool()
def update_inventory(product_id: int, product_name: str = None, category_name: str = None, quantity: int = None, result: list = None, price: float = None):
    """Update product quantity."""

    db = SessionLocal()

    if result is not None:
        updated_count =0
        for item in result:
            if isinstance(item, dict) and "id" in item:
                product_id = item.get("id")
                new_quantity = item.get("quantity", item.get('new_quantity'))

                if product_id is not None and new_quantity is not None:
                    product = db.query(Product).filter(Product.id == product_id).first()
                    if product:
                        product.quantity = new_quantity
                        updated_count += 1
        if updated_count > 0:
            db.commit()
            db.close()
            return {"message": f"Inventory updated for {updated_count} products."}
        else:
            db.close()
            return {"error": "No valid products found in result"}
    elif product_name is not None:
        product = db.query(Product).filter(Product.name == product_name).first()

        if not product:
            db.close()
            return {"error": "Product not found"}
        product.quantity = quantity
        db.commit()
        db.close()
        return {"message": f"Inventory updated for product '{product_name}'"}
    elif category_name is not None and quantity is not None:
        products = db.query(Product).filter(Product.category == category_name).all()

        if not products:
            db.close()
            return {"error": "No products found in this category"}
        
        for product in products:
            product.quantity = quantity
        db.commit()
        db.close()
        return {"message": f"Inventory updated for {len(products)} products in category '{category_name}'"}
    elif product_id is not None and quantity is not None:
        product = db.query(Product).filter(Product.id == product_id).first()
    

        if not product:
            db.close()
            return {"error": "Product not found"}
        product.quantity = quantity
        db.commit()
        db.close()
        return {"message": f"Inventory updated for product ID {product_id}"}
    else:
        db.close()
        return {"error": "Provide product_id and quantity or product_name and quantity or category_name and quantity or result array with id and quantity"}


# -------------------- CATALOG --------------------

@mcp.tool()
def list_catalog():
    """Return all products."""
    db = SessionLocal()

    products = db.query(Product).all()

    result = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "quantity": p.quantity
        }
        for p in products
    ]

    db.close()
    return result


@mcp.tool()
def search_product(keyword: str):
    """Search products by keyword."""
    db = SessionLocal()

    products = db.query(Product).filter(
        Product.name.like(f"%{keyword}%")).all()

    result = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "quantity": p.quantity
        }
        for p in products
    ]

    db.close()
    return result


# -------------------- ANALYTICS --------------------

@mcp.tool()
def total_inventory_value():
    """Calculate total inventory value."""
    db = SessionLocal()
    value = db.query(func.sum(Product.price * Product.quantity)).scalar()

    db.close()
    return {"total_inventory_value": value or 0}


@mcp.tool()
def category_summary():
    """Total value grouped by category."""
    db = SessionLocal()
    result = db.query(
        Product.category,
        func.sum(Product.price * Product.quantity)
        ).group_by(Product.category).all()

    db.close()
    return {category: value for category, value in result}


# -------------------- DISCOUNT --------------------

@mcp.tool()
def apply_discount(percent: float, category: str = None, result: list = None, product_name: str = None):
    """Apply discount to products. Can target by category, product name or result array."""
    db = SessionLocal()

    if product_name:
        product = db.query(Product).filter(
            Product.name == product_name
        ).all()

        if not product:
            db.close()
            return {"error": "Product not found"}
    
    elif result is not None:
        product_ids=[p.get("id") for p in result if isinstance(p, dict) and "id" in p]

        if product_ids:
            products = db.query(Product).filter(
                Product.id.in_(product_ids)
                ).all()
        else:
            db.close()
            return {"error": "No valid products found in result"}

    elif category is not None:
        products = db.query(Product).filter(
            Product.category == category
        ).all()

        if not products:
            db.close()
            return {"error": "No products found in this category"}
    else:
        db.close()
        return {"error": "Provide category or product_name or result"}
        
    for p in products:
        p.price = p.price * (1 - percent / 100)

    db.commit()
    db.close()

   #Return aapropriate message based on which method was used
    if product_name:
       return {"message": f"{percent}% discount applied to product '{product_name}'"}
    elif result is not None:
       return {"message": f"{percent}% discount applied to {len(products)} products from result array"}
    elif category is not None:
       return {"message": f"{percent}% discount applied to '{category}'"}
    else:
         return {"message": f"{percent}% discount applied"} 

# -------------------- LOW STOCK --------------------

@mcp.tool()
def low_stock_products(threshold: int = 10, name: str = None, category: str = None):
    """Return low stock products."""
    db = SessionLocal()

    query = db.query(Product).filter(Product.quantity < threshold)

    if name is not None:
        query = query.filter(Product.name.like(f"%{name}%"))
    if category is not None:
        query = query.filter(Product.category.like(f"%{category}%"))
    products = query.all()

    result = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "quantity": p.quantity
        }
        for p in products
    ]

    db.close()
    return result

if __name__ == "__main__":
    mcp.run(transport="http", port=8001)