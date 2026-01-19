import React, { useState, useEffect } from 'react'
import { format } from 'date-fns'
import { Clock, MapPin, User, Shield, AlertTriangle } from 'lucide-react'
import api from '../services/api'

export default function AttackTimeline() {
  const [timeline, setTimeline] = useState([])
  const [selectedEvent, setSelectedEvent] = useState(null)
  const [relatedEvents, setRelatedEvents] = useState([])
  const [filters, setFilters] = useState({
    scenarioType: '',
    user: ''
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTimeline()
  }, [filters])

  const fetchTimeline = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filters.scenarioType) params.append('scenario_type', filters.scenarioType)
      if (filters.user) params.append('user', filters.user)

      const res = await api.get(`/events/timeline?${params}`)
      setTimeline(res.data)
    } catch (error) {
      console.error('Error fetching timeline:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleEventClick = async (event) => {
    setSelectedEvent(event)
    try {
      const params = new URLSearchParams()
      if (event.user) params.append('user', event.user)
      if (event.detection_id) params.append('detection_id', event.detection_id)
      
      const res = await api.get(`/events?${params}`)
      setRelatedEvents(res.data.events || [])
    } catch (error) {
      console.error('Error fetching related events:', error)
    }
  }

  const getEventIcon = (eventType) => {
    switch (eventType) {
      case 'detection':
        return <Shield className="h-5 w-5 text-red-500" />
      case 'attack':
        return <AlertTriangle className="h-5 w-5 text-orange-500" />
      default:
        return <Clock className="h-5 w-5 text-gray-400" />
    }
  }

  const getEventColor = (eventType) => {
    switch (eventType) {
      case 'detection':
        return 'bg-red-100 border-red-300'
      case 'attack':
        return 'bg-orange-100 border-orange-300'
      default:
        return 'bg-gray-100 border-gray-300'
    }
  }

  // Group events by scenario
  const groupedTimeline = timeline.reduce((acc, event) => {
    const key = event.scenario_type || 'normal'
    if (!acc[key]) acc[key] = []
    acc[key].push(event)
    return acc
  }, {})

  if (loading) {
    return <div className="text-center py-12">Loading timeline...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Attack Timeline (Simulation View)</h2>
        <div className="flex gap-4">
          <select
            value={filters.scenarioType}
            onChange={(e) => setFilters({ ...filters, scenarioType: e.target.value })}
            className="px-4 py-2 border border-gray-300 rounded-md"
          >
            <option value="">All Scenarios</option>
            <option value="mfa_fatigue">MFA Fatigue</option>
            <option value="impossible_travel">Impossible Travel</option>
            <option value="oauth_abuse">OAuth Abuse</option>
            <option value="privilege_escalation">Privilege Escalation</option>
          </select>
          <input
            type="text"
            value={filters.user}
            onChange={(e) => setFilters({ ...filters, user: e.target.value })}
            placeholder="Filter by user"
            className="px-4 py-2 border border-gray-300 rounded-md"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Timeline */}
        <div className="lg:col-span-2 space-y-6">
          {Object.entries(groupedTimeline).map(([scenario, events]) => (
            <div key={scenario} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 capitalize">
                {scenario.replace('_', ' ')} Scenario
              </h3>
              <div className="relative">
                {/* Timeline line */}
                <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gray-300"></div>
                
                <div className="space-y-4">
                  {events.map((event, idx) => (
                    <div
                      key={event.id}
                      className={`relative flex items-start cursor-pointer hover:opacity-80 transition-opacity ${getEventColor(event.event_type)} rounded-lg p-4 border-2`}
                      onClick={() => handleEventClick(event)}
                    >
                      <div className="absolute left-0 top-4 w-12 flex justify-center">
                        {getEventIcon(event.event_type)}
                      </div>
                      <div className="ml-16 flex-1">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium text-gray-900 capitalize">
                            {event.event_type}
                          </span>
                          <span className="text-xs text-gray-500">
                            {format(new Date(event.timestamp), 'MMM dd, HH:mm')}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-1">{event.description}</p>
                        {event.mitre_tactic && (
                          <div className="mt-2 flex gap-2">
                            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                              {event.mitre_tactic}
                            </span>
                            {event.mitre_technique && (
                              <span className="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">
                                {event.mitre_technique}
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Event Details Panel */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Event Details</h3>
          {selectedEvent ? (
            <div className="space-y-4">
              <div>
                <p className="text-sm font-medium text-gray-700">Type</p>
                <p className="text-sm text-gray-900 capitalize">{selectedEvent.event_type}</p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">Timestamp</p>
                <p className="text-sm text-gray-900">
                  {format(new Date(selectedEvent.timestamp), 'PPpp')}
                </p>
              </div>
              <div>
                <p className="text-sm font-medium text-gray-700">User</p>
                <p className="text-sm text-gray-900">{selectedEvent.user}</p>
              </div>
              {selectedEvent.mitre_tactic && (
                <div>
                  <p className="text-sm font-medium text-gray-700">MITRE Tactic</p>
                  <p className="text-sm text-gray-900">{selectedEvent.mitre_tactic}</p>
                </div>
              )}
              {selectedEvent.mitre_technique && (
                <div>
                  <p className="text-sm font-medium text-gray-700">MITRE Technique</p>
                  <p className="text-sm text-gray-900">{selectedEvent.mitre_technique}</p>
                </div>
              )}
              {selectedEvent.detection_id && (
                <div>
                  <p className="text-sm font-medium text-gray-700">Detection ID</p>
                  <p className="text-sm text-gray-900">{selectedEvent.detection_id}</p>
                </div>
              )}
            </div>
          ) : (
            <p className="text-sm text-gray-500">Click an event to view details</p>
          )}

          {relatedEvents.length > 0 && (
            <div className="mt-6">
              <h4 className="text-sm font-semibold text-gray-900 mb-2">Related Events</h4>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {relatedEvents.slice(0, 5).map((event) => (
                  <div key={event.id} className="text-xs bg-gray-50 p-2 rounded">
                    <p className="font-medium">{event.user}</p>
                    <p className="text-gray-600">{format(new Date(event.timestamp), 'MMM dd, HH:mm')}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
