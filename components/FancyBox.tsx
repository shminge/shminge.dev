export default function FancyBox({ children }: { children: React.ReactNode }) {
    return (
        <div style={{
            border: '2px solid #666',
            padding: '1rem',
            borderRadius: '8px',
            background: '#eee'
        }}>
            {children}
        </div>
    )
}
