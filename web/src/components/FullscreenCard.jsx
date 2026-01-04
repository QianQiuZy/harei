import React from 'react'

export default function FullscreenCard({ open, onClose, children }) {
  if (!open) return null
  return (
    <div className="fullscreen-overlay" onClick={onClose}>
      <div className="fullscreen-card" onClick={(e) => e.stopPropagation()}>
        <button className="fullscreen-close" onClick={onClose}>
          退出
        </button>
        <div className="fullscreen-content">{children}</div>
      </div>
    </div>
  )
}
