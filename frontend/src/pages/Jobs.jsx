/**
 * Jobs Page
 */
import { Card, Button } from '../components';

const Jobs = () => {
  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-neutral-900 dark:text-neutral-100">
          Jobs
        </h1>
        <Button variant="primary">New Job</Button>
      </div>
      
      <Card>
          <p className="text-neutral-500 dark:text-neutral-400">
          Jobs list will appear here
        </p>
      </Card>
    </div>
  );
};

export default Jobs;

