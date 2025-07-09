import fs from 'fs'
import path from 'path'
import { GetStaticPaths, GetStaticProps } from 'next'
import { MDXRemote, MDXRemoteSerializeResult } from 'next-mdx-remote'
import { serialize } from 'next-mdx-remote/serialize'
import FancyBox from '../../components/FancyBox'

const components = { FancyBox }


/**
 * This is the default export, so Nextjs will render this during build phase.
 * The PostPage takes in a mdx source, and frontmatter that can change stuff.
 * @param source
 * @param frontMatter
 * @constructor
 */
export default function PostPage({
                                     source,
                                     frontMatter,
                                 }: {
    source: MDXRemoteSerializeResult
    frontMatter: any
}) {
    console.log("Building page with " + JSON.stringify(frontMatter))
    return (
        <main style={{ padding: '2rem' }}>
            <h1>{frontMatter.title}</h1>
            <p>{frontMatter.date}</p>
            <MDXRemote {...source} components={components} />
        </main>
    )
}

/**
 * We want to be able to dynamically handle /blog/*.mdx, so we read which exist in order to tell nextjs to make them.
 */
export const getStaticPaths: GetStaticPaths = async () => {
    console.log("getStaticPaths called")
    // Grab the files out of /posts/
    const files = fs.readdirSync(path.join(process.cwd(), 'posts'))

    // for each file, we pass it as a potential slug value.
    const paths = files.map((file) => ({
        params: { slug: file.replace(/\.mdx$/, '') },
    }))

    return { paths, fallback: false }
}


/**
 * This function takes the params created by getStaticPaths and turns them into props to populate the page with.
 * @param params
 */
export const getStaticProps: GetStaticProps = async ({ params }) => {
    console.log("getStaticProps called with:", params)
    const slug = params?.slug as string
    const filepath = path.join(process.cwd(), 'posts', `${slug}.mdx`)
    const source = fs.readFileSync(filepath, 'utf8')

    const mdxSource = await serialize(source, {
        parseFrontmatter: true,
    })

    return {
        props: {
            source: mdxSource,
            frontMatter: mdxSource.frontmatter,
        },
    }
}
