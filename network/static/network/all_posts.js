// All posts Page

function AllPosts(){
    // Return allposts conatiner
    return (
        <div id="allposts_page" class="page">
            <span>All posts</span>
        </div>
    );
}

// Render All Posts page to the DOM
ReactDOM.render(<AllPosts />, document.querySelector('#allposts_wrapper'));
