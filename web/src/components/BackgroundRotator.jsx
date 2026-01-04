import React, { useEffect, useState } from 'react'

export default function BackgroundRotator() {
  const [backgrounds, setBackgrounds] = useState([])
  const [index, setIndex] = useState(0)

  useEffect(() => {
    fetch('/api/backgrounds')
      .then((res) => res.json())
      .then((data) => setBackgrounds(data.items || []))
      .catch(() => setBackgrounds([]))
  }, [])

  useEffect(() => {
    if (backgrounds.length <= 1) return
    const timer = setInterval(() => {
      setIndex((prev) => (prev + 1) % backgrounds.length)
    }, 5000)
    return () => clearInterval(timer)
  }, [backgrounds])

  if (backgrounds.length === 0) return null

  return (
    <div className="background-rotator">
      {backgrounds.map((bg, i) => (
        <div
          key={bg}
          className={`background-layer ${i === index ? 'active' : ''}`}
          style={{ backgroundImage: `url(${bg})` }}
        />
      ))}
    </div>
  )
}
