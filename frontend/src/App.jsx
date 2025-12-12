/**
 * Main App Component
 */
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import Jobs from './pages/Jobs';
import Products from './pages/Products';
import Staff from './pages/Staff';
import './styles/globals.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-neutral-100 dark:bg-neutral-900">
        {/* Navigation */}
        <nav className="bg-neutral-100 dark:bg-neutral-900 shadow-md">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <h1 className="text-xl font-bold text-primary">Outcry Projects</h1>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link
                    to="/"
                    className="border-transparent text-neutral-500 hover:border-neutral-300 hover:text-neutral-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium dark:text-neutral-400 dark:hover:text-neutral-200"
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/projects"
                    className="border-transparent text-neutral-500 hover:border-neutral-300 hover:text-neutral-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium dark:text-neutral-400 dark:hover:text-neutral-200"
                  >
                    Projects
                  </Link>
                  <Link
                    to="/jobs"
                    className="border-transparent text-neutral-500 hover:border-neutral-300 hover:text-neutral-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium dark:text-neutral-400 dark:hover:text-neutral-200"
                  >
                    Jobs
                  </Link>
                  <Link
                    to="/products"
                    className="border-transparent text-neutral-500 hover:border-neutral-300 hover:text-neutral-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium dark:text-neutral-400 dark:hover:text-neutral-200"
                  >
                    Products
                  </Link>
                  <Link
                    to="/staff"
                    className="border-transparent text-neutral-500 hover:border-neutral-300 hover:text-neutral-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium dark:text-neutral-400 dark:hover:text-neutral-200"
                  >
                    Staff
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/jobs" element={<Jobs />} />
            <Route path="/products" element={<Products />} />
            <Route path="/staff" element={<Staff />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

