import React, { useState, useEffect } from 'react'
import { Shield, AlertTriangle, Search, FileText } from 'lucide-react'
import api from '../services/api'

export default function DetectionLibrary() {
  const [detections, setDetections] = useState([])
  const [selectedDetection, setSelectedDetection] = useState(null)
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchDetections()
  }, [])

  const fetchDetections = async () => {
    setLoading(true)
    try {
      const res = await api.get('/detections')
      setDetections(res.data)
    } catch (error) {
      console.error('Error fetching detections:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDetectionClick = async (detectionId) => {
    try {
      const res = await api.get(`/detections/${detectionId}`)
      setSelectedDetection(res.data)
    } catch (error) {
      console.error('Error fetching detection details:', error)
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return 'bg-red-100 text-red-800'
      case 'high':
        return 'bg-orange-100 text-orange-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-blue-100 text-blue-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const filteredDetections = detections.filter(det =>
    det.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    det.mitre_tactic?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    det.mitre_technique?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return <div className="text-center py-12">Loading detections...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Detection Library (Engineering View)</h2>
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search detections..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-md"
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Detection List */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Detection
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Tactic
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Technique
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Severity
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredDetections.map((detection) => (
                  <tr
                    key={detection.id}
                    onClick={() => handleDetectionClick(detection.detection_id)}
                    className="hover:bg-gray-50 cursor-pointer"
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{detection.name}</div>
                      <div className="text-xs text-gray-500">{detection.detection_id}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{detection.mitre_tactic}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{detection.mitre_technique}</div>
                      {detection.mitre_technique_id && (
                        <div className="text-xs text-gray-500">{detection.mitre_technique_id}</div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getSeverityColor(detection.severity)}`}>
                        {detection.severity}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Detection Details */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Detection Details</h3>
          {selectedDetection ? (
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-gray-700">Name</p>
                <p className="text-sm text-gray-900 mt-1">{selectedDetection.name}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Description</p>
                <p className="text-sm text-gray-900 mt-1">{selectedDetection.description}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Detection Logic</p>
                <p className="text-sm text-gray-900 mt-1">{selectedDetection.detection_logic}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Required Signals</p>
                <p className="text-xs text-gray-600 mt-1 font-mono bg-gray-50 p-2 rounded">
                  {selectedDetection.required_signals}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Expected False Positives</p>
                <p className="text-sm text-gray-900 mt-1">{selectedDetection.expected_false_positives}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Recommended Response</p>
                <p className="text-sm text-gray-900 mt-1">{selectedDetection.recommended_response}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">MITRE Mapping</p>
                <div className="mt-1 space-y-1">
                  <p className="text-xs text-gray-600">Tactic: {selectedDetection.mitre_tactic}</p>
                  <p className="text-xs text-gray-600">Technique: {selectedDetection.mitre_technique}</p>
                  {selectedDetection.mitre_technique_id && (
                    <p className="text-xs text-gray-600">ID: {selectedDetection.mitre_technique_id}</p>
                  )}
                </div>
              </div>
              {selectedDetection.alert_count !== undefined && (
                <div>
                  <p className="text-sm font-medium text-gray-700">Alert Count</p>
                  <p className="text-sm text-gray-900 mt-1">{selectedDetection.alert_count}</p>
                </div>
              )}
              {selectedDetection.example_events && selectedDetection.example_events.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-gray-700 mb-2">Example Triggering Events</p>
                  <div className="space-y-2 max-h-48 overflow-y-auto">
                    {selectedDetection.example_events.map((event, idx) => (
                      <div key={idx} className="text-xs bg-gray-50 p-2 rounded">
                        <p className="font-medium">{event.user}</p>
                        <p className="text-gray-600">{new Date(event.timestamp).toLocaleString()}</p>
                        <p className="text-gray-500 capitalize">{event.scenario_type}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <p className="text-sm text-gray-500">Select a detection to view details</p>
          )}
        </div>
      </div>
    </div>
  )
}
