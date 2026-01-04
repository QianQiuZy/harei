import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import BackgroundRotator from '../components/BackgroundRotator'
import FullscreenCard from '../components/FullscreenCard'

export default function HistoryPage() {
  const [items, setItems] = useState([])
  const [tags, setTags] = useState([])
  const [selectedTag, setSelectedTag] = useState('')
  const [activeItem, setActiveItem] = useState(null)

  const fetchItems = (tag) => {
    const url = tag ? `/api/messages/history?tag=${encodeURIComponent(tag)}` : '/api/messages/history'
    fetch(url)
      .then((res) => res.json())
      .then((data) => setItems(data.items || []))
  }

  useEffect(() => {
    fetchItems('')
    fetch('/api/tags')
      .then((res) => res.json())
      .then((data) => setTags(data.items || []))
  }, [])

  const onTagChange = (tag) => {
    setSelectedTag(tag)
    fetchItems(tag)
  }

  return (
    <div className="page">
      <BackgroundRotator />
      <div className="container">
        <header className="page-header">
          <h1>历史提问箱</h1>
          <nav>
            <Link to="/">返回首页</Link>
          </nav>
        </header>
        <div className="card filter-bar">
          <span>Tag 过滤:</span>
          <select value={selectedTag} onChange={(e) => onTagChange(e.target.value)}>
            <option value="">全部</option>
            {tags.map((tag) => (
              <option key={tag} value={tag}>
                {tag}
              </option>
            ))}
          </select>
        </div>
        <div className="card-grid">
          {items.map((item) => (
            <button
              key={item.message_id}
              className="card card-button"
              onClick={() => setActiveItem(item)}
            >
              <h3>{item.tag || '未命名 Tag'}</h3>
              <p>{item.message_text}</p>
              <div className="thumbnail-list">
                {item.images.map((img) => (
                  <img key={img.thumbnail} src={img.thumbnail} alt="thumbnail" />
                ))}
              </div>
              <span className="muted">{new Date(item.created_at).toLocaleString()}</span>
            </button>
          ))}
        </div>
      </div>
      <FullscreenCard open={!!activeItem} onClose={() => setActiveItem(null)}>
        {activeItem && (
          <div className="preview-card">
            <h3>{activeItem.tag || '未命名 Tag'}</h3>
            <p>{activeItem.message_text}</p>
            <div className="image-viewer">
              {activeItem.images.map((img) => (
                <img key={img.url} src={img.url} alt="full" />
              ))}
            </div>
          </div>
        )}
      </FullscreenCard>
    </div>
  )
}
