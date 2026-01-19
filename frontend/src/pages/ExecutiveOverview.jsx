import React, { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { AlertTriangle, Users, Clock, TrendingUp, Shield } from 'lucide-react'
import api from '../services/api'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8']

export default function ExecutiveOverview() {
  const [kpis, setKpis] = useState(null)
  const [alertTrends, setAlertTrends] = useState([])
  const [signInStats, setSignInStats] = useState(null)
  const [mfaStats, setMfaStats] = useState(null)
  const [filters, setFilters] = useState({
    startDate: '',
    endDate: '',
    user: '',
    scenarioType: '',
    severity: ''
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchData()
  }, [filters])

  const fetchData = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filters.startDate) params.append('start_date', filters.startDate)
      if (filters.endDate) params.append('end_date', filters.endDate)
      if (filters.user) params.append('user', filters.user)
      if (filters.scenarioType) params.append('scenario_type', filters.scenarioType)
      if (filters.severity) params.append('severity', filters.severity)

      const [kpisRes, trendsRes, signInRes, mfaRes] = await Promise.all([
        api.get(`/dashboard/kpis?${params}`),
        api.get(`/dashboard/alert-trends?${params}`),
        api.get(`/dashboard/sign-in-stats?${params}`),
        api.get(`/dashboard/mfa-stats?${params}`)
      ])

      setKpis(kpisRes.data)
      setAlertTrends(trendsRes.data)
      setSignInStats(signInRes.data)
      setMfaStats(mfaRes.data)
    } catch (error) {
      console.error('Error fetching data:', error)
      setError(`Failed to connect to backend. Make sure it's running on http://localhost:8000. Error: ${error.message}`)
      // Set default values on error
      setKpis({ total_alerts: 0, high_severity_alerts: 0, distinct_impacted_users: 0, mttd_minutes: 0, mttr_minutes: 0, top_tactics: [] })
      setAlertTrends([])
      setSignInStats({ success: 0, fail: 0 })
      setMfaStats({ pass: 0, fail: 0, timeout: 0 })
    } finally {
      setLoading(false)
    }
  }

  // Debug: Always show something
  useEffect(() => {
    console.log('ExecutiveOverview mounted')
    console.log('Loading:', loading)
    console.log('KPIs:', kpis)
    console.log('Error:', error)
  }, [loading, kpis, error])

  if (loading && !kpis) {
    return (
      <div className="text-center py-12">
        <div className="text-lg font-semibold">Loading dashboard data...</div>
        <div className="text-sm text-gray-500 mt-2">Connecting to backend API...</div>
      </div>
    )
  }

  // Ensure we have default values
  const displayKpis = kpis || { total_alerts: 0, high_severity_alerts: 0, distinct_impacted_users: 0, mttd_minutes: 0, mttr_minutes: 0, top_tactics: [] }
  const displaySignInStats = signInStats || { success: 0, fail: 0 }
  const displayMfaStats = mfaStats || { pass: 0, fail: 0, timeout: 0 }

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg">
          <p className="font-medium">Connection Error</p>
          <p className="text-sm">{error}</p>
          <p className="text-sm mt-2">Make sure the backend is running: <code className="bg-red-100 px-2 py-1 rounded">uvicorn app.main:app --reload</code></p>
        </div>
      )}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Executive Security Overview</h2>
      </div>

      {/* Filters */}
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
            <input
              type="date"
              value={filters.startDate}
              onChange={(e) => setFilters({ ...filters, startDate: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
            <input
              type="date"
              value={filters.endDate}
              onChange={(e) => setFilters({ ...filters, endDate: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">User</label>
            <input
              type="text"
              value={filters.user}
              onChange={(e) => setFilters({ ...filters, user: e.target.value })}
              placeholder="Filter by user"
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Scenario</label>
            <select
              value={filters.scenarioType}
              onChange={(e) => setFilters({ ...filters, scenarioType: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">All</option>
              <option value="mfa_fatigue">MFA Fatigue</option>
              <option value="impossible_travel">Impossible Travel</option>
              <option value="oauth_abuse">OAuth Abuse</option>
              <option value="privilege_escalation">Privilege Escalation</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Severity</label>
            <select
              value={filters.severity}
              onChange={(e) => setFilters({ ...filters, severity: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="">All</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Alerts</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{displayKpis.total_alerts || 0}</p>
            </div>
            <AlertTriangle className="h-8 w-8 text-red-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">High Severity</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{displayKpis.high_severity_alerts || 0}</p>
            </div>
            <Shield className="h-8 w-8 text-orange-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Impacted Users</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{displayKpis.distinct_impacted_users || 0}</p>
            </div>
            <Users className="h-8 w-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">MTTD (min)</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{displayKpis.mttd_minutes?.toFixed(1) || '0'}</p>
            </div>
            <Clock className="h-8 w-8 text-green-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">MTTR (min)</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">{displayKpis.mttr_minutes?.toFixed(1) || '0'}</p>
            </div>
            <TrendingUp className="h-8 w-8 text-purple-500" />
          </div>
        </div>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Alerts Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={alertTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="count" stroke="#0ea5e9" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top MITRE Tactics</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={displayKpis.top_tactics || []}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="tactic" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Sign-In Results</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={[
                  { name: 'Success', value: displaySignInStats.success || 0 },
                  { name: 'Fail', value: displaySignInStats.fail || 0 }
                ]}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                <Cell fill="#00C49F" />
                <Cell fill="#FF8042" />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">MFA Results</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={[
              { name: 'Pass', value: displayMfaStats.pass || 0 },
              { name: 'Fail', value: displayMfaStats.fail || 0 },
              { name: 'Timeout', value: displayMfaStats.timeout || 0 }
            ]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
