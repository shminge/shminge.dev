import Link from 'next/link'
import Header from '../components/mainheader'
import LinkWidget, { LinkWidgetProps } from '../components/linkwidget'

const links: LinkWidgetProps[] = [
    {
        icon: 'https://cdn-icons-png.flaticon.com/512/25/25231.png',
        altText: 'Github',
        link: 'https://github.com/shminge',
        backgroundColour: '#F0F6FC',
    },
    {
        icon: 'https://cdn-icons-png.flaticon.com/512/15707/15707956.png',
        altText: 'LinkedIn',
        link: 'https://www.linkedin.com/in/elliott-price-056124348/',
        backgroundColour: '#0077B5',
    },
    {
        icon: 'https://kyoko.openprocessing.org/profileImages/user165611.jpg',
        altText: 'OpenProcessing',
        link: 'https://openprocessing.org/user/360219',
        backgroundColour: '#333333',
    },
    {
        icon: 'https://chainbroker.io/_next/image/?url=https%3A%2F%2Fstatic.chainbroker.io%2Fmediafiles%2Fprojects%2Ffxhash%2Ffxhash.jpeg&w=2560&q=75',
        altText: 'fxhash',
        link: 'https://www.fxhash.xyz/u/shminge',
        backgroundColour: '#000000',
    },
    {
        icon: 'https://codestats.net/assets/frontend/images/Logo-92e1d93256eae2d7dde539f1df59b06c.svg?vsn=d',
        altText: 'Code::Stats',
        backgroundColour: '#F2B866',
        link: 'https://codestats.net/users/shminge'
    }
]

export default function Home() {
    return (
        <main className="p-8 space-y-8 max-w-5xl mx-auto">
            {/* Title and Menu Bar */}
            <Header />

            {/* Content Area */}
            <section className="flex flex-row gap-8">
                {/* Text */}
                <div className="flex-1 max-w-full">
                    <p className="mb-4 break-words"> 
                        This is heavily under construction. Check back later!
                    </p>
                    <ul className="space-y-2 list-disc list-inside">
                        <li>
                            <Link href="/blog/hello-world" className="text-blue-600 hover:underline">
                                Hello World
                            </Link>
                        </li>
                    </ul>
                </div>

                {/* Link Widget Grid */}
                <div className="w-max  ml-auto">
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-1">
                        {links.map((link, index) => (
                            <LinkWidget key={index} {...link} />
                        ))}
                    </div>
                </div>
            </section>
        </main>
    )
}
