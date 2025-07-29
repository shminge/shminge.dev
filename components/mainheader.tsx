import Link from "next/link";

export default function Header() {
    return(
        <header 
            className="text-white p-4 rounded flex justify-between items-center"
            style={{ backgroundColor: '#3e3e5c' }}
        >
            <h1 className="text-2xl font-bold">shminge</h1>
            <nav className="space-x-4">
                <Link href="/" className="hover:underline" style={{ color: '#e9d758' }}>
                    Home
                </Link>
                <Link href="/blog" className="hover:underline" style={{ color: '#e9d758' }}>
                    Blog
                </Link>
            </nav>
        </header>
    )
}