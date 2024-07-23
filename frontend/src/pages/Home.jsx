import React, { useEffect, useState } from 'react';
import { getPosts } from '../services/postService';
import Post from '../components/Post';

function Home() {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        const fetchPosts = async () => {
            const posts = await getPosts();
            setPosts(posts);
        };
        fetchPosts();
    }, []);

    return (
        <div>
            {posts.length > 0 ? posts.map((post) => (
                <Post key={post.id} post={post} />
            )) : 'Loading...'}
        </div>
    );
}

export default Home;