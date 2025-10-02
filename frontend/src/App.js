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

  return <h1>{msg}</h1>;
}

export default App;
