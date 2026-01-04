import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import BackgroundRotator from '../components/BackgroundRotator'
import FullscreenCard from '../components/FullscreenCard'

export default function HomePage() {
  const [messageText, setMessageText] = useState('')
  const [tag, setTag] = useState('')
  const [files, setFiles] = useState([])
  const [status, setStatus] = useState('')
  const [previewOpen, setPreviewOpen] = useState(false)

  const submitMessage = async (event) => {
    event.preventDefault()
    setStatus('提交中...')
    const formData = new FormData()
    formData.append('message_text', messageText)
    formData.append('tag', tag)
    files.forEach((file) => formData.append('images', file))

    const res = await fetch('/api/messages', { method: 'POST', body: formData })
    if (!res.ok) {
      setStatus('提交失败，请稍后重试')
      return
    }
    setStatus('提交成功，等待审核')
    setMessageText('')
    setTag('')
    setFiles([])
  }

  return (
    <div className="page">
      <BackgroundRotator />
      <div className="container">
        <header className="page-header">
          <h1>提问箱</h1>
          <nav>
            <Link to="/history">历史提问箱</Link>
            <Link to="/message">管理入口</Link>
          </nav>
        </header>
        <form className="card" onSubmit={submitMessage}>
          <h2>留言</h2>
          <label>
            Tag
            <input value={tag} onChange={(e) => setTag(e.target.value)} placeholder="可选" />
          </label>
          <label>
            内容
            <textarea
              value={messageText}
              onChange={(e) => setMessageText(e.target.value)}
              placeholder="写下你的问题"
              required
            />
          </label>
          <label>
            图片
            <input
              type="file"
              accept="image/*"
              multiple
              onChange={(e) => setFiles([...e.target.files])}
            />
          </label>
          <div className="actions">
            <button type="submit">提交</button>
            <button type="button" className="secondary" onClick={() => setPreviewOpen(true)}>
              预览卡片
            </button>
          </div>
          {status && <p className="status">{status}</p>}
        </form>
      </div>
      <FullscreenCard open={previewOpen} onClose={() => setPreviewOpen(false)}>
        <div className="preview-card">
          <h3>{tag || '未命名 Tag'}</h3>
          <p>{messageText || '这里是提问内容预览'}</p>
        </div>
      </FullscreenCard>
    </div>
  )
}
