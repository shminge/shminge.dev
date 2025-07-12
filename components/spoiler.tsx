import { useState } from "react"

export default function Spoiler({ children }: { children: React.ReactNode }) {
  const [revealed, setRevealed] = useState(false)

  return (
    <span
      onClick={() => setRevealed(true)}
      className={`inline-block rounded px-1 transition-all duration-300 ${
        revealed
          ? "text-black bg-black/20"
          : "bg-black text-black brightness-0 cursor-pointer"
      }`}
    >
      {children}
    </span>
  )
}
