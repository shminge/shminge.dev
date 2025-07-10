import Link from 'next/link'

export default function Home() {
    return (
        <main style={{ padding: '2rem' }}>
            <h1 className="bg-red-500 text-white p-4 rounded">My Blog</h1>
            <p>This is heavily under construction. Check back later!</p>
            <ul>
                <li><Link href="/blog/hello-world">Hello World</Link></li>
            </ul>
        </main>
    )
}
