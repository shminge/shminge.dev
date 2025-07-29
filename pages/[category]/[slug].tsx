import fs from 'fs'
import path from 'path'
import { GetStaticPaths, GetStaticProps } from 'next'
import { MDXRemote, MDXRemoteSerializeResult } from 'next-mdx-remote'
import { serialize } from 'next-mdx-remote/serialize'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import Spoiler from '../../components/spoiler'
import '../../styles/globals.css'
import Link from 'next/link'

const components = {
    Spoiler,
    Link,
    h1: (props: any) => <h1 {...props} />,
    p: (props: any) => <p {...props} />,
}

export default function PostPage({
    source,
    frontMatter,
}: {
    source: MDXRemoteSerializeResult
    frontMatter: any
}) {
    return (
        <div className="content">
            <MDXRemote {...source} components={components} />
        </div>
    )
}

export const getStaticPaths: GetStaticPaths = async () => {
    const categories = ['blog', 'puzzles']
    const paths: { params: { category: string; slug: string } }[] = []

    for (const category of categories) {
        const files = fs.readdirSync(path.join(process.cwd(), `mdx-src/${category}`))

        files.forEach((file) => {
            paths.push({
                params: {
                    category,
                    slug: file.replace(/\.mdx$/, ''),
                },
            })
        })
    }

    return { paths, fallback: false }
}

export const getStaticProps: GetStaticProps = async ({ params }) => {
    const category = params?.category as string
    const slug = params?.slug as string

    const filepath = path.join(process.cwd(), `mdx-src/${category}`, `${slug}.mdx`)
    const source = fs.readFileSync(filepath, 'utf8')

    const mdxSource = await serialize(source, {
        parseFrontmatter: true,
        mdxOptions: {
            remarkPlugins: [remarkMath],
            rehypePlugins: [rehypeKatex],
        },
    })

    return {
        props: {
            source: mdxSource,
            frontMatter: mdxSource.frontmatter,
        },
    }
}
