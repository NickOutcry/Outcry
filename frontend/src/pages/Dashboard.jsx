/**
 * Dashboard Page
 */
import { Card } from '../components';

const Dashboard = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-neutral-900 dark:text-neutral-100 mb-6">
        Dashboard
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card title="Overview">
          <p className="text-neutral-500 dark:text-neutral-400">
            Welcome to Outcry Projects Dashboard
          </p>
        </Card>
        
        <Card title="Quick Stats">
          <p className="text-neutral-500 dark:text-neutral-400">
            Statistics will appear here
          </p>
        </Card>
        
        <Card title="Recent Activity">
          <p className="text-neutral-500 dark:text-neutral-400">
            Recent activity will appear here
          </p>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;

