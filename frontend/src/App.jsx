import { useState, useEffect } from "react"

function ScoreBadge({ score }) {
  const color = score >= 80 ? "#ef4444" : score >= 50 ? "#f59e0b" : "#10b981"
  return (
    <span style={{
      backgroundColor: color,
      color: "white",
      padding: "4px 12px",
      borderRadius: "20px",
      fontWeight: "bold",
      fontSize: "14px"
    }}>
      {score}/100
    </span>
  )
}

function ReviewCard({ review }) {
  return (
    <div style={{
      border: "1px solid #e2e8f0",
      borderRadius: "12px",
      padding: "20px",
      marginBottom: "16px",
      backgroundColor: "white",
      boxShadow: "0 2px 4px rgba(0,0,0,0.05)"
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
        <div>
          <h3 style={{ margin: 0, color: "#1e293b" }}>{review.repo} — PR #{review.pr_number}</h3>
          <p style={{ margin: "4px 0 0", color: "#64748b", fontSize: "14px" }}>{review.created_at}</p>
        </div>
        <ScoreBadge score={review.roast_score} />
      </div>
      <p style={{ fontStyle: "italic", color: "#475569" }}>{review.summary}</p>
      <div style={{ marginTop: "12px" }}>
        <h4 style={{ color: "#ef4444" }}>Critical Issues</h4>
        <ul>{review.critical.map((c, i) => <li key={i}>{c}</li>)}</ul>
        <h4 style={{ color: "#f59e0b" }}>Warnings</h4>
        <ul>{review.warnings.map((w, i) => <li key={i}>{w}</li>)}</ul>
        <h4 style={{ color: "#10b981" }}>Suggestions</h4>
        <ul>{review.suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul>
      </div>
    </div>
  )
}

export default function App() {
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch("http://13.212.169.213:8000/reviews")
      .then(res => res.json())
      .then(data => {
        setReviews(data)
        setLoading(false)
      })
  }, [])

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "40px 20px", fontFamily: "sans-serif", backgroundColor: "#f8fafc", minHeight: "100vh" }}>
      <h1 style={{ color: "#1e293b", marginBottom: "8px" }}>PR Roaster</h1>
      <p style={{ color: "#64748b", marginBottom: "32px" }}>AI-powered code review history</p>
      {loading ? (
        <p>Loading reviews...</p>
      ) : reviews.length === 0 ? (
        <p>No reviews yet. Open a PR to get roasted!</p>
      ) : (
        reviews.map(review => <ReviewCard key={review.id} review={review} />)
      )}
    </div>
  )
}