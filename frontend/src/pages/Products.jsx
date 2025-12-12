/**
 * Products Page
 */
import { Card, Button } from '../components';

const Products = () => {
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-neutral-900 dark:text-neutral-100">
          Products
        </h1>
        <Button variant="primary">New Product</Button>
      </div>
      
      <Card>
          <p className="text-neutral-500 dark:text-neutral-400">
          Products list will appear here
        </p>
      </Card>
    </div>
  );
};

export default Products;

