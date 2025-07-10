import Link from "next/link";

export default function Header() {
    return(
            <header className="bg-green-300 text-white p-4 rounded flex justify-between items-center">
                <h1 className="text-2xl font-bold">shminge</h1>
                <nav className="space-x-4">
                    <Link href="/" className="hover:underline">Home</Link>
                    <Link href="/blog" className="hover:underline">Blog</Link>
                </nav>
            </header>
    )
}