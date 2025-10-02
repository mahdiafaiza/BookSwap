import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Tasks from "./pages/Tasks";
import BookGallery from "./pages/BookGallery";
import BooksPage from "./pages/BooksPage";
import MySwapRequestsPage from "./pages/MySwapRequestsPage";
import SwapRequestsOwnerPage from "./pages/SwapRequestsOwnerPage";
import { useAuth } from "./context/AuthContext";

// ✅ Protected route wrapper
function PrivateRoute({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected routes */}
        <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
        <Route path="/tasks" element={<PrivateRoute><Tasks /></PrivateRoute>} />
        <Route path="/books" element={<PrivateRoute><BooksPage /></PrivateRoute>} />
        <Route path="/swap-requests/owner" element={<PrivateRoute><SwapRequestsOwnerPage /></PrivateRoute>} />
        <Route path="/swap-requests/requester" element={<PrivateRoute><MySwapRequestsPage /></PrivateRoute>} />

        {/* Public landing page */}
        <Route path="/" element={<BookGallery />} />
      </Routes>
    </Router>
  );
}

export default App;
