// src/App.js
import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [iocs, setIocs] = useState({});
  const [findings, setFindings] = useState([]);
  const [timeline, setTimeline] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/iocs").then((res) => setIocs(res.data));
    axios.get("http://127.0.0.1:5000/api/findings").then((res) => setFindings(res.data));
    axios.get("http://127.0.0.1:5000/api/timeline").then((res) => setTimeline(res.data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>🔐 CyberSOC Intrusion Dashboard</h2>

      <h3>📌 IOCs</h3>
      <pre>{JSON.stringify(iocs, null, 2)}</pre>

      <h3>🚨 Findings</h3>
      <ul>
        {findings.map((f, i) => (
          <li key={i}>{f}</li>
        ))}
      </ul>

      <h3>📅 Timeline</h3>
      <table border="1">
        <thead>
          <tr><th>Timestamp</th><th>Description</th></tr>
        </thead>
        <tbody>
          {timeline.map((t, i) => (
            <tr key={i}>
              <td>{t.timestamp}</td>
              <td>{t.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;

