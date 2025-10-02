import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [msg, setMsg] = useState("");

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/hello")
      .then(res => setMsg(res.data.message))
      .catch(err => console.error(err));
  }, []);

  return (

    <div className="bg-red-500 text-white text-3xl p-5">
      {msg}
      <br></br>
      If this is red with big white text, Tailwind works 🎉
    </div>
  )
  
  ;
}


export default App;
