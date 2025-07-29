import '../styles/globals.css'
import type { AppProps } from 'next/app'
import 'katex/dist/katex.min.css'
import Header from '../components/mainheader'

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div className="min-h-screen" style={{ backgroundColor: '#5d5d81' }}>
      <main className="p-8 space-y-8 max-w-5xl mx-auto">
        {/* Title and Menu Bar */}
        <Header />
        

        {/* Content area with darker background */}
        <div 
          className="p-6 rounded-lg"
          style={{ backgroundColor: '#4a4a6b' }}
        >
          <Component {...pageProps} />
        </div>
      </main>
    </div>
  )
}