// All posts Page

function Home(){
    // Return allposts conatiner
    return (
        <div id="home_page" class="page">
            <span>Home</span>
        </div>
    );
}

// Render All Posts page to the DOM
ReactDOM.render(<Home />, document.querySelector('#home_wrapper'));
