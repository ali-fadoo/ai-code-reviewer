import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import ReviewDetailPage from "./pages/ReviewDetail";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-zinc-950">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/review/:id" element={<ReviewDetailPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
