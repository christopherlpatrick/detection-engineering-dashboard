import React, { useState, useEffect } from 'react'
import { Shield, UserX, Lock, Smartphone, Ban, CheckCircle, Clock, AlertCircle } from 'lucide-react'
import { format } from 'date-fns'
import api from '../services/api'

const ACTION_TYPES = [
  {
    id: 'disable_user',
    name: 'Disable User',
    icon: UserX,
    color: 'bg-red-500 hover:bg-red-600',
    description: 'Disable the user account in Azure AD'
  },
  {
    id: 'revoke_sessions',
    name: 'Revoke Sessions',
    icon: Lock,
    color: 'bg-orange-500 hover:bg-orange-600',
    description: 'Invalidate all active tokens and sessions'
  },
  {
    id: 'password_reset',
    name: 'Require Password Reset',
    icon: Shield,
    color: 'bg-yellow-500 hover:bg-yellow-600',
    description: 'Force password reset on next sign-in'
  },
  {
    id: 'isolate_endpoint',
    name: 'Isolate Endpoint',
    icon: Smartphone,
    color: 'bg-purple-500 hover:bg-purple-600',
    description: 'Isolate device from network'
  },
  {
    id: 'block_oauth',
    name: 'Block OAuth App',
    icon: Ban,
    color: 'bg-blue-500 hover:bg-blue-600',
    description: 'Revoke consent and block OAuth application'
  }
]

const STATUS_COLORS = {
  open: 'bg-gray-100 text-gray-800',
  investigating: 'bg-blue-100 text-blue-800',
  contained: 'bg-yellow-100 text-yellow-800',
  resolved: 'bg-green-100 text-green-800'
}

export default function ResponseActions() {
  const [incidents, setIncidents] = useState([])
  const [selectedIncident, setSelectedIncident] = useState(null)
  const [responseActions, setResponseActions] = useState([])
  const [loading, setLoading] = useState(true)
  const [executing, setExecuting] = useState(false)

  useEffect(() => {
    fetchIncidents()
  }, [])

  useEffect(() => {
    if (selectedIncident) {
      fetchResponseActions()
    }
  }, [selectedIncident])

  const fetchIncidents = async () => {
    setLoading(true)
    try {
      const res = await api.get('/incidents')
      setIncidents(res.data)
    } catch (error) {
      console.error('Error fetching incidents:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchResponseActions = async () => {
    if (!selectedIncident) return
    try {
      const res = await api.get(`/incidents/${selectedIncident.incident_id}/response-actions`)
      setResponseActions(res.data)
    } catch (error) {
      console.error('Error fetching response actions:', error)
    }
  }

  const handleExecuteAction = async (actionType) => {
    if (!selectedIncident) return
    
    setExecuting(true)
    try {
      const res = await api.post(`/incidents/${selectedIncident.incident_id}/response/${actionType}`)
      alert(res.data.message)
      await fetchIncidents()
      await fetchResponseActions()
      // Update selected incident
      const updatedIncident = incidents.find(i => i.incident_id === selectedIncident.incident_id)
      if (updatedIncident) {
        setSelectedIncident(updatedIncident)
      }
    } catch (error) {
      console.error('Error executing action:', error)
      alert('Error executing action')
    } finally {
      setExecuting(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading incidents...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Response Actions (Simulated)</h2>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Incidents List */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200">
            <div className="p-4 border-b border-gray-200">
              <h3 className="font-semibold text-gray-900">Active Incidents</h3>
            </div>
            <div className="divide-y divide-gray-200 max-h-96 overflow-y-auto">
              {incidents.map((incident) => (
                <div
                  key={incident.id}
                  onClick={() => setSelectedIncident(incident)}
                  className={`p-4 cursor-pointer hover:bg-gray-50 transition-colors ${
                    selectedIncident?.incident_id === incident.incident_id ? 'bg-blue-50' : ''
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-900">{incident.title}</span>
                    <span className={`px-2 py-1 text-xs rounded-full ${STATUS_COLORS[incident.status] || STATUS_COLORS.open}`}>
                      {incident.status}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mb-1">{incident.user}</p>
                  <p className="text-xs text-gray-500">
                    {format(new Date(incident.detected_at), 'MMM dd, HH:mm')}
                  </p>
                  <div className="mt-2">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      incident.severity === 'high' || incident.severity === 'critical'
                        ? 'bg-red-100 text-red-800'
                        : incident.severity === 'medium'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {incident.severity}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Response Actions Panel */}
        <div className="lg:col-span-2 space-y-6">
          {selectedIncident ? (
            <>
              {/* Incident Details */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">{selectedIncident.title}</h3>
                  <div className="flex items-center gap-2">
                    <span className={`px-3 py-1 text-sm rounded-full ${STATUS_COLORS[selectedIncident.status] || STATUS_COLORS.open}`}>
                      {selectedIncident.status}
                    </span>
                  </div>
                </div>
                <p className="text-sm text-gray-600 mb-4">{selectedIncident.description}</p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">User</p>
                    <p className="font-medium text-gray-900">{selectedIncident.user}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">Severity</p>
                    <p className="font-medium text-gray-900 capitalize">{selectedIncident.severity}</p>
                  </div>
                  <div>
                    <p className="text-gray-600">MTTD</p>
                    <p className="font-medium text-gray-900">
                      {selectedIncident.mttd_minutes?.toFixed(1) || 'N/A'} min
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-600">MTTR</p>
                    <p className="font-medium text-gray-900">
                      {selectedIncident.mttr_minutes?.toFixed(1) || 'N/A'} min
                    </p>
                  </div>
                </div>
              </div>

              {/* Response Actions */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Response Actions</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {ACTION_TYPES.map((action) => {
                    const Icon = action.icon
                    return (
                      <button
                        key={action.id}
                        onClick={() => handleExecuteAction(action.id)}
                        disabled={executing}
                        className={`${action.color} text-white p-4 rounded-lg flex items-center gap-3 transition-colors disabled:opacity-50 disabled:cursor-not-allowed`}
                      >
                        <Icon className="h-5 w-5" />
                        <div className="text-left">
                          <p className="font-medium">{action.name}</p>
                          <p className="text-xs opacity-90">{action.description}</p>
                        </div>
                      </button>
                    )
                  })}
                </div>
                <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-start gap-2">
                    <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
                    <div className="text-sm text-blue-800">
                      <p className="font-medium mb-1">Simulated Actions</p>
                      <p>All actions are simulated for demonstration purposes. In production, these actions would interact with Azure AD, Microsoft Defender, and other security tools to execute the response.</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Executed Actions History */}
              {responseActions.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Executed Actions</h3>
                  <div className="space-y-3">
                    {responseActions.map((action) => (
                      <div key={action.id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                        <div className="flex items-center gap-3">
                          <CheckCircle className="h-5 w-5 text-green-600" />
                          <div>
                            <p className="font-medium text-gray-900">{action.action_name}</p>
                            <p className="text-xs text-gray-600">{action.description}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-gray-500">
                            {format(new Date(action.executed_at), 'MMM dd, HH:mm')}
                          </p>
                          <p className="text-xs text-gray-400">Simulated</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Incident Status Timeline */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Incident Status Timeline</h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <Clock className="h-4 w-4 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Detected</p>
                      <p className="text-xs text-gray-500">
                        {format(new Date(selectedIncident.detected_at), 'PPpp')}
                      </p>
                    </div>
                  </div>
                  {selectedIncident.acknowledged_at && (
                    <div className="flex items-center gap-3">
                      <CheckCircle className="h-4 w-4 text-blue-500" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">Acknowledged</p>
                        <p className="text-xs text-gray-500">
                          {format(new Date(selectedIncident.acknowledged_at), 'PPpp')}
                        </p>
                      </div>
                    </div>
                  )}
                  {selectedIncident.contained_at && (
                    <div className="flex items-center gap-3">
                      <Shield className="h-4 w-4 text-yellow-500" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">Contained</p>
                        <p className="text-xs text-gray-500">
                          {format(new Date(selectedIncident.contained_at), 'PPpp')}
                        </p>
                      </div>
                    </div>
                  )}
                  {selectedIncident.resolved_at && (
                    <div className="flex items-center gap-3">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">Resolved</p>
                        <p className="text-xs text-gray-500">
                          {format(new Date(selectedIncident.resolved_at), 'PPpp')}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
              <Shield className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">Select an incident to view response actions</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
