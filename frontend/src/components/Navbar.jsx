// src/components/Navbar.jsx
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-purple-900 text-white px-6 py-4 flex justify-between items-center shadow-lg">
      {/* Logo / Home link */}
      <Link to="/" className="text-2xl font-bold hover:text-gray-200 transition">
        📚 BookSwap
      </Link>

      {/* Links */}
      <div className="flex items-center space-x-4">
        {user ? (
          <>
            <Link to="/" className="hover:text-gray-300">Gallery</Link>
            <Link to="/books" className="hover:text-gray-300">Books</Link>
            <Link to="/swap-requests/owner" className="hover:text-gray-300">Swap Requests</Link>
            <Link to="/swap-requests/requester" className="hover:text-gray-300">My Requests</Link>
            <Link
              to="/profile"
              className="px-3 py-1 bg-blue-700 rounded-lg hover:bg-blue-600 transition"
            >
              {user.name ? `Hi, ${user.name}` : 'Profile'}
            </Link>
            <button
              onClick={handleLogout}
              className="bg-red-600 px-3 py-1 rounded-lg hover:bg-red-500 transition"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:text-gray-300">Login</Link>
            <Link
              to="/register"
              className="px-3 py-1 bg-green-600 rounded-lg hover:bg-green-500 transition"
            >
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
