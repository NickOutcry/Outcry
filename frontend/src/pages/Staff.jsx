/**
 * Staff Page
 */
import { Card, Button } from '../components';

const Staff = () => {
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-neutral-900 dark:text-neutral-100">
          Staff
        </h1>
        <Button variant="primary">Add Staff Member</Button>
      </div>
      
      <Card>
          <p className="text-neutral-500 dark:text-neutral-400">
          Staff list will appear here
        </p>
      </Card>
    </div>
  );
};

export default Staff;

