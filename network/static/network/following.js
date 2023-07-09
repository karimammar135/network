// All posts Page

function Following(){
    // Return allposts conatiner
    return (
        <div id="following_page" class="page">
            <span>Following</span>
        </div>
    );
}

// Render All Posts page to the DOM
ReactDOM.render(<Following />, document.querySelector('#following_wrapper'));
