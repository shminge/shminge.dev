// pages/_app.tsx
import '../styles/globals.css'
import type { AppProps } from 'next/app'
import 'katex/dist/katex.min.css'
import Header from '../components/mainheader'


export default function MyApp({ Component, pageProps }: AppProps) {
  return (
          <main className="p-8 space-y-8 max-w-5xl mx-auto">
            {/* Title and Menu Bar */}
            <Header />
            <Component {...pageProps} />
          </main>
  )
}
