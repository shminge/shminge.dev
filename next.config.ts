import type { NextConfig } from "next";
import withMDX from "@next/mdx";

// Enable `.mdx` file support
const withMDXConfig = withMDX({
    extension: /\.mdx?$/,
});

// Your base Next.js config
const baseConfig: NextConfig = {
    pageExtensions: ["ts", "tsx", "mdx"], // allow MDX pages
    reactStrictMode: true,
    // add other Next config options here
};

// Combine both
export default withMDXConfig(baseConfig);
