/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        remotePatterns: [
            {
                protocol: 'https',
                hostname: 'ai-news-fvca.onrender.com',
            },
            {
                protocol: 'https',
                hostname: 'images.pexels.com',
            }
        ],
    },
};

export default nextConfig;
