import { useState, useEffect } from 'react';
import axiosInstance from '../axiosConfig';
import { useAuth } from '../context/AuthContext';

const SwapRequestsOwnerPage = () => {
  const { user } = useAuth();
  const [ownerRequests, setOwnerRequests] = useState([]);

  useEffect(() => {
    if (!user?.token) return;

    const fetchOwnerRequests = async () => {
      try {
        const res = await axiosInstance.get('/swap-requests/owner', {
          headers: { Authorization: `Bearer ${user.token}` },
        });
        setOwnerRequests(res.data);
      } catch (err) {
        console.error('Error fetching owner swap requests:', err);
        alert(err.response?.data?.message || 'Failed to fetch swap requests.');
      }
    };

    fetchOwnerRequests();
  }, [user]);

  const handleRespond = async (reqId, status) => {
    try {
      const res = await axiosInstance.put(
        `/swap-requests/${reqId}/respond`,
        { status },
        { headers: { Authorization: `Bearer ${user.token}` } }
      );

      setOwnerRequests(ownerRequests.map((r) =>
        r._id === reqId ? { ...r, status } : r
      ));
      alert(`Request ${status}`);
    } catch (err) {
      console.error('Error responding to swap request:', err);
      alert(err.response?.data?.message || 'Failed to respond');
    }
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Swap Requests on My Books</h1>

      {ownerRequests.length === 0 ? (
        <p>No swap requests for your books.</p>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {ownerRequests.map((req) => (
            <div key={req._id} className="bg-white p-4 shadow-md rounded flex flex-col justify-between">
              <div>
                <h3 className="text-xl font-semibold">{req.requestedBook?.title}</h3>
                <p className="text-gray-600">by {req.requestedBook?.author}</p>
                <p className="mt-1 text-sm">Requested by: {req.requester?.name || 'Unknown'}</p>
                <p className="mt-1 text-sm">Email: {req.requester?.email || 'Hidden'}</p>
                <p className="mt-1 text-sm">
                  Book Offered for Swap: {req.offeredBook?.title || 'None'}
                </p>
                <p className="mt-2 text-sm">Message: {req.message || 'No message'}</p>
                <p className="mt-1 font-semibold">Status: {req.status}</p>
              </div>

              {req.status === 'pending' && (
                <div className="mt-4 flex gap-2">
                  <button
                    className="flex-1 bg-green-600 text-white p-2 rounded hover:bg-green-700"
                    onClick={() => handleRespond(req._id, 'accepted')}
                  >
                    Accept
                  </button>
                  <button
                    className="flex-1 bg-red-600 text-white p-2 rounded hover:bg-red-700"
                    onClick={() => handleRespond(req._id, 'rejected')}
                  >
                    Reject
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SwapRequestsOwnerPage;
