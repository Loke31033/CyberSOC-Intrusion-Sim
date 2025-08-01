import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [iocs, setIocs] = useState({});
  const [findings, setFindings] = useState([]);
  const [timeline, setTimeline] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/api/iocs").then((res) => {
      setIocs(res.data);
    });
    axios.get("http://127.0.0.1:5000/api/findings").then((res) => {
      setFindings(res.data.findings);
    });
    axios.get("http://127.0.0.1:5000/api/timeline").then((res) => {
      setTimeline(res.data.timeline);
    });
  }, []);

  return (
    <div className="App">
      <h1>🛡️ CyberSOC Intrusion Dashboard</h1>

      <section>
        <h2>🔍 Indicators of Compromise (IOCs)</h2>
        <ul>
          <li><b>Attacker IPs:</b> {iocs.attacker_ips?.join(", ")}</li>
          <li><b>Compromised Users:</b> {iocs.compromised_users?.join(", ")}</li>
          <li><b>Targets:</b> {iocs.targets?.join(", ")}</li>
        </ul>
      </section>

      <section>
        <h2>🚨 Findings</h2>
        <ul>
          {findings.map((f, idx) => (
            <li key={idx}>{f}</li>
          ))}
        </ul>
      </section>

      <section>
        <h2>📜 Timeline</h2>
        <table border="1" cellPadding="6">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {timeline.map((item, index) => (
              <tr key={index}>
                <td>{item.Timestamp}</td>
                <td>{item.Description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

export default App;

