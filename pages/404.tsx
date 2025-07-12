export default function Custom404() {
  return (
    <main className="flex  flex-col items-center justify-center bg-white text-gray-900 p-4">
      <h1 className="text-6xl font-bold">404</h1>
      <p className="mt-4 text-xl">This page does not exist.</p>
      <a
        href="/"
        className="mt-6 text-blue-600 hover:underline"
      >
        Return to homepage
      </a>
    </main>
  )
}
