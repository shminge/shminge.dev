import Link from 'next/link'

export default function Home() {
    return (
        <main style={{ padding: '2rem' }}>
            <h1>My Blog</h1>
            <ul>
                <li><Link href="/blog/hello-world">Hello World</Link></li>
            </ul>
        </main>
    )
}
