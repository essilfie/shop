import React from "react"
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import "./App.css"

import Simple from "./components/simple"
import Fish from "./components/fish"

function App() {
    return (
        <div className="App">
            <h1>My first shop</h1>
            <Router>
                <Routes>
                    <Route path="/" element={<Simple />} />
                    <Route path="/api" element={<Fish />} />
                </Routes>
            </Router>
        </div>
    )
}

export default App
