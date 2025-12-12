"""
Pydantic schemas for Product domain models
"""
from pydantic import BaseModel
from typing import Optional


# ProductCategory Schemas
class ProductCategoryBase(BaseModel):
    name: str


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryRead(ProductCategoryBase):
    product_category_id: int
    
    class Config:
        from_attributes = True


# MeasureType Schemas
class MeasureTypeBase(BaseModel):
    measure_type: str


class MeasureTypeCreate(MeasureTypeBase):
    pass


class MeasureTypeRead(MeasureTypeBase):
    measure_type_id: int
    
    class Config:
        from_attributes = True


# Product Schemas
class ProductBase(BaseModel):
    name: str
    product_category_id: int
    measure_type_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    product_id: int
    
    class Config:
        from_attributes = True


# ProductVariable Schemas
class ProductVariableBase(BaseModel):
    name: str
    data_type: str


class ProductVariableCreate(ProductVariableBase):
    pass


class ProductVariableRead(ProductVariableBase):
    product_variable_id: int
    
    class Config:
        from_attributes = True


# VariableOption Schemas
class VariableOptionBase(BaseModel):
    name: str
    base_cost: float
    multiplier_cost: float
    product_variable_id: int


class VariableOptionCreate(VariableOptionBase):
    pass


class VariableOptionRead(VariableOptionBase):
    variable_option_id: int
    
    class Config:
        from_attributes = True


# ProductProductVariable Schemas
class ProductProductVariableBase(BaseModel):
    product_id: int
    product_variable_id: int
    display_order: Optional[int] = None


class ProductProductVariableCreate(ProductProductVariableBase):
    pass


class ProductProductVariableRead(ProductProductVariableBase):
    product_product_variable: int
    
    class Config:
        from_attributes = True

