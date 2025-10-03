import { useState, useEffect } from 'react';
import axiosInstance from '../axiosConfig';
import { useAuth } from '../context/AuthContext';

const LandingPage = () => {
  const { user } = useAuth();

  return (
    <div className="container mx-auto px-6 py-10 bg-gray-100 min-h-screen">
      {/* Hero Section */}
      <section class="py-16 sm:py-24 lg:py-32 bg-white text-center">
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Tagline */}
                <p class="text-secondary font-semibold uppercase tracking-wider mb-3">Sustainable Reading, Free Exchange</p>
                {/* Main Headline */}
                <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold leading-tight text-text-dark mb-6">
                    Swap Your Reads. <span class="text-primary block lg:inline">Discover Your Next Favorite Book.</span>
                </h1>
                {/* Subheadline */}
                <p class="text-lg sm:text-xl text-gray-500 mb-10 max-w-2xl mx-auto">
                    Stop collecting dust and start connecting! Easily exchange your beloved physical books with thousands of passionate readers in your local community and beyond.
                </p>

                {/* Action Button */}
                <Link
                    to="/register"
                    className="bg-green-500 px-4 py-2 rounded hover:bg-green-700"
                >
                    Register
                </Link>
            </div>
        </section>
    </div>
  );
};

export default LandingPage;
