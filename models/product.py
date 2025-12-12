"""
Product domain models
"""
from sqlalchemy import Column, Integer, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from . import Base


class ProductCategory(Base):
    """Product Category schema for categorizing products"""
    __tablename__ = 'product_categories'
    __table_args__ = {'schema': 'product'}
    
    product_category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    
    # Relationships
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<ProductCategory(product_category_id={self.product_category_id}, name='{self.name}')>"


class MeasureType(Base):
    """Measure Type schema for storing measurement types"""
    __tablename__ = 'measure_type'
    __table_args__ = {'schema': 'product'}
    
    measure_type_id = Column(Integer, primary_key=True, autoincrement=True)
    measure_type = Column(Text, nullable=False)
    
    # Relationships
    products = relationship("Product", back_populates="measure_type")
    
    def __repr__(self):
        return f"<MeasureType(measure_type_id={self.measure_type_id}, measure_type='{self.measure_type}')>"


class Product(Base):
    """Product schema for storing product information"""
    __tablename__ = 'products'
    __table_args__ = {'schema': 'product'}
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    product_category_id = Column(Integer, ForeignKey('product.product_categories.product_category_id'), nullable=False)
    measure_type_id = Column(Integer, ForeignKey('product.measure_type.measure_type_id'), nullable=True)
    
    # Relationships
    category = relationship("ProductCategory", back_populates="products")
    measure_type = relationship("MeasureType", back_populates="products")
    product_variable_assignments = relationship(
        "ProductProductVariable",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    variables = relationship(
        "ProductVariable",
        secondary="product.product_product_variable",
        back_populates="products",
        order_by="ProductProductVariable.display_order"
    )
    items = relationship("Item", back_populates="product")
    
    def __repr__(self):
        return f"<Product(product_id={self.product_id}, name='{self.name}')>"


class ProductVariable(Base):
    """Product Variable schema for storing product variations"""
    __tablename__ = 'product_variables'
    __table_args__ = {'schema': 'product'}
    
    product_variable_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    data_type = Column(Text, nullable=False)
    
    # Relationships
    options = relationship("VariableOption", back_populates="product_variable")
    item_variables = relationship("ItemVariable", back_populates="product_variable")
    product_assignments = relationship(
        "ProductProductVariable",
        back_populates="product_variable",
        cascade="all, delete-orphan"
    )
    products = relationship(
        "Product",
        secondary="product.product_product_variable",
        back_populates="variables"
    )
    
    def __repr__(self):
        return f"<ProductVariable(product_variable_id={self.product_variable_id}, name='{self.name}')>"


class VariableOption(Base):
    """Variable Option schema for storing specific options of product variables"""
    __tablename__ = 'variable_options'
    __table_args__ = {'schema': 'product'}
    
    variable_option_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    base_cost = Column(Float, nullable=False)
    multiplier_cost = Column(Float, nullable=False)
    product_variable_id = Column(Integer, ForeignKey('product.product_variables.product_variable_id'), nullable=False)
    
    # Relationships
    product_variable = relationship("ProductVariable", back_populates="options")
    item_variable_options = relationship("ItemVariableOption", back_populates="variable_option")
    
    def __repr__(self):
        return f"<VariableOption(variable_option_id={self.variable_option_id}, name='{self.name}')>"


class ProductProductVariable(Base):
    """Join table to control which variables are assigned to a product and their order"""
    __tablename__ = 'product_product_variable'
    __table_args__ = {'schema': 'product'}

    product_product_variable = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.products.product_id', ondelete='CASCADE'), nullable=False)
    product_variable_id = Column(Integer, ForeignKey('product.product_variables.product_variable_id', ondelete='CASCADE'), nullable=False)
    display_order = Column(Integer)

    # Relationships
    product = relationship("Product", back_populates="product_variable_assignments")
    product_variable = relationship("ProductVariable", back_populates="product_assignments")

    def __repr__(self):
        return (
            f"<ProductProductVariable("
            f"product_product_variable={self.product_product_variable}, "
            f"product_id={self.product_id}, "
            f"product_variable_id={self.product_variable_id}, "
            f"display_order={self.display_order}"
            f")>"
        )

