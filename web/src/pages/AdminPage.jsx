import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const tokenKey = 'admin_token'

export default function AdminPage() {
  const [password, setPassword] = useState('')
  const [token, setToken] = useState(localStorage.getItem(tokenKey) || '')
  const [messages, setMessages] = useState([])
  const [summary, setSummary] = useState(null)
  const [statusFilter, setStatusFilter] = useState('pending')

  const fetchSummary = () => {
    fetch('/api/admin/summary', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => setSummary(data))
  }

  const fetchMessages = () => {
    const url = `/api/messages?status=${statusFilter}`
    fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setMessages(data.items || []))
  }

  useEffect(() => {
    if (token) {
      fetchSummary()
      fetchMessages()
    }
  }, [token, statusFilter])

  const login = async () => {
    const res = await fetch('/api/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password }),
    })
    if (!res.ok) return
    const data = await res.json()
    localStorage.setItem(tokenKey, data.token)
    setToken(data.token)
    setPassword('')
  }

  const updateStatus = async (messageId, status) => {
    await fetch(`/api/messages/${messageId}/status`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ status }),
    })
    fetchMessages()
    fetchSummary()
  }

  if (!token) {
    return (
      <div className="page">
        <div className="container">
          <header className="page-header">
            <h1>管理登录</h1>
            <nav>
              <Link to="/">返回首页</Link>
            </nav>
          </header>
          <div className="card">
            <label>
              管理密码
              <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" />
            </label>
            <button onClick={login}>登录</button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <div className="container">
        <header className="page-header">
          <h1>管理面板</h1>
          <nav>
            <Link to="/">返回首页</Link>
          </nav>
        </header>
        {summary && (
          <div className="card summary">
            <h2>概览</h2>
            <div className="summary-grid">
              <div>
                <strong>待审核</strong>
                <span>{summary.pending}</span>
              </div>
              <div>
                <strong>已通过</strong>
                <span>{summary.approved}</span>
              </div>
              <div>
                <strong>已删除</strong>
                <span>{summary.deleted}</span>
              </div>
            </div>
          </div>
        )}
        <div className="card filter-bar">
          <span>状态筛选:</span>
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
            <option value="pending">待审核</option>
            <option value="approved">已通过</option>
            <option value="rejected">已拒绝</option>
            <option value="deleted">已删除</option>
          </select>
        </div>
        <div className="card-grid">
          {messages.map((item) => (
            <div key={item.message_id} className="card">
              <h3>{item.tag || '未命名 Tag'}</h3>
              <p>{item.message_text}</p>
              <div className="thumbnail-list">
                {item.images.map((img) => (
                  <img key={img.thumbnail} src={img.thumbnail} alt="thumb" />
                ))}
              </div>
              <div className="actions">
                <button onClick={() => updateStatus(item.message_id, 'approved')}>通过</button>
                <button className="secondary" onClick={() => updateStatus(item.message_id, 'rejected')}>
                  拒绝
                </button>
                <button className="danger" onClick={() => updateStatus(item.message_id, 'deleted')}>
                  删除
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
