import React from 'react';

function Post({ post }) {
    return (
        <div className="post">
            <h2 className="post-title">{post.title}</h2>
            <p className="post-content">{post.content}</p>
            <p className="post-author">Posted by {post.author}</p>
        </div>
    );
}

export default Post;