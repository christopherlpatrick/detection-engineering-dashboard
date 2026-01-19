import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ExecutiveOverview from './pages/ExecutiveOverview'
import AttackTimeline from './pages/AttackTimeline'
import DetectionLibrary from './pages/DetectionLibrary'
import InvestigationDrillDown from './pages/InvestigationDrillDown'
import ResponseActions from './pages/ResponseActions'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<ExecutiveOverview />} />
          <Route path="/timeline" element={<AttackTimeline />} />
          <Route path="/detections" element={<DetectionLibrary />} />
          <Route path="/investigation" element={<InvestigationDrillDown />} />
          <Route path="/response" element={<ResponseActions />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
