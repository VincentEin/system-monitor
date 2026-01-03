import { useEffect, useState } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function App() {
  const [metrics, setMetrics] = useState([])

  const fetchMetrics = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/metrics')
      setMetrics(response.data)
    } catch (error) {
      console.error("Kunde inte hämta data:", error)
    }
  }

  const clearHistory = async () => {
    try {
      await axios.delete('http://localhost:5001/api/metrics')
      setMetrics([]) 
    } catch (error) {
      console.error("Kunde inte rensa historik:", error)
    }
  }

  useEffect(() => {
    fetchMetrics()
    const interval = setInterval(fetchMetrics, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <h1>System Monitor</h1>
      
      {/* 1. Flytta rubriken hit, utanför diven med fast höjd */}
      <h3 style={{ marginTop: '2rem' }}>CPU & RAM Usage (%)</h3>

      {/* 2. Denna div ska BARA innehålla grafen för att höjden ska bli rätt */}
      <div style={{ width: '100%', height: 400, marginBottom: '20px' }}>
        {metrics.length > 0 ? (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={metrics}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="created_at" tick={false} />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="cpu_usage" stroke="#8884d8" name="CPU %" strokeWidth={2} />
              <Line type="monotone" dataKey="ram_usage" stroke="#82ca9d" name="RAM %" strokeWidth={2} />
              <Line type="monotone" dataKey="disk_usage" stroke="#ff7300" name="Disk %" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p>Väntar på data från agenten...</p>
        )}
      </div>

      {/* 3. Knappen fungerar nu eftersom grafen inte täcker den */}
      <button 
        onClick={clearHistory}
        style={{
          padding: '10px 20px',
          backgroundColor: '#ff4d4f',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          fontWeight: 'bold',
          marginBottom: '20px' // Lite luft under knappen också
        }}
      >
        🗑️ Rensa Historik
      </button>

      <div style={{ marginTop: '20px' }}>
        <h3>Senaste mätvärdena:</h3>
        {metrics.slice(-3).reverse().map((m) => (
          <div key={m.id || m.timestamp || Math.random()} style={{ borderBottom: '1px solid #ddd', padding: '5px' }}>
            <strong>{m.created_at}:</strong> CPU: {m.cpu_usage}% | RAM: {m.ram_usage}% | Disk: {m.disk_usage}%
          </div>
        ))}
      </div>
    </div>
  )
}

export default App