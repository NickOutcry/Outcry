"""
Product domain router - ProductCategory, Product, ProductVariable, VariableOption, MeasureType CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from database import SessionLocal
from models.product import (
    ProductCategory, Product, ProductVariable, VariableOption,
    ProductProductVariable, MeasureType
)
from schemas.product import (
    ProductCategoryBase, ProductCategoryCreate, ProductCategoryRead,
    MeasureTypeBase, MeasureTypeCreate, MeasureTypeRead,
    ProductBase, ProductCreate, ProductRead,
    ProductVariableBase, ProductVariableCreate, ProductVariableRead,
    VariableOptionBase, VariableOptionCreate, VariableOptionRead,
    ProductProductVariableBase, ProductProductVariableCreate, ProductProductVariableRead
)
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api", tags=["product"])


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# PRODUCT CATEGORY ROUTES
# ============================================================================

@router.get("/categories", response_model=List[ProductCategoryRead])
async def get_categories(db: Session = Depends(get_db)):
    """Get all product categories"""
    categories = db.query(ProductCategory).all()
    return categories


@router.get("/categories/{category_id}", response_model=ProductCategoryRead)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a single product category by ID"""
    category = db.query(ProductCategory).filter(
        ProductCategory.product_category_id == category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/categories", response_model=ProductCategoryRead, status_code=201)
async def create_category(category: ProductCategoryCreate, db: Session = Depends(get_db)):
    """Create a new product category"""
    try:
        new_category = ProductCategory(name=category.name)
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/categories/{category_id}", response_model=ProductCategoryRead)
async def update_category(
    category_id: int,
    category: ProductCategoryCreate,
    db: Session = Depends(get_db)
):
    """Update an existing product category"""
    try:
        category_obj = db.query(ProductCategory).filter(
            ProductCategory.product_category_id == category_id
        ).first()
        if not category_obj:
            raise HTTPException(status_code=404, detail="Category not found")
        
        category_obj.name = category.name
        db.commit()
        db.refresh(category_obj)
        return category_obj
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a product category"""
    try:
        category = db.query(ProductCategory).filter(
            ProductCategory.product_category_id == category_id
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Check if category has products
        if category.products:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete category with existing products"
            )
        
        db.delete(category)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# MEASURE TYPE ROUTES
# ============================================================================

@router.get("/measure-types", response_model=List[MeasureTypeRead])
async def get_measure_types(db: Session = Depends(get_db)):
    """Get all measure types"""
    measure_types = db.query(MeasureType).all()
    return measure_types


@router.get("/measure-types/{measure_type_id}", response_model=MeasureTypeRead)
async def get_measure_type(measure_type_id: int, db: Session = Depends(get_db)):
    """Get a single measure type by ID"""
    measure_type = db.query(MeasureType).filter(
        MeasureType.measure_type_id == measure_type_id
    ).first()
    if not measure_type:
        raise HTTPException(status_code=404, detail="Measure type not found")
    return measure_type


@router.post("/measure-types", response_model=MeasureTypeRead, status_code=201)
async def create_measure_type(measure_type: MeasureTypeCreate, db: Session = Depends(get_db)):
    """Create a new measure type"""
    try:
        new_measure_type = MeasureType(measure_type=measure_type.measure_type)
        db.add(new_measure_type)
        db.commit()
        db.refresh(new_measure_type)
        return new_measure_type
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/measure-types/{measure_type_id}", response_model=MeasureTypeRead)
async def update_measure_type(
    measure_type_id: int,
    measure_type: MeasureTypeCreate,
    db: Session = Depends(get_db)
):
    """Update an existing measure type"""
    try:
        measure_type_obj = db.query(MeasureType).filter(
            MeasureType.measure_type_id == measure_type_id
        ).first()
        if not measure_type_obj:
            raise HTTPException(status_code=404, detail="Measure type not found")
        
        measure_type_obj.measure_type = measure_type.measure_type
        db.commit()
        db.refresh(measure_type_obj)
        return measure_type_obj
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/measure-types/{measure_type_id}", status_code=204)
async def delete_measure_type(measure_type_id: int, db: Session = Depends(get_db)):
    """Delete a measure type"""
    try:
        measure_type = db.query(MeasureType).filter(
            MeasureType.measure_type_id == measure_type_id
        ).first()
        if not measure_type:
            raise HTTPException(status_code=404, detail="Measure type not found")
        
        db.delete(measure_type)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# PRODUCT ROUTES
# ============================================================================

@router.get("/products", response_model=List[ProductRead])
async def get_products(db: Session = Depends(get_db)):
    """Get all products with their variables"""
    products = db.query(Product).all()
    result = []
    for product in products:
        product_data = {
            "product_id": product.product_id,
            "name": product.name,
            "base_cost": 0.0,
            "multiplier_cost": 0.0,
            "product_category_id": product.product_category_id,
            "category_name": product.category.name if product.category else None,
            "measure_type_id": product.measure_type_id,
            "measure_type_name": product.measure_type.measure_type if product.measure_type else None,
            "variables": []
        }
        
        for variable in product.variables:
            variable_data = {
                "product_variable_id": variable.product_variable_id,
                "name": variable.name,
                "base_cost": 0.0,
                "multiplier_cost": 0.0,
                "data_type": variable.data_type,
                "options": []
            }
            
            for option in variable.options:
                option_data = {
                    "variable_option_id": option.variable_option_id,
                    "name": option.name,
                    "base_cost": float(option.base_cost),
                    "multiplier_cost": float(option.multiplier_cost)
                }
                variable_data["options"].append(option_data)
            
            product_data["variables"].append(variable_data)
        
        result.append(product_data)
    
    return result


@router.get("/products/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a single product by ID"""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", response_model=ProductRead, status_code=201)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    try:
        new_product = Product(
            name=product.name,
            product_category_id=product.product_category_id,
            measure_type_id=product.measure_type_id
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/products/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product: ProductBase,
    db: Session = Depends(get_db)
):
    """Update an existing product"""
    try:
        product_obj = db.query(Product).filter(Product.product_id == product_id).first()
        if not product_obj:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product_obj.name = product.name
        product_obj.product_category_id = product.product_category_id
        product_obj.measure_type_id = product.measure_type_id
        
        db.commit()
        db.refresh(product_obj)
        return product_obj
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        db.delete(product)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# PRODUCT VARIABLE ROUTES
# ============================================================================

@router.get("/variables", response_model=List[ProductVariableResponse])
async def list_variables(db: Session = Depends(get_db)):
    """Get all product variables with their options"""
    variables = db.query(ProductVariable).all()
    result = []
    for variable in variables:
        variable_data = {
            "product_variable_id": variable.product_variable_id,
            "name": variable.name,
            "base_cost": 0.0,
            "multiplier_cost": 0.0,
            "data_type": variable.data_type,
            "product_ids": [assignment.product_id for assignment in variable.product_assignments],
            "options": []
        }
        
        for option in variable.options:
            option_data = {
                "variable_option_id": option.variable_option_id,
                "name": option.name,
                "base_cost": float(option.base_cost),
                "multiplier_cost": float(option.multiplier_cost)
            }
            variable_data["options"].append(option_data)
        
        result.append(variable_data)
    return result


@router.get("/variables/{variable_id}", response_model=ProductVariableRead)
async def get_variable(variable_id: int, db: Session = Depends(get_db)):
    """Get a single product variable by ID"""
    variable = db.query(ProductVariable).filter(
        ProductVariable.product_variable_id == variable_id
    ).first()
    if not variable:
        raise HTTPException(status_code=404, detail="Variable not found")
    return variable


@router.post("/variables", response_model=ProductVariableRead, status_code=201)
async def create_variable(variable: ProductVariableCreate, db: Session = Depends(get_db)):
    """Create a new product variable"""
    try:
        new_variable = ProductVariable(
            name=variable.name,
            data_type=variable.data_type
        )
        db.add(new_variable)
        db.flush()
        
        if variable.product_id:
            max_order = (
                db.query(func.coalesce(func.max(ProductProductVariable.display_order), 0))
                .filter(ProductProductVariable.product_id == variable.product_id)
                .scalar()
            ) or 0
            order_value = variable.display_order if variable.display_order is not None else (max_order + 1)
            assignment = ProductProductVariable(
                product_id=variable.product_id,
                product_variable_id=new_variable.product_variable_id,
                display_order=order_value
            )
            db.add(assignment)
        
        db.commit()
        db.refresh(new_variable)
        return new_variable
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/variables/{variable_id}", response_model=ProductVariableRead)
async def update_variable(
    variable_id: int,
    variable: ProductVariableBase,
    db: Session = Depends(get_db)
):
    """Update an existing product variable"""
    try:
        variable_obj = db.query(ProductVariable).filter(
            ProductVariable.product_variable_id == variable_id
        ).first()
        if not variable_obj:
            raise HTTPException(status_code=404, detail="Variable not found")
        
        variable_obj.name = variable.name
        variable_obj.data_type = variable.data_type
        db.commit()
        db.refresh(variable_obj)
        return variable_obj
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/variables/{variable_id}", status_code=204)
async def delete_variable(variable_id: int, db: Session = Depends(get_db)):
    """Delete a product variable"""
    try:
        variable = db.query(ProductVariable).filter(
            ProductVariable.product_variable_id == variable_id
        ).first()
        if not variable:
            raise HTTPException(status_code=404, detail="Variable not found")
        
        db.query(VariableOption).filter(
            VariableOption.product_variable_id == variable_id
        ).delete()
        db.delete(variable)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# VARIABLE OPTION ROUTES
# ============================================================================

@router.get("/options", response_model=List[VariableOptionRead])
async def get_options(
    product_variable_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all variable options, optionally filtered by product_variable_id"""
    query = db.query(VariableOption)
    if product_variable_id:
        query = query.filter(VariableOption.product_variable_id == product_variable_id)
    options = query.all()
    return options


@router.get("/options/{option_id}", response_model=VariableOptionRead)
async def get_option(option_id: int, db: Session = Depends(get_db)):
    """Get a single variable option by ID"""
    option = db.query(VariableOption).filter(
        VariableOption.variable_option_id == option_id
    ).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    return option


@router.post("/options", response_model=VariableOptionRead, status_code=201)
async def create_option(option: VariableOptionCreate, db: Session = Depends(get_db)):
    """Create a new variable option"""
    try:
        new_option = VariableOption(
            name=option.name,
            base_cost=option.base_cost,
            multiplier_cost=option.multiplier_cost,
            product_variable_id=option.product_variable_id
        )
        db.add(new_option)
        db.commit()
        db.refresh(new_option)
        return new_option
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/options/{option_id}", response_model=VariableOptionRead)
async def update_option(
    option_id: int,
    option: VariableOptionBase,
    db: Session = Depends(get_db)
):
    """Update an existing variable option"""
    try:
        option_obj = db.query(VariableOption).filter(
            VariableOption.variable_option_id == option_id
        ).first()
        if not option_obj:
            raise HTTPException(status_code=404, detail="Option not found")
        
        option_obj.name = option.name
        option_obj.base_cost = option.base_cost
        option_obj.multiplier_cost = option.multiplier_cost
        db.commit()
        db.refresh(option_obj)
        return option_obj
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/options/{option_id}", status_code=204)
async def delete_option(option_id: int, db: Session = Depends(get_db)):
    """Delete a variable option"""
    try:
        option = db.query(VariableOption).filter(
            VariableOption.variable_option_id == option_id
        ).first()
        if not option:
            raise HTTPException(status_code=404, detail="Option not found")
        
        db.delete(option)
        db.commit()
        return None
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# ============================================================================
# PRODUCT-PRODUCT VARIABLE ASSIGNMENT ROUTES
# ============================================================================

@router.post("/products/{product_id}/variables/{variable_id}", status_code=201)
async def assign_variable_to_product(
    product_id: int,
    variable_id: int,
    display_order: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Assign a variable to a product"""
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        variable = db.query(ProductVariable).filter(
            ProductVariable.product_variable_id == variable_id
        ).first()
        if not variable:
            raise HTTPException(status_code=404, detail="Variable not found")
        
        existing = db.query(ProductProductVariable).filter(
            ProductProductVariable.product_id == product_id,
            ProductProductVariable.product_variable_id == variable_id
        ).first()
        if existing:
            return {"message": "Variable already assigned to product"}
        
        if display_order is None:
            max_order = (
                db.query(func.coalesce(func.max(ProductProductVariable.display_order), 0))
                .filter(ProductProductVariable.product_id == product_id)
                .scalar()
            ) or 0
            display_order = max_order + 1
        
        assignment = ProductProductVariable(
            product_id=product_id,
            product_variable_id=variable_id,
            display_order=display_order
        )
        db.add(assignment)
        db.commit()
        
        return {
            "message": "Variable assigned successfully",
            "product_id": product_id,
            "product_variable_id": variable_id
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))



# ============================================================================
# TEST ENDPOINT
# ============================================================================

@router.get("/product/test", response_class=JSONResponse)
async def test_product_connection(db: Session = Depends(get_db)):
    """
    Test endpoint to verify database connection and models.
    Returns the first record from ProductCategory, Product, and ProductVariable tables.
    """
    result = {
        "status": "success",
        "message": "Database connection and models are working",
        "data": {}
    }
    
    try:
        # Test ProductCategory table
        first_category = db.query(ProductCategory).first()
        if first_category:
            result["data"]["category"] = {
                "product_category_id": first_category.product_category_id,
                "name": first_category.name
            }
        else:
            result["data"]["category"] = None
        
        # Test Product table
        first_product = db.query(Product).first()
        if first_product:
            result["data"]["product"] = {
                "product_id": first_product.product_id,
                "name": first_product.name,
                "product_category_id": first_product.product_category_id,
                "measure_type_id": first_product.measure_type_id
            }
        else:
            result["data"]["product"] = None
        
        # Test ProductVariable table
        first_variable = db.query(ProductVariable).first()
        if first_variable:
            result["data"]["variable"] = {
                "product_variable_id": first_variable.product_variable_id,
                "name": first_variable.name,
                "data_type": first_variable.data_type
            }
        else:
            result["data"]["variable"] = None
        
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection error: {str(e)}",
            "data": {}
        }
