import { useState, useEffect } from 'react';
import axiosInstance from '../axiosConfig';
import { useAuth } from '../context/AuthContext';

const MySwapRequestsPage = () => {
  const { user } = useAuth();
  const [myRequests, setMyRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!user?.token) return;

    const fetchRequests = async () => {
      setLoading(true);
      try {
        const res = await axiosInstance.get('/swap-requests/requester', {
          headers: { Authorization: `Bearer ${user.token}` },
        });
        setMyRequests(res.data);
      } catch (err) {
        console.error('Error fetching my swap requests:', err);
        setError(err.response?.data?.message || 'Failed to fetch your swap requests.');
      } finally {
        setLoading(false);
      }
    };

    fetchRequests();
  }, [user]);

  if (loading) return <p className="p-6">Loading requests...</p>;
  if (error) return <p className="p-6 text-red-600">{error}</p>;

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">My Swap Requests</h1>

      {myRequests.length === 0 ? (
        <p>You haven't made any swap requests yet.</p>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {myRequests.map((req) => (
            <div key={req._id} className="bg-white p-4 shadow-md rounded flex flex-col justify-between">
              <div>
                <h2 className="text-xl font-semibold">{req.requestedBook?.title}</h2>
                <p className="text-gray-600">Author: {req.requestedBook?.author}</p>
                
                {/* Owner only shown when request is accepted */}
                {req.status === 'accepted' && (
                  <p className="text-gray-600">
                    Owner: {req.ownerId?.name} | Contact Email:  {req.ownerId?.email}
                  </p>
                )}

                {req.offeredBook && (
                  <p className="mt-1 text-sm">
                    You offered: <span className="font-semibold">{req.offeredBook.title}</span>
                  </p>
                )}

                <p className="mt-1 font-semibold">Status: {req.status}</p>
                <p className="mt-1 text-sm text-gray-500">Message: {req.message || 'No message'}</p>

                {req.createdAt && (
                  <p className="mt-2 text-xs text-gray-400">
                    Requested on: {new Date(req.createdAt).toLocaleDateString()}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MySwapRequestsPage;
