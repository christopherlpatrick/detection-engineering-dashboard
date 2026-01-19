import React, { useState, useEffect } from 'react'
import { User, MapPin, Smartphone, Globe, Shield, AlertTriangle, Clock } from 'lucide-react'
import { format } from 'date-fns'
import api from '../services/api'

export default function InvestigationDrillDown() {
  const [selectedUser, setSelectedUser] = useState('')
  const [investigation, setInvestigation] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleInvestigate = async () => {
    if (!selectedUser) return
    
    setLoading(true)
    try {
      const res = await api.get(`/users/${selectedUser}/investigation`)
      setInvestigation(res.data)
    } catch (error) {
      console.error('Error fetching investigation:', error)
      alert('Error fetching investigation data')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Investigation Drill-Down</h2>
      </div>

      {/* User Search */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        <div className="flex gap-4">
          <input
            type="text"
            value={selectedUser}
            onChange={(e) => setSelectedUser(e.target.value)}
            placeholder="Enter user email (e.g., alice.johnson@company.com)"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md"
          />
          <button
            onClick={handleInvestigate}
            disabled={!selectedUser || loading}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Investigating...' : 'Investigate'}
          </button>
        </div>
      </div>

      {investigation && (
        <div className="space-y-6">
          {/* User Summary */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center gap-3 mb-4">
              <User className="h-6 w-6 text-blue-600" />
              <h3 className="text-xl font-semibold text-gray-900">{investigation.user}</h3>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-600">Total Events</p>
                <p className="text-2xl font-bold text-gray-900">{investigation.events?.length || 0}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Alerts</p>
                <p className="text-2xl font-bold text-orange-600">{investigation.alerts?.length || 0}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Incidents</p>
                <p className="text-2xl font-bold text-red-600">{investigation.incidents?.length || 0}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Unique IPs</p>
                <p className="text-2xl font-bold text-gray-900">{investigation.unique_ips?.length || 0}</p>
              </div>
            </div>
          </div>

          {/* Key Information Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* IP Addresses */}
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-3">
                <Globe className="h-5 w-5 text-blue-600" />
                <h4 className="font-semibold text-gray-900">IP Addresses</h4>
              </div>
              <div className="space-y-1">
                {investigation.unique_ips?.slice(0, 5).map((ip, idx) => (
                  <p key={idx} className="text-sm text-gray-600 font-mono">{ip}</p>
                ))}
                {investigation.unique_ips?.length > 5 && (
                  <p className="text-xs text-gray-500">+{investigation.unique_ips.length - 5} more</p>
                )}
              </div>
            </div>

            {/* Devices */}
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-3">
                <Smartphone className="h-5 w-5 text-green-600" />
                <h4 className="font-semibold text-gray-900">Devices</h4>
              </div>
              <div className="space-y-1">
                {investigation.unique_devices?.slice(0, 5).map((device, idx) => (
                  <p key={idx} className="text-sm text-gray-600">{device}</p>
                ))}
              </div>
            </div>

            {/* Applications */}
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-3">
                <Globe className="h-5 w-5 text-purple-600" />
                <h4 className="font-semibold text-gray-900">Applications</h4>
              </div>
              <div className="space-y-1">
                {investigation.unique_apps?.slice(0, 5).map((app, idx) => (
                  <p key={idx} className="text-sm text-gray-600">{app}</p>
                ))}
              </div>
            </div>

            {/* OAuth Apps */}
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-3">
                <Shield className="h-5 w-5 text-orange-600" />
                <h4 className="font-semibold text-gray-900">OAuth Apps</h4>
              </div>
              <div className="space-y-1">
                {investigation.unique_oauth_apps?.length > 0 ? (
                  investigation.unique_oauth_apps.map((app, idx) => (
                    <p key={idx} className="text-sm text-gray-600">{app}</p>
                  ))
                ) : (
                  <p className="text-sm text-gray-500">None</p>
                )}
              </div>
            </div>
          </div>

          {/* Geolocation Changes */}
          {investigation.geolocation_changes && investigation.geolocation_changes.length > 0 && (
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-4">
                <MapPin className="h-5 w-5 text-red-600" />
                <h3 className="text-lg font-semibold text-gray-900">Geolocation Changes</h3>
              </div>
              <div className="space-y-3">
                {investigation.geolocation_changes.map((change, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <div>
                      <p className="font-medium text-gray-900">{change.city}, {change.country}</p>
                      <p className="text-xs text-gray-600 font-mono">{change.ip_address}</p>
                    </div>
                    <p className="text-sm text-gray-500">
                      {format(new Date(change.timestamp), 'MMM dd, HH:mm')}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Role Changes */}
          {investigation.role_changes && investigation.role_changes.length > 0 && (
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-4">
                <Shield className="h-5 w-5 text-blue-600" />
                <h3 className="text-lg font-semibold text-gray-900">Role Changes</h3>
              </div>
              <div className="space-y-3">
                {investigation.role_changes.map((change, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <div>
                      <p className="font-medium text-gray-900">{change.role_name}</p>
                      <p className="text-xs text-gray-600 font-mono">{change.ip_address}</p>
                    </div>
                    <p className="text-sm text-gray-500">
                      {format(new Date(change.timestamp), 'MMM dd, HH:mm')}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* OAuth Consents */}
          {investigation.oauth_consents && investigation.oauth_consents.length > 0 && (
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center gap-2 mb-4">
                <AlertTriangle className="h-5 w-5 text-orange-600" />
                <h3 className="text-lg font-semibold text-gray-900">OAuth Consents</h3>
              </div>
              <div className="space-y-3">
                {investigation.oauth_consents.map((consent, idx) => (
                  <div key={idx} className="p-3 bg-gray-50 rounded">
                    <div className="flex items-center justify-between mb-2">
                      <p className="font-medium text-gray-900">{consent.app_name}</p>
                      <p className="text-sm text-gray-500">
                        {format(new Date(consent.timestamp), 'MMM dd, HH:mm')}
                      </p>
                    </div>
                    <p className="text-xs text-gray-600 mb-1">Scopes: {consent.scopes}</p>
                    <p className="text-xs text-gray-500 font-mono">IP: {consent.ip_address}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recent Events */}
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Sign-In History</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Timestamp</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Result</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">MFA</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Risk</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Location</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">IP</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {investigation.events?.slice(0, 10).map((event) => (
                    <tr key={event.id}>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                        {format(new Date(event.timestamp), 'MMM dd, HH:mm')}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          event.sign_in_result === 'success' 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {event.sign_in_result || 'N/A'}
                        </span>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                        {event.mfa_result || 'N/A'}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          event.risk_level === 'high' 
                            ? 'bg-red-100 text-red-800'
                            : event.risk_level === 'medium'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-blue-100 text-blue-800'
                        }`}>
                          {event.risk_level || 'N/A'}
                        </span>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                        {event.geo_city}, {event.geo_country}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-600 font-mono">
                        {event.ip_address}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
