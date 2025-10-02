# 📚 Book Swap Application

A simple and interactive platform for students and readers to exchange books.
Users can list their own books, browse others’ listings, and send or accept swap requests.
The platform fosters community-driven knowledge sharing while making it easier to discover new reads. 

---

## 🚀 Features

### User Management  
- User Registration & Authentication (JWT-based)  
- Login / Logout  
- Profile Management (Update name, university, address, etc.)  

### Book Management  
- Add Books (Title, Author, Condition, Description)
- View Books (Own listings & community listings)
- Update Book Details
- Delete Books  

### Swap System  
- Send Swap Requests (to other users)
- Accept / Reject Swap Requests
- Track Swap History  

---

## System Architecture  

The platform is structured into Frontend, Backend, and Database components with modular services.
- Frontend: React.js
- Backend: Python + Node.js + Express
- Database: MongoDB
- CI/CD Pipeline: AWS (EC2 Instance)

---

## Technical Stack Info

- **Frontend**: React.js  
- **Backend**: Python + Node.js + Express  
- **Database**: MongoDB  
- **Cloud Deployment**: AWS (EC2, CI/CD pipeline)  

---

## Getting Started  

### Prerequisites  
- Python
- Node.js & npm  
- MongoDB  
- AWS Account (for deployment)  

### Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/mahdiafaiza/BookSwap.git
   cd Freelancer-Project-Bidding-Platform
   ```

2. Install dependencies:  
   ```bash
   npm run install-all
   ```

3. Start backend server & frontend concurrently:  
   ```bash
   npm start
   ```

---

## License  
This project is licensed under the **MIT License** – feel free to use and modify.  

---

## Useful Links  
- 🌐 [Project Website](http://x.x.x.x:5001)